from importlib.util import *
from importlib._bootstrap import *
from inspect import getmembers, isfunction, isclass, ismethod, stack
import sys
import builtins
import atexit
import json


access = {}
used_self = None
init_mod_attr = ['__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']

_NEEDS_LOADING = object()


class Wrapper:
    """Wraps a function, class or class method and, when it is called, puts its usage
    in the 'access' dictionary with an indicator if it's allowed or not.

    ----Member variables----
    wrap_init:    Used to check if function is used to initialize the locals with
                  wrapped built-in functions.
    wrapped:      The function/class/classmethod to wrap.
    mod_name:     The name of the module, where the function is defined.
    caller_class: The class, where the method belongs to.
                  Has value, if it's a class method or class function.
                  None, otherwise.
    """
    def __init__(self, wrapped, mod_name, caller_class=None):
        self.wrap_init = True
        self.wrapped = wrapped
        self.mod_name = mod_name
        self.caller_class = caller_class

    def __new__(cls, *args, **kwargs):
        global used_self

        used_self = object.__new__(cls)
        return used_self

    def __setattr__(self, name, value):
        try:
            w_init = self.__dict__['wrap_init']
        except KeyError:
            w_init = value
            self.__dict__['wrap_init'] = w_init
        try:
            wrapped = self.__dict__['wrapped']
        except KeyError:
            wrapped = value
            self.__dict__['wrapped'] = wrapped
        try:
            mod_name = self.__dict__['mod_name']
        except KeyError:
            mod_name = value
            self.__dict__['mod_name'] = mod_name
        try:
            caller_class = self.__dict__['caller_class']
        except KeyError:
            caller_class = value
            self.__dict__['caller_class'] = caller_class
        if not w_init:
            self.wrapped.__dict__[name] = value
        else:
            self.__dict__[name] = value

    def __get__(self, instance, owner=None):
        return self.wrapped.__get__(instance, owner)

    def __getattr__(self, name):
        if name not in dir(self.wrapped):
            if name == '__bases__':
                return self.wrapped.__bases__
            if name == '__mro_entries__':
                return self.wrapped.__mro_entries__
        return getattr(self.wrapped, name)

    #def __getattribute__(self, name):
    #    if self.wrapped.__name__ == 'super':
    #        return object.__getattribute__(self.wrapped, name)
    #    return object.__getattribute__(self, name)

    def getoriginalclass(self):
        return self.caller_class

    def __call__(self, *args, **kwargs):
        global access

        #fn = Namespace.get_instance().get(self.fn, *args)
        #if not fn:
        #    raise Exception("no matching function found.")
        #print(*args, **kwargs)
        #if self.mod_name == 'random':
        #    print(*args, **kwargs)

        if not (self.wrap_init and self.wrapped.__name__ == "getattr"):
            if self.caller_class:  # if it's a method or class function
                key = self.mod_name + "." + self.caller_class.__name__ + "." + self.wrapped.__name__
                val = "allow"
            else:  # function or class
                if self.mod_name == "builtins":
                    key = self.wrapped.__name__
                    val = "allow"
                else:
                    key = self.mod_name + "." + self.wrapped.__name__
                    val = "allow"
            f = list(sys._current_frames().values())[0]
            if '__file__' in f.f_back.f_globals:
                path = f.f_back.f_globals['__file__']  # The path of the caller module
                if path not in access.keys():
                    """if it's the first time a function is called
                    create a new dictionary item for access
                    and put the message inside of it
                    """
                    access[path] = {key: val}
                else:
                    """else, add the message as element in the list
                    with the path of the module imported as key
                    """
                    access[path][key] = val
        else:
            self.wrap_init = False

        st_locals = stack()[1][0].f_locals

        if self.caller_class:  # class method/function
            caller_self = st_locals.get('self', None)
            if caller_self:
                return self.wrapped(caller_self, *args, **kwargs)
            else:
                return self.wrapped(self.caller_class, *args, **kwargs)

        args = list(args)

        for i in range(len(args)):
            if isinstance(args[i], Wrapper):
                args[i] = args[i].wrapped

        # arguments of super must be type and not Wrapper

        if self.wrapped.__name__ == 'super':
            if len(args) == 0:
                owner_class = st_locals.get('__class__', None)
                owner_obj = st_locals.get('cls', None)
                if owner_obj is None:
                    owner_obj = st_locals.get('self', None)
                return self.wrapped(owner_class, owner_obj)

        # same for isinstance

        if self.wrapped.__name__ == 'isinstance':

            # args[1] = class/type/tuple
            if isinstance(args[1], tuple):
                args[1] = list(args[1])
                for i in range(len(args[1])):
                    if isinstance(args[1][i], Wrapper):
                        args[1][i] = args[1][i].wrapped
                args[1] = tuple(args[1])

        # same for issubclass

        if self.wrapped.__name__ == 'issubclass':
            for i in range(len(args)):
                if isinstance(args[i], Wrapper):
                    args[i] = args[i].getoriginalclass()

        # handle type and fix metaclass conflict

        if self.wrapped.__name__ == 'type':
            if len(args) > 1:  # it's meant to have 3 arguments
                args[1] = list(args[1])  # args[1] = list(bases) = bases
                # change every Wrapper object of bases to its content
                for i in range(len(args[1])):
                    if isinstance(args[1][i], Wrapper):
                        args[1][i] = args[1][i].wrapped
                args[1] = tuple(args[1])

        if self.wrapped.__name__ == 'eval':
            args.append(st_locals)

        args = tuple(args)

        # normal function or class

        return self.wrapped(*args, **kwargs)

    #def key(self, args=None):
    #    if args is None:
    #        args = getfullargspec(self.fn).args
    #
    #    return tuple([
    #        self.fn.__module__,
    #        self.fn.__class__,
    #        self.fn.__name__,
    #        len(args or []),
    #    ])


