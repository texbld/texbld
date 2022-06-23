def error(*s):
    print("\033[91mError:\033[0m", *s)


def progress(*s):
    print("\033[93mTeXbld:\033[0m", *s)


def done(*s):
    print("\033[92mTeXbld:\033[0m", *s)
