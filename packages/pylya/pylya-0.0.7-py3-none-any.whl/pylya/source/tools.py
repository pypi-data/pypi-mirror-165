import distutils.sysconfig as sysconfig
import pkgutil
import inspect
import importlib.util
import glob
from pathlib import Path
import os
import sys
import json


wrapped = []


MODULE_EXTENSIONS = '.py'


class Namespace:  # May be used later
    __instance = None
    
    # If there is no Namespace, __init__ initializes
    # the function_map dictionary and the Namespace (__instance member variable).
    # Otherwise, if there is already one, it raises an exception.
    def __init__(self):
        if self.__instance is None:
            self.function_map = dict()
            Namespace.__instance = self
        else:
            raise Exception("cannot instantiate a virtual Namespace again")

    @staticmethod
    def get_instance():
        if Namespace.__instance is None:
            Namespace()
        return Namespace.__instance
    
    # adds the function to the function_map dictionary
    def register(self, fn, *args):
        func = Wrapper(fn)
        print(func.key())
        self.function_map[func.key()] = fn
        return func
    
    # takes the function from the function_map dictionary
    def get(self, fn, *args):
        func = Wrapper(fn)
        print(func.key(args=args))
        return self.function_map.get(func.key(args=args))


# new
class Visitor(ast.NodeVisitor):
    def __init__(
            self,
            parts: Sequence[str],
            srcs: Iterable[str],
            *,
            never: bool,
    ) -> None:
        self.parts = parts
        self.srcs = srcs
        self.to_replace: MutableMapping[int, Tuple[str, str]] = {}
        self.never = never

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        level = node.level
        is_absolute = level == 0
        absolute_import = '.'.join(self.parts[:-level])

        should_be_relative = bool(self.never)
        if is_absolute ^ should_be_relative:
            self.generic_visit(node)
            return

        def is_python_file_or_dir(path: str) -> bool:
            return os.path.exists(path+'.py') or os.path.isdir(path)

        if should_be_relative:
            assert node.module is not None  # help mypy
            if not any(
                    is_python_file_or_dir(
                        os.path.join(src, *node.module.split('.')),
                    ) for src in self.srcs
            ):
                # Can't convert to relative, might be third-party
                return
            depth = _find_relative_depth(self.parts, node.module)
            if depth == 0:
                # don't attempt relative import beyond top-level package
                return
            inverse_depth = len(self.parts) - depth
            if node.module == '.'.join(self.parts[:depth]):
                n_dots = inverse_depth
            else:
                # e.g. from a.b.c import d -> from ..c import d
                n_dots = inverse_depth - 1
            replacement = f'\\1{"."*n_dots}'

            self.to_replace[node.lineno] = (
                    rf'(from\s+){".".join(self.parts[:depth])}',
                    replacement,
            )
            self.generic_visit(node)
            return

        if node.module is None:
            # e.g. from . import b
            self.to_replace[
                node.lineno
            ] = (rf'(from\s+){"."*level}\s*', f'\\1{absolute_import} ')
        else:
            # e.g. from .b import c
            module = node.module
            self.to_replace[
                node.lineno
            ] = (
                rf'(from\s+){"."*level}{module}',
                f'\\1{absolute_import}.{module}',
            )

        self.generic_visit(node)


def get_object_methods():
    """Get all object's methods as a set of strings."""
    return {method_name for method_name in dir(object)
            if callable(getattr(object, method_name))}


def get_str_methods():
    """Get all str's methods as a set of strings.
    Only str's, which do not belong to object."""
    all_str_methods = {method_name for method_name in dir("")
                       if callable(getattr("", method_name))}
    return all_str_methods - object_methods


def get_list_methods():
    """Get all list's methods as a set of strings.
    Only list's, which do not belong to object."""
    all_list_methods = {method_name for method_name in dir([])
                        if callable(getattr([], method_name))}
    return all_list_methods - object_methods


object_methods = get_object_methods()
str_methods = get_str_methods()
list_methods = get_list_methods()


def overload(fn):
    func = Wrapper(fn)
    return func #Namespace.get_instance().register(fn)