# __build_class__ C function is called when we use the class statement,
# so we use it to unwrap potentially wrapped base classes.
# TODO: Maybe add its usage to access

build_class_orig = builtins.__build_class__


def build_class_hook(func, className, *baseClasses, **kw):
    """Hook for __build_class__ to unwrap its base classes.
    If they are of type Wrapper, convert them to the original ones,
    to avoid bugs in inheritance.
    """
    baseClasses = list(baseClasses)
    for i in range(len(baseClasses)):
        if isinstance(baseClasses[i], Wrapper):
            baseClasses[i] = baseClasses[i].wrapped
    baseClasses = tuple(baseClasses)
    return build_class_orig(func, className, *baseClasses, **kw)


builtins.__build_class__ = build_class_hook


# TODO: In the future we will add a function to dynamically remove items from prologue
# Removed 'from meta import NewMetaClass'
# TODO: Remove all the resttt of errors
# Excluded : Exception, FileExistsError,
# OSError, __package__, __spec__, __name__, DeprecationWarning,
# UserWarning, ValueError, Warning, IOError, TypeError,
# RuntimeError, KeyError, AttributeError, UnicodeError, __doc__,
# IndexError, AssertionError, NameError, ImportError, MemoryError
# StopIteration, BaseException, True, False, NotImplemented
# __loader__
class Prologue:
    def __init__(self):
        self.prologue = "\nimport builtins\nfrom pylya.source.analysis import Wrapper\n\nbuiltin1 = ['ArithmeticError', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'EOFError', 'Ellipsis', 'EnvironmentError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'ImportWarning', 'IndentationError', 'InterruptedError', 'IsADirectoryError', 'KeyboardInterrupt', 'LookupError', 'ModuleNotFoundError', 'None', 'NotADirectoryError', 'NotImplementedError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeWarning', 'StopAsyncIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'ZeroDivisionError', '__build_class__', '__debug__', '__import__', 'abs', 'all', 'any', 'ascii', 'bin', 'breakpoint', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'format', 'frozenset', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip', 'getattr', 'locals', 'dict', 'bytes', 'bool', 'int', 'slice', 'bytearray', 'float', 'globals']\n\n# Wrap all built-in functions\nfor b in builtin1:\n\tlocals()[b] = Wrapper(getattr(builtins, b), 'builtins')\n"

    def getPrologue(self):
        """Return the value of prologue member variable."""
        return self.prologue


