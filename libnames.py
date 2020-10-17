names = [
    "__future__",       "__phello__.foo",  "_aix_support","_bootlocale",      "_bootsubprocess", "_collections_abc",
    "_compat_pickle",   "_compression",    "_markupbase", "_osx_support",     "_py_abc",         "_pydecimal",
    "_pyio",            "_sitebuiltins",   "_strptime",   "_threading_local", "_weakrefset",     "abc",
    "aifc",             "antigravity",     "argparse",    "ast",              "asynchat",        "asyncore",
    "base64",           "bdb",             "binhex",      "bisect",           "bz2",             "calendar",
    "cgi",              "cgitb",           "chunk",       "cmd",              "code",            "codecs",
    "codeop",           "colorsys",        "compileall",  "configparser",     "contextlib",      "contextvars",
    "copy",             "copyreg",         "cProfile",    "crypt",            "csv",             "dataclasses",
    "datetime",         "decimal",         "difflib",     "dis",              "doctest",         "enum",
    "filecmp",          "fileinput",       "fnmatch",     "formatter",        "fractions",       "ftplib",
    "functools",        "genericpath",     "getopt",      "getpass",          "gettext",         "glob",
    "graphlib",         "gzip",            "hashlib",     "heapq",            "hmac",            "imaplib",
    "imghdr",           "imp",             "inspect",     "io",               "ipaddress",       "keyword",
    "linecache",        "locale",          "lzma",        "mailbox",          "mailcap",         "mimetypes",
    "modulefinder",     "netrc",           "nntplib",     "ntpath",           "nturl2path",      "numbers",
    "opcode",           "operator",        "optparse",    "os",               "pathlib",         "pdb",
    "pickle",           "pickletools",     "pipes",       "pkgutil",          "platform",        "plistlib",
    "poplib",           "posixpath",       "pprint",      "profile",          "pstats",          "pty",
    "py_compile",       "pyclbr",          "pydoc",       "queue",            "quopri",          "random",
    "re",               "reprlib",         "rlcompleter", "runpy",            "sched",           "secrets",
    "selectors",        "shelve",          "shlex",       "shutil",           "signal",          "site",
    "smtpd",            "smtplib",         "sndhdr",      "socket",           "socketserver",    "sre_compile",
    "sre_constants",    "sre_parse",       "ssl",         "stat",             "statistics",      "string",
    "stringprep",       "struct",          "subprocess",  "sunau",            "symtable",        "sysconfig",
    "tabnanny",         "tarfile",         "telnetlib",   "tempfile",         "textwrap",        "this",
    "threading",        "timeit",          "token",       "tokenize",         "trace",           "traceback",
    "tracemalloc",      "tty",             "turtle",      "types",            "typing",          "uu",
    "uuid",             "warnings",        "wave",        "weakref",          "webbrowser",      "xdrlib",
    "zipapp",           "zipfile",         "zipimport"
]
table={
    "_abc":"_py_abc.cpp",
    "_weakref":"weakref.cpp"
}
def fix(name):
    global table
    if name in table:
        return table[name]
    return name