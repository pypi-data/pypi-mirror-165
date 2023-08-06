class NewMetaClass(type):
    def __new__(cls, what, bases=None, dict=None):
        if "print_msg" in dict:
            print("Hello World!")
        else:
            raise Exception("print_msg missing")

        return type.__new__(cls, what, bases, dict)