def _resolve_name(name, package, level):
    """(might be replaced by resolve_name)"""
    bits = package.rsplit('.', level - 1)
    if len(bits) < level:
        raise ValueError('attempted relative import beyond top-level package')
    base = bits[0]
    return '{}.{}'.format(base, name) if name else base


def _wrap_module_members(module):
    """Wrap the members of the given 'module'.

    After gathering all module's members and possible math's and _random's members
    differently (because these modules/libraries are written in C) wrap them with
    class Wrapper.
    - At this time, functions, classes and maybe class methods are getting wrapped.
    - There might be more CPython libraries, which might will have their members wrapped
    in the future.
    """
    name = module.__name__

    # Get imported module's functions, classes and their methods
    # (many of its functions, classes and methods are from analysis.py)
    all_func = set([fn[0] for fn in getmembers(module, isfunction)])
    all_class = set([c[0] for c in getmembers(module, isclass)])

    # Get analysis.py's functions, classes and their methods
    an_func = set([fn[0] for fn in getmembers(sys.modules[__name__], isfunction)])
    an_class = set([c[0] for c in getmembers(sys.modules[__name__], isclass)])

    # Imported module's functions without the analysis.py's functions
    func = all_func - an_func
    # Imported module's classes without the analysis.py's classes
    clas = all_class - an_class

    # Get possible math's functions and add them to the module's functions
    if 'math' in dir(module):
        math_mod = vars(module)['math']
        math_func = set()
        for fn in dir(math_mod):
            if isinstance(math_mod.__dict__[fn], types.BuiltinFunctionType):
                math_func.add(fn)
        func = func | math_func

    # Get possible _random's functions and add them to the module's functions
    if '_random' in dir(module):
        rand_mod = vars(module)['_random']
        rand_func = set()
        for fn in dir(rand_mod):
            if isinstance(rand_mod.__dict__[fn], types.BuiltinFunctionType):
                rand_func.add(fn)
        func = func | rand_func

    # Add possible _random's classses
    if '_random' in dir(module):
        rand_mod = vars(module)['_random']
        rand_cls = set()
        for c in dir(rand_mod):
            if isinstance(rand_mod.__dict__[c], type):
                rand_cls.add(c)
        clas = clas | rand_cls

    # Wrap all of them

    for fn in func:
        # math and _random are written in C
        if 'math' in dir(module) and fn in math_func:
            wrap = Wrapper(getattr(math_mod, fn), 'math')
            setattr(math_mod, fn, wrap)
        elif '_random' in dir(module) and fn in rand_func:  # fn in rand_func
            wrap = Wrapper(getattr(rand_mod, fn), '_random')
            setattr(rand_mod, fn, wrap)
        else:
            current_function = getattr(module, fn)
            if current_function.__module__ != module.__name__:
                continue
            # fn not in math_func nor in rand_func
            # and math nor _random were imported
            wrap = Wrapper(current_function, name)
            setattr(module, fn, wrap)

    for c in clas:
        if c not in init_mod_attr:
            caller_class = getattr(module, c)

            if caller_class.__module__ != module.__name__:
                continue

            # Wrap class's methods and functions first

            caller_class_methods = set([m[0] for m in getmembers(caller_class, ismethod)])
            if '_random' in dir(module) and c in rand_cls and c not in init_mod_attr:
                caller_class_methods |= set([m[0] for m in getmembers(getattr(rand_mod, c), ismethod)])

            # Classes have functions, too!
            caller_class_functions = set([f[0] for f in getmembers(caller_class, isfunction)])
            if '_random' in dir(module) and c in rand_cls and c not in init_mod_attr:
                caller_class_functions |= set([f[0] for f in getmembers(getattr(rand_mod, c), isfunction)])

            for m in caller_class_methods:
                wrap = Wrapper(getattr(caller_class, m), name, caller_class=caller_class)
                setattr(caller_class, m, wrap)
            for f in caller_class_functions:
                if '_random' in dir(module) and f in rand_func:  # f in rand_func
                    wrap = Wrapper(getattr(getattr(rand_mod, c), f), '_random', caller_class=getattr(rand_mod, c))
                    setattr(getattr(rand_mod, c), f, wrap)
                wrap = Wrapper(getattr(caller_class, f), name, caller_class=caller_class)
                setattr(caller_class, f, wrap)

            # Wrap the class

            if '_random' in dir(module) and c in rand_cls:
                wrap = Wrapper(getattr(rand_mod, c), '_random')
                setattr(rand_mod, c, wrap)
            else:
                wrap = Wrapper(caller_class, name)
                setattr(module, c, wrap)