def isNotWrapped(name):
    """
    'name' is a string and it is the name of the module.
    Adds 'name' and returns True if 'name' doesn't exist in list 'wrapped'.
    Returns False if 'name' exists in the list.
    """
    global wrapped

    if name in wrapped:
        return False
    else:
        wrapped.append(name)
        return True


def package_contents(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return set()
   
    pathname = Path(spec.origin).parent
    ret = set()
    with os.scandir(pathname) as entries:
        for entry in entries:
            if entry.name.startswith('__'):
                continue
            current = '.'.join((package_name, entry.name.partition('.')[0]))
            if entry.is_file():
                if entry.name.endswith(MODULE_EXTENSIONS):
                    ret.add(current)
            elif entry.is_dir():
                ret.add(current)
                ret |= package_contents(current)


    return ret


# Used to get built-in and standard library module names
# -------
# Lets make a file that contains all the external functions used to generate the string, etc
def generateBuiltinsNames():
    # Get list of the loaded source modules on sys.path.
    modules = {
            module
            for _, module, package in list(pkgutil.iter_modules())
            if package is False
            }

    # Glob all the 'top_level.txt' files installed under site-packages.
    site_packages = glob.iglob(os.path.join(os.path.dirname(os.__file__) + '/site-packages', '*-info', 'top_level.txt'))

    # Read the files for the import names and remove them from the modules list.
    modules -= {open(txt).read().strip() for txt in site_packages}

    # Get the system packages.
    system_modules = set(sys.builtin_module_names)

    # Get the just the top-level packages from the python install.
    python_root = sysconfig.get_python_lib(standard_lib=True)
    _, top_level_libs, _ = list(os.walk(python_root))[0]

    saved = sorted(top_level_libs + list(modules | system_modules))
    
    #saved = []
    #for pkg_name in saved_pkgs:
    #    saved += list(package_contents(pkg_name))

    #saved = [name for pkg_name in saved_pkgs for _, name, _ in pkgutil.iter_modules([pkg_name])]
    
    # Packages + subpackages and modules
    #saved = saved_pkgs + saved

    with open("saved.json", "w") as f:
        json.dump(saved, f)  # Should remove the usermade module names

    return saved


# new
def _find_relative_depth(parts: Sequence[str], module: str) -> int:
    depth = 0
    for n, _ in enumerate(parts, start=1):
        if module.startswith('.'.join(parts[:n])):
            depth += 1
        else:
            break
    return depth


# new
def absolute_imports(
        contents_text: str,
        srcs: Iterable[str], 
) -> str:
    #relative_paths = []
    #possible_srcs = []
    #path = Path(file).resolve()
    #for src in srcs:
    #    try:
    #        path_relative_to_i = path.relative_to(src)
    #    except ValueError:
    #        # `relative_path` can't be resolved relative to `i`
    #        pass
    #    else:
    #        relative_paths.append(path_relative_to_i)
    #        possible_srcs.append(src)
    #if not relative_paths:
    #    raise ValueError(
    #        f'{file} can\'t be resolved relative to the current directory.\n'
    #        'Either run absolufy-imports from the project root, or pass\n'
    #        '--application-directories',
    #    )
    #relative_path = min(relative_paths, key=lambda x: len(x.parts))

    #with open(file, 'rb') as fb:
    #    contents_bytes = fb.read()
    #try:
    #    contents_text = contents_bytes.decode()
    #except UnicodeDecodeError:
    #    print(f'{file} is non-utf-8 (not supported)')
    #    return 1
    try:
        tree = ast.parse(contents_text)
    except SyntaxError:
        return 0
    print(contents_text)
    visitor = Visitor(
        relative_path.parts,
        srcs,
        never=never,
    )
    visitor.visit(tree)

    if not visitor.to_replace:
        return 0

    newlines = []
    for lineno, line in enumerate(
        contents_text.splitlines(keepends=True), start=1,
    ):
        if lineno in visitor.to_replace:
            re1, re2 = visitor.to_replace[lineno]
            line = re.sub(re1, re2, line)
        newlines.append(line) 
    code = ''.join(newlines)
    return code


generateBuiltinsNames()

