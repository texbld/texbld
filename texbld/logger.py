import sys


def error(*s):
    sys.stderr.write(" ".join(["\033[91mTeXbld Error:\033[0m", *s]) + "\n")


def progress(*s):
    sys.stderr.write(" ".join(["\033[93mTeXbld:\033[0m", *s]) + "\n")


def done(*s):
    sys.stderr.write(" ".join(["\033[92mTeXbld:\033[0m", *s]) + "\n")