def _call_with_frames_removed(f, *args, **kwds):
    return f(*args, **kwds)


def _analyze_import(name, locals_):
    """Wrap the analyzed module's functions and put their interactions
    in 'access' dictionary, after importing it.
    """
    global access

    try:
        return sys.modules[name]
    except KeyError:
        pass

    path = None
    if '.' in name:
        pname, _, cname = name.rpartition('.')
        if pname not in sys.modules:
            _call_with_frames_removed(_analyze_import, pname, locals_)
        pmodule = sys.modules[pname]
        path = pmodule.__spec__.submodule_search_locations
    for finder in sys.meta_path:
        if 'find_spec' not in dir(finder):
            # find and load module differently
            finder = finder.find_module(name, path)
            if finder is not None:
                module = finder.load_module(name)
                break
        else:
            ex_spec = finder.find_spec(name, path)
            if ex_spec is not None:
                module = module_from_spec(ex_spec)
                sys.modules[name] = module
                break
    else:
        msg = f'No module named {name!r}'
        raise ModuleNotFoundError(msg, name=name)

    # Put usage of import in access dictionary

    if locals_:
        if '__file__' in locals_:  # Ignore block when we import from interpreter (REPL)
            caller_path = locals_['__file__']  # The path of the caller module

            if caller_path not in access.keys():
                """if it's the first time a function is called
                create a new dictionary item for access
                and put the message inside of it
                """
                access[caller_path] = {"import": "allow"}
            else:
                """else, add the message as element in the list
                with the path of the module imported as key
                """
                access[caller_path]["import"] = "allow"

    prolObj = Prologue()
    prologue = prolObj.prologue # Get the function wrapping code
    ex_source = module.__spec__.loader.get_source(name) # Get an example code

    # Modify the ex_source:

    if ex_source:
        #ex_source = ex_source.replace('(type)', '(type.wrapped)')
        ex_source = ex_source.replace('str.maketrans', 'str.wrapped.maketrans')
    else:
        ex_source = ""

    if "from __future__ import" in ex_source:
        future_pos = ex_source.find("from __future__ import")
        # TODO: Fix bug when we use multiple lines for 'from __future__ import'
        future_instr = ex_source[future_pos:ex_source.find("\n", future_pos)]
        source_without_future = ex_source.replace(future_instr, "")
        source = future_instr + prologue + source_without_future
    else:
        source = prologue + ex_source

    codeObj = compile(source, module.__spec__.origin, 'exec')
    exec(codeObj, module.__dict__)

    _wrap_module_members(module)

    if path is not None:
        setattr(pmodule, cname, module)

    return module


def _handle_fromlist(module, fromlist, import_, locals_, *, recursive=False):
    """Figure out what __import__ should return.

    The import_ parameter is a callable which takes the name of module to
    import. It is required to decouple the function from assuming importlib's
    import implementation is desired.

    """
    # The hell that is fromlist ...
    # If a package was imported, try to import stuff from fromlist.
    for x in fromlist:
        if not isinstance(x, str):
            if recursive:
                where = module.__name__ + '.__all__'
            else:
                where = "``from list''"
            raise TypeError(f"Item in {where} must be str, "
                            f"not {type(x).__name__}")
        elif x == '*':
            if not recursive and hasattr(module, '__all__'):
                _handle_fromlist(module, module.__all__, import_,
                                 locals_, recursive=True)
        elif not hasattr(module, x):
            from_name = '{}.{}'.format(module.__name__, x)
            try:
                _call_with_frames_removed(import_, from_name, locals_)
            except ModuleNotFoundError as exc:
                # Backwards-compatibility dictates we ignore failed
                # imports triggered by fromlist for modules that don't
                # exist.
                if (exc.name == from_name and
                    sys.modules.get(from_name, _NEEDS_LOADING) is not None):
                    continue
                raise
    return module


# Excluded: random
def get_python_library():
    """Get all Python's native packages.

    These are built-in or standard library packages.
    Return them in a list of strings.
    """
    return ["urllib3", "pkg_resources", "requests",
            "__future__", "__pycache__", "_abc", "_ast", "_asyncio", "_bisect", "_blake2", "_bootlocale", "_bz2", "_codecs", "_codecs_cn", "_codecs_hk", "_codecs_iso2022", "_codecs_jp", "_codecs_kr", "_codecs_tw", "_collections", "_collections_abc", "_compat_pickle", "_compression", "_contextvars", "_crypt", "_csv", "_ctypes", "_ctypes_test", "_curses", "_curses_panel", "_datetime", "_dbm", "_decimal", "_dummy_thread", "_elementtree", "_functools", "_hashlib", "_heapq", "_imp", "_io", "_json", "_locale", "_lsprof", "_lzma", "_markupbase", "_md5", "_multibytecodec", "_multiprocessing", "_opcode", "_operator", "_osx_support", "_pickle", "_posixshmem", "_posixsubprocess", "_py_abc", "_pydecimal", "_pyio", "_queue", "_random", "_sha1", "_sha256", "_sha3", "_sha512", "_signal", "_sitebuiltins", "_socket", "_sqlite3", "_sre", "_ssl", "_stat", "_statistics", "_string", "_strptime", "_struct", "_symtable", "_sysconfigdata__linux_x86_64-linux-gnu", "_sysconfigdata__x86_64-linux-gnu", "_testbuffer", "_testcapi", "_testimportmultiple", "_testinternalcapi", "_testmultiphase", "_thread", "_threading_local", "_tkinter", "_tracemalloc", "_uuid", "_warnings", "_weakref", "_weakrefset", "_xxsubinterpreters", "_xxtestfuzz", "abc", "aifc", "analysis", "antigravity", "argparse", "array", "ast", "asynchat", "asyncio", "asyncore", "atexit", "audioop", "base64", "bdb", "binascii", "binhex", "bisect", "builtins", "bz2", "cProfile", "calendar", "cgi", "cgitb", "chunk", "cmath", "cmd", "code", "codecs", "codeop", "collections", "colorsys", "compileall", "concurrent", "config-3.8-x86_64-linux-gnu", "configparser", "contextlib", "contextvars", "copy", "copyreg", "crypt", "csv", "ctypes", "curses", "cycler", "dataclasses", "datetime", "dbm", "decimal", "difflib", "dis", "distutils", "doctest", "dummy_threading", "easy_install", "email", "encodings", "ensurepip", "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput", "fnmatch", "formatter", "fractions", "ftplib", "functools", "gc", "genericpath", "getopt", "getpass", "gettext", "glob", "grp", "gzip", "hashlib", "heapq", "hmac", "html", "http", "imaplib", "imghdr", "imp", "importlib", "inspect", "io", "ipaddress", "itertools", "json", "keyword", "kiwisolver", "lib-dynload", "lib2to3", "linecache", "locale", "logging", "lzma", "mailbox", "mailcap", "marshal", "math", "meta", "mimetypes", "mmap", "modulefinder", "multiprocessing", "netrc", "nis", "nntplib", "ntpath", "nturl2path", "numbers", "opcode", "operator", "optparse", "os", "ossaudiodev", "parser", "pathlib", "pdb", "pickle", "pickletools", "pipes", "pkgutil", "platform", "plistlib", "poplib", "posix", "posixpath", "pprint", "profile", "pstats", "pty", "pwd", "py_compile", "pyclbr", "pydoc", "pydoc_data", "pyexpat", "pylab", "pyparsing", "queue", "quopri", "re", "readline", "reprlib", "resource", "rlcompleter", "runpy", "sched", "secrets", "select", "selectors", "shelve", "shlex", "shutil", "signal", "site", "sitecustomize", "six", "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "spwd", "sqlite3", "sre_compile", "sre_constants", "sre_parse", "ssl", "stat", "statistics", "string", "stringprep", "struct", "subprocess", "sunau", "symbol", "symtable", "sys", "sysconfig", "syslog", "tabnanny", "tarfile", "telnetlib", "tempfile", "termios", "test", "textwrap", "this", "threading", "time", "timeit", "tkinter", "token", "tokenize", "trace", "traceback", "tracemalloc", "tty", "turtle", "types", "typing", "unicodedata", "unittest", "urllib", "uu", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser", "wsgiref", "xdrlib", "xml", "xmlrpc", "xxlimited", "xxsubtype", "zipapp", "zipfile", "zipimport", "zlib"]


modules = get_python_library()


def _calculate_package(globals):
    """Calculate what __package__ should be.

    __package__ is not guaranteed to be defined or could be set to None
    to represent that its proper value is unknown.
    """
    package = globals.get('__package__')
    spec = globals.get('__spec__')
    if package is not None:
        return package
    elif spec is not None:
        return spec.parent
    else:
        package = globals['__name__']
        if '__path__' not in globals:
            package = package.rpartition('.')[0]
    return package


def _import(name, globals=None, locals=None, fromlist=(), level=0):
    """Wrap the user made modules with code that wraps the built-in functions.
    Ignore the built-in modules and standard library modules and import them originally.
    Ignore the already wrapped modules and don't do anything in this case.
    """
    global modules

    # If level > 0 means that we are working with relative import
    # so you need to resolve the correct name.

    if level > 0:
        globals_ = globals if globals is not None else {}
        package = _calculate_package(globals_)
        name = _resolve_name(name, package, level)
        level = 0

    # Handle native packages

    # cpython modules
    if name in ['numpy.core._multiarray_umath', 'numpy.core._multiarray_tests',
                'numpy.random.mtrand', 'numpy.random.bit_generator',
                'numpy.random._common', 'numpy.random._bounded_integers',
                'numpy.random._philox', 'numpy.random._pcg64',
                'numpy.random._sfc64', 'numpy.random._generator', 'plum.function',
                'matplotlib._path', 'matplotlib._c_internal_utils'
                'matplotlib._contour', 'matplotlib._image', 'matplotlib._qhull',
                'matplotlib._tri', 'matplotlib._ttconv', 'matplotlib.ft2font']:
        return original_import(name, globals, locals, fromlist, level)

    rname = name
    while '.' in rname:
        rname, _, _ = rname.rpartition('.')

    # 'rname' is the leftmost name of the module's name
    # if 'rname' is one of the native packages taken from 'modules',
    # we just import the module without analyzing it.
    if rname in modules:
        return original_import(name, globals, locals, fromlist, level)

    module = _analyze_import(name, locals)

    # TODO: describe code bellow
    if not fromlist:
        if level == 0:
            return _analyze_import(name.partition('.')[0], locals)
        elif not name:
            return module
        else:
            cut_off = len(name) - len(name.partition('.')[0])
            return sys.modules[module.__name__[:len(module.__name__)-cut_off]]
    elif hasattr(module, '__path__'):
        return _handle_fromlist(module, fromlist, _analyze_import, locals)
    else:
        return module


original_import = builtins.__import__
builtins.__import__ = _import


def exit_handler():
    """Save a list of function names and allow or deny
    in a json file when the program terminates.
    """
    print(access)
    with open("access.json", "w") as f:
        json.dump(access, f, indent=4, sort_keys=True)


atexit.register(exit_handler)
