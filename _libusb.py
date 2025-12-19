r"""Wrapper for libusb.h

Generated with:
ctypesgen /usr/include/libusb-1.0/libusb.h -l usb-1.0 -o libusb.py

Do not modify this file.
"""

__docformat__ = "restructuredtext"

# Begin preamble for Python

import ctypes
import sys
from ctypes import *  # noqa: F401, F403

_int_types = (ctypes.c_int16, ctypes.c_int32)
if hasattr(ctypes, "c_int64"):
    # Some builds of ctypes apparently do not have ctypes.c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (ctypes.c_int64,)
for t in _int_types:
    if ctypes.sizeof(t) == ctypes.sizeof(ctypes.c_size_t):
        c_ptrdiff_t = t
del t
del _int_types



class UserString:
    def __init__(self, seq):
        if isinstance(seq, bytes):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq).encode()

    def __bytes__(self):
        return self.data

    def __str__(self):
        return self.data.decode()

    def __repr__(self):
        return repr(self.data)

    def __int__(self):
        return int(self.data.decode())

    def __long__(self):
        return int(self.data.decode())

    def __float__(self):
        return float(self.data.decode())

    def __complex__(self):
        return complex(self.data.decode())

    def __hash__(self):
        return hash(self.data)

    def __le__(self, string):
        if isinstance(string, UserString):
            return self.data <= string.data
        else:
            return self.data <= string

    def __lt__(self, string):
        if isinstance(string, UserString):
            return self.data < string.data
        else:
            return self.data < string

    def __ge__(self, string):
        if isinstance(string, UserString):
            return self.data >= string.data
        else:
            return self.data >= string

    def __gt__(self, string):
        if isinstance(string, UserString):
            return self.data > string.data
        else:
            return self.data > string

    def __eq__(self, string):
        if isinstance(string, UserString):
            return self.data == string.data
        else:
            return self.data == string

    def __ne__(self, string):
        if isinstance(string, UserString):
            return self.data != string.data
        else:
            return self.data != string

    def __contains__(self, char):
        return char in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.__class__(self.data[index])

    def __getslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, bytes):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other).encode())

    def __radd__(self, other):
        if isinstance(other, bytes):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other).encode() + self.data)

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self):
        return self.__class__(self.data.capitalize())

    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))

    def count(self, sub, start=0, end=sys.maxsize):
        return self.data.count(sub, start, end)

    def decode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())

    def encode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())

    def endswith(self, suffix, start=0, end=sys.maxsize):
        return self.data.endswith(suffix, start, end)

    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))

    def find(self, sub, start=0, end=sys.maxsize):
        return self.data.find(sub, start, end)

    def index(self, sub, start=0, end=sys.maxsize):
        return self.data.index(sub, start, end)

    def isalpha(self):
        return self.data.isalpha()

    def isalnum(self):
        return self.data.isalnum()

    def isdecimal(self):
        return self.data.isdecimal()

    def isdigit(self):
        return self.data.isdigit()

    def islower(self):
        return self.data.islower()

    def isnumeric(self):
        return self.data.isnumeric()

    def isspace(self):
        return self.data.isspace()

    def istitle(self):
        return self.data.istitle()

    def isupper(self):
        return self.data.isupper()

    def join(self, seq):
        return self.data.join(seq)

    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))

    def lower(self):
        return self.__class__(self.data.lower())

    def lstrip(self, chars=None):
        return self.__class__(self.data.lstrip(chars))

    def partition(self, sep):
        return self.data.partition(sep)

    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))

    def rfind(self, sub, start=0, end=sys.maxsize):
        return self.data.rfind(sub, start, end)

    def rindex(self, sub, start=0, end=sys.maxsize):
        return self.data.rindex(sub, start, end)

    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))

    def rpartition(self, sep):
        return self.data.rpartition(sep)

    def rstrip(self, chars=None):
        return self.__class__(self.data.rstrip(chars))

    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)

    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)

    def splitlines(self, keepends=0):
        return self.data.splitlines(keepends)

    def startswith(self, prefix, start=0, end=sys.maxsize):
        return self.data.startswith(prefix, start, end)

    def strip(self, chars=None):
        return self.__class__(self.data.strip(chars))

    def swapcase(self):
        return self.__class__(self.data.swapcase())

    def title(self):
        return self.__class__(self.data.title())

    def translate(self, *args):
        return self.__class__(self.data.translate(*args))

    def upper(self):
        return self.__class__(self.data.upper())

    def zfill(self, width):
        return self.__class__(self.data.zfill(width))


class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""

    def __init__(self, string=""):
        self.data = string

    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")

    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + sub + self.data[index + 1 :]

    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + self.data[index + 1 :]

    def __setslice__(self, start, end, sub):
        start = max(start, 0)
        end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start] + sub.data + self.data[end:]
        elif isinstance(sub, bytes):
            self.data = self.data[:start] + sub + self.data[end:]
        else:
            self.data = self.data[:start] + str(sub).encode() + self.data[end:]

    def __delslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]

    def immutable(self):
        return UserString(self.data)

    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, bytes):
            self.data += other
        else:
            self.data += str(other).encode()
        return self

    def __imul__(self, n):
        self.data *= n
        return self


class String(MutableString, ctypes.Union):

    _fields_ = [("raw", ctypes.POINTER(ctypes.c_char)), ("data", ctypes.c_char_p)]

    def __init__(self, obj=b""):
        if isinstance(obj, (bytes, UserString)):
            self.data = bytes(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(ctypes.POINTER(ctypes.c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from bytes
        elif isinstance(obj, bytes):
            return cls(obj)

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj.encode())

        # Convert from c_char_p
        elif isinstance(obj, ctypes.c_char_p):
            return obj

        # Convert from POINTER(ctypes.c_char)
        elif isinstance(obj, ctypes.POINTER(ctypes.c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(ctypes.cast(obj, ctypes.POINTER(ctypes.c_char)))

        # Convert from ctypes.c_char array
        elif isinstance(obj, ctypes.c_char * len(obj)):
            return obj

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)

    from_param = classmethod(from_param)


def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)


# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to ctypes.c_void_p.
def UNCHECKED(type):
    if hasattr(type, "_type_") and isinstance(type._type_, str) and type._type_ != "P":
        return type
    else:
        return ctypes.c_void_p


# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self, func, restype, argtypes, errcheck):
        self.func = func
        self.func.restype = restype
        self.argtypes = argtypes
        if errcheck:
            self.func.errcheck = errcheck

    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func

    def __call__(self, *args):
        fixed_args = []
        i = 0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i += 1
        return self.func(*fixed_args + list(args[i:]))


def ord_if_char(value):
    """
    Simple helper used for casts to simple builtin types:  if the argument is a
    string type, it will be converted to it's ordinal value.

    This function will raise an exception if the argument is string with more
    than one characters.
    """
    return ord(value) if (isinstance(value, bytes) or isinstance(value, str)) else value

# End preamble

_libs = {}
_libdirs = []

# Begin loader

"""
Load libraries - appropriately for all our supported platforms
"""
# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import ctypes
import ctypes.util
import glob
import os.path
import platform
import re
import sys


def _environ_path(name):
    """Split an environment variable into a path-like list elements"""
    if name in os.environ:
        return os.environ[name].split(":")
    return []


class LibraryLoader:
    """
    A base class For loading of libraries ;-)
    Subclasses load libraries for specific platforms.
    """

    # library names formatted specifically for platforms
    name_formats = ["%s"]

    class Lookup:
        """Looking up calling conventions for a platform"""

        mode = ctypes.DEFAULT_MODE

        def __init__(self, path):
            super(LibraryLoader.Lookup, self).__init__()
            self.access = dict(cdecl=ctypes.CDLL(path, self.mode))

        def get(self, name, calling_convention="cdecl"):
            """Return the given name according to the selected calling convention"""
            if calling_convention not in self.access:
                raise LookupError(
                    "Unknown calling convention '{}' for function '{}'".format(
                        calling_convention, name
                    )
                )
            return getattr(self.access[calling_convention], name)

        def has(self, name, calling_convention="cdecl"):
            """Return True if this given calling convention finds the given 'name'"""
            if calling_convention not in self.access:
                return False
            return hasattr(self.access[calling_convention], name)

        def __getattr__(self, name):
            return getattr(self.access["cdecl"], name)

    def __init__(self):
        self.other_dirs = []

    def __call__(self, libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            # noinspection PyBroadException
            try:
                return self.Lookup(path)
            except Exception:  # pylint: disable=broad-except
                pass

        raise ImportError("Could not load %s." % libname)

    def getpaths(self, libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # search through a prioritized series of locations for the library

            # we first search any specific directories identified by user
            for dir_i in self.other_dirs:
                for fmt in self.name_formats:
                    # dir_i should be absolute already
                    yield os.path.join(dir_i, fmt % libname)

            # check if this code is even stored in a physical file
            try:
                this_file = __file__
            except NameError:
                this_file = None

            # then we search the directory where the generated python interface is stored
            if this_file is not None:
                for fmt in self.name_formats:
                    yield os.path.abspath(os.path.join(os.path.dirname(__file__), fmt % libname))

            # now, use the ctypes tools to try to find the library
            for fmt in self.name_formats:
                path = ctypes.util.find_library(fmt % libname)
                if path:
                    yield path

            # then we search all paths identified as platform-specific lib paths
            for path in self.getplatformpaths(libname):
                yield path

            # Finally, we'll try the users current working directory
            for fmt in self.name_formats:
                yield os.path.abspath(os.path.join(os.path.curdir, fmt % libname))

    def getplatformpaths(self, _libname):  # pylint: disable=no-self-use
        """Return all the library paths available in this platform"""
        return []


# Darwin (Mac OS X)


class DarwinLibraryLoader(LibraryLoader):
    """Library loader for MacOS"""

    name_formats = [
        "lib%s.dylib",
        "lib%s.so",
        "lib%s.bundle",
        "%s.dylib",
        "%s.so",
        "%s.bundle",
        "%s",
    ]

    class Lookup(LibraryLoader.Lookup):
        """
        Looking up library files for this platform (Darwin aka MacOS)
        """

        # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
        # of the default RTLD_LOCAL.  Without this, you end up with
        # libraries not being loadable, resulting in "Symbol not found"
        # errors
        mode = ctypes.RTLD_GLOBAL

    def getplatformpaths(self, libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [fmt % libname for fmt in self.name_formats]

        for directory in self.getdirs(libname):
            for name in names:
                yield os.path.join(directory, name)

    @staticmethod
    def getdirs(libname):
        """Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        """

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [
                os.path.expanduser("~/lib"),
                "/usr/local/lib",
                "/usr/lib",
            ]

        dirs = []

        if "/" in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
            dirs.extend(_environ_path("LD_RUN_PATH"))

        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "macosx_app":
            dirs.append(os.path.join(os.environ["RESOURCEPATH"], "..", "Frameworks"))

        dirs.extend(dyld_fallback_library_path)

        return dirs


# Posix


class PosixLibraryLoader(LibraryLoader):
    """Library loader for POSIX-like systems (including Linux)"""

    _ld_so_cache = None

    _include = re.compile(r"^\s*include\s+(?P<pattern>.*)")

    name_formats = ["lib%s.so", "%s.so", "%s"]

    class _Directories(dict):
        """Deal with directories"""

        def __init__(self):
            dict.__init__(self)
            self.order = 0

        def add(self, directory):
            """Add a directory to our current set of directories"""
            if len(directory) > 1:
                directory = directory.rstrip(os.path.sep)
            # only adds and updates order if exists and not already in set
            if not os.path.exists(directory):
                return
            order = self.setdefault(directory, self.order)
            if order == self.order:
                self.order += 1

        def extend(self, directories):
            """Add a list of directories to our set"""
            for a_dir in directories:
                self.add(a_dir)

        def ordered(self):
            """Sort the list of directories"""
            return (i[0] for i in sorted(self.items(), key=lambda d: d[1]))

    def _get_ld_so_conf_dirs(self, conf, dirs):
        """
        Recursive function to help parse all ld.so.conf files, including proper
        handling of the `include` directive.
        """

        try:
            with open(conf) as fileobj:
                for dirname in fileobj:
                    dirname = dirname.strip()
                    if not dirname:
                        continue

                    match = self._include.match(dirname)
                    if not match:
                        dirs.add(dirname)
                    else:
                        for dir2 in glob.glob(match.group("pattern")):
                            self._get_ld_so_conf_dirs(dir2, dirs)
        except IOError:
            pass

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = self._Directories()
        for name in (
            "LD_LIBRARY_PATH",
            "SHLIB_PATH",  # HP-UX
            "LIBPATH",  # OS/2, AIX
            "LIBRARY_PATH",  # BE/OS
        ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))

        self._get_ld_so_conf_dirs("/etc/ld.so.conf", directories)

        bitage = platform.architecture()[0]

        unix_lib_dirs_list = []
        if bitage.startswith("64"):
            # prefer 64 bit if that is our arch
            unix_lib_dirs_list += ["/lib64", "/usr/lib64"]

        # must include standard libs, since those paths are also used by 64 bit
        # installs
        unix_lib_dirs_list += ["/lib", "/usr/lib"]
        if sys.platform.startswith("linux"):
            # Try and support multiarch work in Ubuntu
            # https://wiki.ubuntu.com/MultiarchSpec
            if bitage.startswith("32"):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ["/lib/i386-linux-gnu", "/usr/lib/i386-linux-gnu"]
            elif bitage.startswith("64"):
                # Assume Intel/AMD x86 compatible
                unix_lib_dirs_list += [
                    "/lib/x86_64-linux-gnu",
                    "/usr/lib/x86_64-linux-gnu",
                ]
            else:
                # guess...
                unix_lib_dirs_list += glob.glob("/lib/*linux-gnu")
        directories.extend(unix_lib_dirs_list)

        cache = {}
        lib_re = re.compile(r"lib(.*)\.s[ol]")
        # ext_re = re.compile(r"\.s[ol]$")
        for our_dir in directories.ordered():
            try:
                for path in glob.glob("%s/*.s[ol]*" % our_dir):
                    file = os.path.basename(path)

                    # Index by filename
                    cache_i = cache.setdefault(file, set())
                    cache_i.add(path)

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        cache_i = cache.setdefault(library, set())
                        cache_i.add(path)
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname, set())
        for i in result:
            # we iterate through all found paths for library, since we may have
            # actually found multiple architectures or other library types that
            # may not load
            yield i


# Windows


class WindowsLibraryLoader(LibraryLoader):
    """Library loader for Microsoft Windows"""

    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll", "%s"]

    class Lookup(LibraryLoader.Lookup):
        """Lookup class for Windows libraries..."""

        def __init__(self, path):
            super(WindowsLibraryLoader.Lookup, self).__init__(path)
            self.access["stdcall"] = ctypes.windll.LoadLibrary(path)


# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin": DarwinLibraryLoader,
    "cygwin": WindowsLibraryLoader,
    "win32": WindowsLibraryLoader,
    "msys": WindowsLibraryLoader,
}

load_library = loaderclass.get(sys.platform, PosixLibraryLoader)()


def add_library_search_dirs(other_dirs):
    """
    Add libraries to search paths.
    If library paths are relative, convert them to absolute with respect to this
    file's directory
    """
    for path in other_dirs:
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        load_library.other_dirs.append(path)


del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries
_libs["usb-1.0"] = load_library("usb-1.0")

# 1 libraries
# End libraries

# No modules

__uint8_t = c_ubyte# /usr/include/x86_64-linux-gnu/bits/types.h: 38

__uint16_t = c_ushort# /usr/include/x86_64-linux-gnu/bits/types.h: 40

__uint32_t = c_uint# /usr/include/x86_64-linux-gnu/bits/types.h: 42

__time_t = c_long# /usr/include/x86_64-linux-gnu/bits/types.h: 160

__suseconds_t = c_long# /usr/include/x86_64-linux-gnu/bits/types.h: 162

uint8_t = __uint8_t# /usr/include/x86_64-linux-gnu/bits/stdint-uintn.h: 24

uint16_t = __uint16_t# /usr/include/x86_64-linux-gnu/bits/stdint-uintn.h: 25

uint32_t = __uint32_t# /usr/include/x86_64-linux-gnu/bits/stdint-uintn.h: 26

intptr_t = c_long# /usr/include/stdint.h: 76

# /usr/include/x86_64-linux-gnu/bits/types/struct_timeval.h: 8
class struct_timeval(Structure):
    pass

struct_timeval.__slots__ = [
    'tv_sec',
    'tv_usec',
]
struct_timeval._fields_ = [
    ('tv_sec', __time_t),
    ('tv_usec', __suseconds_t),
]

# /usr/include/libusb-1.0/libusb.h: 198
class union_anon_15(Union):
    pass

union_anon_15.__slots__ = [
    'b8',
    'b16',
]
union_anon_15._fields_ = [
    ('b8', uint8_t * int(2)),
    ('b16', uint16_t),
]

# /usr/include/libusb-1.0/libusb.h: 198
for _lib in _libs.values():
    try:
        _tmp = (union_anon_15).in_dll(_lib, "_tmp")
        break
    except:
        pass

enum_libusb_class_code = c_int# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_PER_INTERFACE = 0x00# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_AUDIO = 0x01# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_COMM = 0x02# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_HID = 0x03# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_PHYSICAL = 0x05# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_IMAGE = 0x06# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_PTP = 0x06# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_PRINTER = 0x07# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_MASS_STORAGE = 0x08# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_HUB = 0x09# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_DATA = 0x0a# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_SMART_CARD = 0x0b# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_CONTENT_SECURITY = 0x0d# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_VIDEO = 0x0e# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_PERSONAL_HEALTHCARE = 0x0f# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_DIAGNOSTIC_DEVICE = 0xdc# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_WIRELESS = 0xe0# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_MISCELLANEOUS = 0xef# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_APPLICATION = 0xfe# /usr/include/libusb-1.0/libusb.h: 218

LIBUSB_CLASS_VENDOR_SPEC = 0xff# /usr/include/libusb-1.0/libusb.h: 218

enum_libusb_descriptor_type = c_int# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_DEVICE = 0x01# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_CONFIG = 0x02# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_STRING = 0x03# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_INTERFACE = 0x04# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_ENDPOINT = 0x05# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_INTERFACE_ASSOCIATION = 0x0b# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_BOS = 0x0f# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_DEVICE_CAPABILITY = 0x10# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_HID = 0x21# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_REPORT = 0x22# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_PHYSICAL = 0x23# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_HUB = 0x29# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_SUPERSPEED_HUB = 0x2a# /usr/include/libusb-1.0/libusb.h: 283

LIBUSB_DT_SS_ENDPOINT_COMPANION = 0x30# /usr/include/libusb-1.0/libusb.h: 283

enum_libusb_endpoint_direction = c_int# /usr/include/libusb-1.0/libusb.h: 361

LIBUSB_ENDPOINT_OUT = 0x00# /usr/include/libusb-1.0/libusb.h: 361

LIBUSB_ENDPOINT_IN = 0x80# /usr/include/libusb-1.0/libusb.h: 361

enum_libusb_endpoint_transfer_type = c_int# /usr/include/libusb-1.0/libusb.h: 375

LIBUSB_ENDPOINT_TRANSFER_TYPE_CONTROL = 0x0# /usr/include/libusb-1.0/libusb.h: 375

LIBUSB_ENDPOINT_TRANSFER_TYPE_ISOCHRONOUS = 0x1# /usr/include/libusb-1.0/libusb.h: 375

LIBUSB_ENDPOINT_TRANSFER_TYPE_BULK = 0x2# /usr/include/libusb-1.0/libusb.h: 375

LIBUSB_ENDPOINT_TRANSFER_TYPE_INTERRUPT = 0x3# /usr/include/libusb-1.0/libusb.h: 375

enum_libusb_standard_request = c_int# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_REQUEST_GET_STATUS = 0x00# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_REQUEST_CLEAR_FEATURE = 0x01# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_REQUEST_SET_FEATURE = 0x03# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_REQUEST_SET_ADDRESS = 0x05# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_REQUEST_GET_DESCRIPTOR = 0x06# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_REQUEST_SET_DESCRIPTOR = 0x07# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_REQUEST_GET_CONFIGURATION = 0x08# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_REQUEST_SET_CONFIGURATION = 0x09# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_REQUEST_GET_INTERFACE = 0x0a# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_REQUEST_SET_INTERFACE = 0x0b# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_REQUEST_SYNCH_FRAME = 0x0c# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_REQUEST_SET_SEL = 0x30# /usr/include/libusb-1.0/libusb.h: 391

LIBUSB_SET_ISOCH_DELAY = 0x31# /usr/include/libusb-1.0/libusb.h: 391

enum_libusb_request_type = c_int# /usr/include/libusb-1.0/libusb.h: 441

LIBUSB_REQUEST_TYPE_STANDARD = (0x00 << 5)# /usr/include/libusb-1.0/libusb.h: 441

LIBUSB_REQUEST_TYPE_CLASS = (0x01 << 5)# /usr/include/libusb-1.0/libusb.h: 441

LIBUSB_REQUEST_TYPE_VENDOR = (0x02 << 5)# /usr/include/libusb-1.0/libusb.h: 441

LIBUSB_REQUEST_TYPE_RESERVED = (0x03 << 5)# /usr/include/libusb-1.0/libusb.h: 441

enum_libusb_request_recipient = c_int# /usr/include/libusb-1.0/libusb.h: 459

LIBUSB_RECIPIENT_DEVICE = 0x00# /usr/include/libusb-1.0/libusb.h: 459

LIBUSB_RECIPIENT_INTERFACE = 0x01# /usr/include/libusb-1.0/libusb.h: 459

LIBUSB_RECIPIENT_ENDPOINT = 0x02# /usr/include/libusb-1.0/libusb.h: 459

LIBUSB_RECIPIENT_OTHER = 0x03# /usr/include/libusb-1.0/libusb.h: 459

enum_libusb_iso_sync_type = c_int# /usr/include/libusb-1.0/libusb.h: 480

LIBUSB_ISO_SYNC_TYPE_NONE = 0x0# /usr/include/libusb-1.0/libusb.h: 480

LIBUSB_ISO_SYNC_TYPE_ASYNC = 0x1# /usr/include/libusb-1.0/libusb.h: 480

LIBUSB_ISO_SYNC_TYPE_ADAPTIVE = 0x2# /usr/include/libusb-1.0/libusb.h: 480

LIBUSB_ISO_SYNC_TYPE_SYNC = 0x3# /usr/include/libusb-1.0/libusb.h: 480

enum_libusb_iso_usage_type = c_int# /usr/include/libusb-1.0/libusb.h: 501

LIBUSB_ISO_USAGE_TYPE_DATA = 0x0# /usr/include/libusb-1.0/libusb.h: 501

LIBUSB_ISO_USAGE_TYPE_FEEDBACK = 0x1# /usr/include/libusb-1.0/libusb.h: 501

LIBUSB_ISO_USAGE_TYPE_IMPLICIT = 0x2# /usr/include/libusb-1.0/libusb.h: 501

enum_libusb_supported_speed = c_int# /usr/include/libusb-1.0/libusb.h: 516

LIBUSB_LOW_SPEED_OPERATION = (1 << 0)# /usr/include/libusb-1.0/libusb.h: 516

LIBUSB_FULL_SPEED_OPERATION = (1 << 1)# /usr/include/libusb-1.0/libusb.h: 516

LIBUSB_HIGH_SPEED_OPERATION = (1 << 2)# /usr/include/libusb-1.0/libusb.h: 516

LIBUSB_SUPER_SPEED_OPERATION = (1 << 3)# /usr/include/libusb-1.0/libusb.h: 516

enum_libusb_usb_2_0_extension_attributes = c_int# /usr/include/libusb-1.0/libusb.h: 535

LIBUSB_BM_LPM_SUPPORT = (1 << 1)# /usr/include/libusb-1.0/libusb.h: 535

enum_libusb_ss_usb_device_capability_attributes = c_int# /usr/include/libusb-1.0/libusb.h: 545

LIBUSB_BM_LTM_SUPPORT = (1 << 1)# /usr/include/libusb-1.0/libusb.h: 545

enum_libusb_bos_type = c_int# /usr/include/libusb-1.0/libusb.h: 553

LIBUSB_BT_WIRELESS_USB_DEVICE_CAPABILITY = 0x01# /usr/include/libusb-1.0/libusb.h: 553

LIBUSB_BT_USB_2_0_EXTENSION = 0x02# /usr/include/libusb-1.0/libusb.h: 553

LIBUSB_BT_SS_USB_DEVICE_CAPABILITY = 0x03# /usr/include/libusb-1.0/libusb.h: 553

LIBUSB_BT_CONTAINER_ID = 0x04# /usr/include/libusb-1.0/libusb.h: 553

LIBUSB_BT_PLATFORM_DESCRIPTOR = 0x05# /usr/include/libusb-1.0/libusb.h: 553

LIBUSB_BT_SUPERSPEED_PLUS_CAPABILITY = 0x0A# /usr/include/libusb-1.0/libusb.h: 553

# /usr/include/libusb-1.0/libusb.h: 578
class struct_libusb_device_descriptor(Structure):
    pass

struct_libusb_device_descriptor.__slots__ = [
    'bLength',
    'bDescriptorType',
    'bcdUSB',
    'bDeviceClass',
    'bDeviceSubClass',
    'bDeviceProtocol',
    'bMaxPacketSize0',
    'idVendor',
    'idProduct',
    'bcdDevice',
    'iManufacturer',
    'iProduct',
    'iSerialNumber',
    'bNumConfigurations',
]
struct_libusb_device_descriptor._fields_ = [
    ('bLength', uint8_t),
    ('bDescriptorType', uint8_t),
    ('bcdUSB', uint16_t),
    ('bDeviceClass', uint8_t),
    ('bDeviceSubClass', uint8_t),
    ('bDeviceProtocol', uint8_t),
    ('bMaxPacketSize0', uint8_t),
    ('idVendor', uint16_t),
    ('idProduct', uint16_t),
    ('bcdDevice', uint16_t),
    ('iManufacturer', uint8_t),
    ('iProduct', uint8_t),
    ('iSerialNumber', uint8_t),
    ('bNumConfigurations', uint8_t),
]

# /usr/include/libusb-1.0/libusb.h: 632
class struct_libusb_endpoint_descriptor(Structure):
    pass

struct_libusb_endpoint_descriptor.__slots__ = [
    'bLength',
    'bDescriptorType',
    'bEndpointAddress',
    'bmAttributes',
    'wMaxPacketSize',
    'bInterval',
    'bRefresh',
    'bSynchAddress',
    'extra',
    'extra_length',
]
struct_libusb_endpoint_descriptor._fields_ = [
    ('bLength', uint8_t),
    ('bDescriptorType', uint8_t),
    ('bEndpointAddress', uint8_t),
    ('bmAttributes', uint8_t),
    ('wMaxPacketSize', uint16_t),
    ('bInterval', uint8_t),
    ('bRefresh', uint8_t),
    ('bSynchAddress', uint8_t),
    ('extra', POINTER(c_ubyte)),
    ('extra_length', c_int),
]

# /usr/include/libusb-1.0/libusb.h: 680
class struct_libusb_interface_association_descriptor(Structure):
    pass

struct_libusb_interface_association_descriptor.__slots__ = [
    'bLength',
    'bDescriptorType',
    'bFirstInterface',
    'bInterfaceCount',
    'bFunctionClass',
    'bFunctionSubClass',
    'bFunctionProtocol',
    'iFunction',
]
struct_libusb_interface_association_descriptor._fields_ = [
    ('bLength', uint8_t),
    ('bDescriptorType', uint8_t),
    ('bFirstInterface', uint8_t),
    ('bInterfaceCount', uint8_t),
    ('bFunctionClass', uint8_t),
    ('bFunctionSubClass', uint8_t),
    ('bFunctionProtocol', uint8_t),
    ('iFunction', uint8_t),
]

# /usr/include/libusb-1.0/libusb.h: 724
class struct_libusb_interface_association_descriptor_array(Structure):
    pass

struct_libusb_interface_association_descriptor_array.__slots__ = [
    'iad',
    'length',
]
struct_libusb_interface_association_descriptor_array._fields_ = [
    ('iad', POINTER(struct_libusb_interface_association_descriptor)),
    ('length', c_int),
]

# /usr/include/libusb-1.0/libusb.h: 739
class struct_libusb_interface_descriptor(Structure):
    pass

struct_libusb_interface_descriptor.__slots__ = [
    'bLength',
    'bDescriptorType',
    'bInterfaceNumber',
    'bAlternateSetting',
    'bNumEndpoints',
    'bInterfaceClass',
    'bInterfaceSubClass',
    'bInterfaceProtocol',
    'iInterface',
    'endpoint',
    'extra',
    'extra_length',
]
struct_libusb_interface_descriptor._fields_ = [
    ('bLength', uint8_t),
    ('bDescriptorType', uint8_t),
    ('bInterfaceNumber', uint8_t),
    ('bAlternateSetting', uint8_t),
    ('bNumEndpoints', uint8_t),
    ('bInterfaceClass', uint8_t),
    ('bInterfaceSubClass', uint8_t),
    ('bInterfaceProtocol', uint8_t),
    ('iInterface', uint8_t),
    ('endpoint', POINTER(struct_libusb_endpoint_descriptor)),
    ('extra', POINTER(c_ubyte)),
    ('extra_length', c_int),
]

# /usr/include/libusb-1.0/libusb.h: 787
class struct_libusb_interface(Structure):
    pass

struct_libusb_interface.__slots__ = [
    'altsetting',
    'num_altsetting',
]
struct_libusb_interface._fields_ = [
    ('altsetting', POINTER(struct_libusb_interface_descriptor)),
    ('num_altsetting', c_int),
]

# /usr/include/libusb-1.0/libusb.h: 802
class struct_libusb_config_descriptor(Structure):
    pass

struct_libusb_config_descriptor.__slots__ = [
    'bLength',
    'bDescriptorType',
    'wTotalLength',
    'bNumInterfaces',
    'bConfigurationValue',
    'iConfiguration',
    'bmAttributes',
    'MaxPower',
    'interface',
    'extra',
    'extra_length',
]
struct_libusb_config_descriptor._fields_ = [
    ('bLength', uint8_t),
    ('bDescriptorType', uint8_t),
    ('wTotalLength', uint16_t),
    ('bNumInterfaces', uint8_t),
    ('bConfigurationValue', uint8_t),
    ('iConfiguration', uint8_t),
    ('bmAttributes', uint8_t),
    ('MaxPower', uint8_t),
    ('interface', POINTER(struct_libusb_interface)),
    ('extra', POINTER(c_ubyte)),
    ('extra_length', c_int),
]

# /usr/include/libusb-1.0/libusb.h: 850
class struct_libusb_ss_endpoint_companion_descriptor(Structure):
    pass

struct_libusb_ss_endpoint_companion_descriptor.__slots__ = [
    'bLength',
    'bDescriptorType',
    'bMaxBurst',
    'bmAttributes',
    'wBytesPerInterval',
]
struct_libusb_ss_endpoint_companion_descriptor._fields_ = [
    ('bLength', uint8_t),
    ('bDescriptorType', uint8_t),
    ('bMaxBurst', uint8_t),
    ('bmAttributes', uint8_t),
    ('wBytesPerInterval', uint16_t),
]

# /usr/include/libusb-1.0/libusb.h: 879
class struct_libusb_bos_dev_capability_descriptor(Structure):
    pass

struct_libusb_bos_dev_capability_descriptor.__slots__ = [
    'bLength',
    'bDescriptorType',
    'bDevCapabilityType',
    'dev_capability_data',
]
struct_libusb_bos_dev_capability_descriptor._fields_ = [
    ('bLength', uint8_t),
    ('bDescriptorType', uint8_t),
    ('bDevCapabilityType', uint8_t),
    ('dev_capability_data', POINTER(uint8_t)),
]

# /usr/include/libusb-1.0/libusb.h: 900
class struct_libusb_bos_descriptor(Structure):
    pass

struct_libusb_bos_descriptor.__slots__ = [
    'bLength',
    'bDescriptorType',
    'wTotalLength',
    'bNumDeviceCaps',
    'dev_capability',
]
struct_libusb_bos_descriptor._fields_ = [
    ('bLength', uint8_t),
    ('bDescriptorType', uint8_t),
    ('wTotalLength', uint16_t),
    ('bNumDeviceCaps', uint8_t),
    ('dev_capability', POINTER(POINTER(struct_libusb_bos_dev_capability_descriptor))),
]

# /usr/include/libusb-1.0/libusb.h: 925
class struct_libusb_usb_2_0_extension_descriptor(Structure):
    pass

struct_libusb_usb_2_0_extension_descriptor.__slots__ = [
    'bLength',
    'bDescriptorType',
    'bDevCapabilityType',
    'bmAttributes',
]
struct_libusb_usb_2_0_extension_descriptor._fields_ = [
    ('bLength', uint8_t),
    ('bDescriptorType', uint8_t),
    ('bDevCapabilityType', uint8_t),
    ('bmAttributes', uint32_t),
]

# /usr/include/libusb-1.0/libusb.h: 951
class struct_libusb_ss_usb_device_capability_descriptor(Structure):
    pass

struct_libusb_ss_usb_device_capability_descriptor.__slots__ = [
    'bLength',
    'bDescriptorType',
    'bDevCapabilityType',
    'bmAttributes',
    'wSpeedSupported',
    'bFunctionalitySupport',
    'bU1DevExitLat',
    'bU2DevExitLat',
]
struct_libusb_ss_usb_device_capability_descriptor._fields_ = [
    ('bLength', uint8_t),
    ('bDescriptorType', uint8_t),
    ('bDevCapabilityType', uint8_t),
    ('bmAttributes', uint8_t),
    ('wSpeedSupported', uint16_t),
    ('bFunctionalitySupport', uint8_t),
    ('bU1DevExitLat', uint8_t),
    ('bU2DevExitLat', uint16_t),
]

enum_libusb_superspeedplus_sublink_attribute_sublink_type = c_int# /usr/include/libusb-1.0/libusb.h: 991

LIBUSB_SSPLUS_ATTR_TYPE_SYM = 0# /usr/include/libusb-1.0/libusb.h: 991

LIBUSB_SSPLUS_ATTR_TYPE_ASYM = 1# /usr/include/libusb-1.0/libusb.h: 991

enum_libusb_superspeedplus_sublink_attribute_sublink_direction = c_int# /usr/include/libusb-1.0/libusb.h: 999

LIBUSB_SSPLUS_ATTR_DIR_RX = 0# /usr/include/libusb-1.0/libusb.h: 999

LIBUSB_SSPLUS_ATTR_DIR_TX = 1# /usr/include/libusb-1.0/libusb.h: 999

enum_libusb_superspeedplus_sublink_attribute_exponent = c_int# /usr/include/libusb-1.0/libusb.h: 1011

LIBUSB_SSPLUS_ATTR_EXP_BPS = 0# /usr/include/libusb-1.0/libusb.h: 1011

LIBUSB_SSPLUS_ATTR_EXP_KBS = 1# /usr/include/libusb-1.0/libusb.h: 1011

LIBUSB_SSPLUS_ATTR_EXP_MBS = 2# /usr/include/libusb-1.0/libusb.h: 1011

LIBUSB_SSPLUS_ATTR_EXP_GBS = 3# /usr/include/libusb-1.0/libusb.h: 1011

enum_libusb_superspeedplus_sublink_attribute_link_protocol = c_int# /usr/include/libusb-1.0/libusb.h: 1021

LIBUSB_SSPLUS_ATTR_PROT_SS = 0# /usr/include/libusb-1.0/libusb.h: 1021

LIBUSB_SSPLUS_ATTR_PROT_SSPLUS = 1# /usr/include/libusb-1.0/libusb.h: 1021

# /usr/include/libusb-1.0/libusb.h: 1029
class struct_libusb_ssplus_sublink_attribute(Structure):
    pass

struct_libusb_ssplus_sublink_attribute.__slots__ = [
    'ssid',
    'exponent',
    'type',
    'direction',
    'protocol',
    'mantissa',
]
struct_libusb_ssplus_sublink_attribute._fields_ = [
    ('ssid', uint8_t),
    ('exponent', enum_libusb_superspeedplus_sublink_attribute_exponent),
    ('type', enum_libusb_superspeedplus_sublink_attribute_sublink_type),
    ('direction', enum_libusb_superspeedplus_sublink_attribute_sublink_direction),
    ('protocol', enum_libusb_superspeedplus_sublink_attribute_link_protocol),
    ('mantissa', uint16_t),
]

# /usr/include/libusb-1.0/libusb.h: 1062
class struct_libusb_ssplus_usb_device_capability_descriptor(Structure):
    pass

struct_libusb_ssplus_usb_device_capability_descriptor.__slots__ = [
    'numSublinkSpeedAttributes',
    'numSublinkSpeedIDs',
    'ssid',
    'minRxLaneCount',
    'minTxLaneCount',
    'sublinkSpeedAttributes',
]
struct_libusb_ssplus_usb_device_capability_descriptor._fields_ = [
    ('numSublinkSpeedAttributes', uint8_t),
    ('numSublinkSpeedIDs', uint8_t),
    ('ssid', uint8_t),
    ('minRxLaneCount', uint8_t),
    ('minTxLaneCount', uint8_t),
    ('sublinkSpeedAttributes', POINTER(struct_libusb_ssplus_sublink_attribute)),
]

# /usr/include/libusb-1.0/libusb.h: 1087
class struct_libusb_container_id_descriptor(Structure):
    pass

struct_libusb_container_id_descriptor.__slots__ = [
    'bLength',
    'bDescriptorType',
    'bDevCapabilityType',
    'bReserved',
    'ContainerID',
]
struct_libusb_container_id_descriptor._fields_ = [
    ('bLength', uint8_t),
    ('bDescriptorType', uint8_t),
    ('bDevCapabilityType', uint8_t),
    ('bReserved', uint8_t),
    ('ContainerID', uint8_t * int(16)),
]

# /usr/include/libusb-1.0/libusb.h: 1112
class struct_libusb_platform_descriptor(Structure):
    pass

struct_libusb_platform_descriptor.__slots__ = [
    'bLength',
    'bDescriptorType',
    'bDevCapabilityType',
    'bReserved',
    'PlatformCapabilityUUID',
    'CapabilityData',
]
struct_libusb_platform_descriptor._fields_ = [
    ('bLength', uint8_t),
    ('bDescriptorType', uint8_t),
    ('bDevCapabilityType', uint8_t),
    ('bReserved', uint8_t),
    ('PlatformCapabilityUUID', uint8_t * int(16)),
    ('CapabilityData', POINTER(uint8_t)),
]

# /usr/include/libusb-1.0/libusb.h: 1141
class struct_libusb_control_setup(Structure):
    pass

struct_libusb_control_setup.__slots__ = [
    'bmRequestType',
    'bRequest',
    'wValue',
    'wIndex',
    'wLength',
]
struct_libusb_control_setup._fields_ = [
    ('bmRequestType', uint8_t),
    ('bRequest', uint8_t),
    ('wValue', uint16_t),
    ('wIndex', uint16_t),
    ('wLength', uint16_t),
]

# /usr/include/libusb-1.0/libusb.h: 1174
class struct_libusb_context(Structure):
    pass

# /usr/include/libusb-1.0/libusb.h: 1175
class struct_libusb_device(Structure):
    pass

# /usr/include/libusb-1.0/libusb.h: 1176
class struct_libusb_device_handle(Structure):
    pass

# /usr/include/libusb-1.0/libusb.h: 1181
class struct_libusb_version(Structure):
    pass

struct_libusb_version.__slots__ = [
    'major',
    'minor',
    'micro',
    'nano',
    'rc',
    'describe',
]
struct_libusb_version._fields_ = [
    ('major', uint16_t),
    ('minor', uint16_t),
    ('micro', uint16_t),
    ('nano', uint16_t),
    ('rc', String),
    ('describe', String),
]

libusb_context = struct_libusb_context# /usr/include/libusb-1.0/libusb.h: 1219

libusb_device = struct_libusb_device# /usr/include/libusb-1.0/libusb.h: 1236

libusb_device_handle = struct_libusb_device_handle# /usr/include/libusb-1.0/libusb.h: 1247

enum_libusb_speed = c_int# /usr/include/libusb-1.0/libusb.h: 1252

LIBUSB_SPEED_UNKNOWN = 0# /usr/include/libusb-1.0/libusb.h: 1252

LIBUSB_SPEED_LOW = 1# /usr/include/libusb-1.0/libusb.h: 1252

LIBUSB_SPEED_FULL = 2# /usr/include/libusb-1.0/libusb.h: 1252

LIBUSB_SPEED_HIGH = 3# /usr/include/libusb-1.0/libusb.h: 1252

LIBUSB_SPEED_SUPER = 4# /usr/include/libusb-1.0/libusb.h: 1252

LIBUSB_SPEED_SUPER_PLUS = 5# /usr/include/libusb-1.0/libusb.h: 1252

LIBUSB_SPEED_SUPER_PLUS_X2 = 6# /usr/include/libusb-1.0/libusb.h: 1252

enum_libusb_error = c_int# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_SUCCESS = 0# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_IO = (-1)# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_INVALID_PARAM = (-2)# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_ACCESS = (-3)# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_NO_DEVICE = (-4)# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_NOT_FOUND = (-5)# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_BUSY = (-6)# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_TIMEOUT = (-7)# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_OVERFLOW = (-8)# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_PIPE = (-9)# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_INTERRUPTED = (-10)# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_NO_MEM = (-11)# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_NOT_SUPPORTED = (-12)# /usr/include/libusb-1.0/libusb.h: 1282

LIBUSB_ERROR_OTHER = (-99)# /usr/include/libusb-1.0/libusb.h: 1282

enum_libusb_transfer_type = c_int# /usr/include/libusb-1.0/libusb.h: 1334

LIBUSB_TRANSFER_TYPE_CONTROL = 0# /usr/include/libusb-1.0/libusb.h: 1334

LIBUSB_TRANSFER_TYPE_ISOCHRONOUS = 1# /usr/include/libusb-1.0/libusb.h: 1334

LIBUSB_TRANSFER_TYPE_BULK = 2# /usr/include/libusb-1.0/libusb.h: 1334

LIBUSB_TRANSFER_TYPE_INTERRUPT = 3# /usr/include/libusb-1.0/libusb.h: 1334

LIBUSB_TRANSFER_TYPE_BULK_STREAM = 4# /usr/include/libusb-1.0/libusb.h: 1334

enum_libusb_transfer_status = c_int# /usr/include/libusb-1.0/libusb.h: 1353

LIBUSB_TRANSFER_COMPLETED = 0# /usr/include/libusb-1.0/libusb.h: 1353

LIBUSB_TRANSFER_ERROR = (LIBUSB_TRANSFER_COMPLETED + 1)# /usr/include/libusb-1.0/libusb.h: 1353

LIBUSB_TRANSFER_TIMED_OUT = (LIBUSB_TRANSFER_ERROR + 1)# /usr/include/libusb-1.0/libusb.h: 1353

LIBUSB_TRANSFER_CANCELLED = (LIBUSB_TRANSFER_TIMED_OUT + 1)# /usr/include/libusb-1.0/libusb.h: 1353

LIBUSB_TRANSFER_STALL = (LIBUSB_TRANSFER_CANCELLED + 1)# /usr/include/libusb-1.0/libusb.h: 1353

LIBUSB_TRANSFER_NO_DEVICE = (LIBUSB_TRANSFER_STALL + 1)# /usr/include/libusb-1.0/libusb.h: 1353

LIBUSB_TRANSFER_OVERFLOW = (LIBUSB_TRANSFER_NO_DEVICE + 1)# /usr/include/libusb-1.0/libusb.h: 1353

enum_libusb_transfer_flags = c_int# /usr/include/libusb-1.0/libusb.h: 1383

LIBUSB_TRANSFER_SHORT_NOT_OK = (1 << 0)# /usr/include/libusb-1.0/libusb.h: 1383

LIBUSB_TRANSFER_FREE_BUFFER = (1 << 1)# /usr/include/libusb-1.0/libusb.h: 1383

LIBUSB_TRANSFER_FREE_TRANSFER = (1 << 2)# /usr/include/libusb-1.0/libusb.h: 1383

LIBUSB_TRANSFER_ADD_ZERO_PACKET = (1 << 3)# /usr/include/libusb-1.0/libusb.h: 1383

# /usr/include/libusb-1.0/libusb.h: 1428
class struct_libusb_iso_packet_descriptor(Structure):
    pass

struct_libusb_iso_packet_descriptor.__slots__ = [
    'length',
    'actual_length',
    'status',
]
struct_libusb_iso_packet_descriptor._fields_ = [
    ('length', c_uint),
    ('actual_length', c_uint),
    ('status', enum_libusb_transfer_status),
]

# /usr/include/libusb-1.0/libusb.h: 1458
class struct_libusb_transfer(Structure):
    pass

libusb_transfer_cb_fn = CFUNCTYPE(UNCHECKED(None), POINTER(struct_libusb_transfer))# /usr/include/libusb-1.0/libusb.h: 1450

struct_libusb_transfer.__slots__ = [
    'dev_handle',
    'flags',
    'endpoint',
    'type',
    'timeout',
    'status',
    'length',
    'actual_length',
    'callback',
    'user_data',
    'buffer',
    'num_iso_packets',
    'iso_packet_desc',
]
struct_libusb_transfer._fields_ = [
    ('dev_handle', POINTER(libusb_device_handle)),
    ('flags', uint8_t),
    ('endpoint', c_ubyte),
    ('type', c_ubyte),
    ('timeout', c_uint),
    ('status', enum_libusb_transfer_status),
    ('length', c_int),
    ('actual_length', c_int),
    ('callback', libusb_transfer_cb_fn),
    ('user_data', POINTER(None)),
    ('buffer', POINTER(c_ubyte)),
    ('num_iso_packets', c_int),
    ('iso_packet_desc', POINTER(struct_libusb_iso_packet_descriptor)),
]

enum_libusb_capability = c_int# /usr/include/libusb-1.0/libusb.h: 1524

LIBUSB_CAP_HAS_CAPABILITY = 0x0000# /usr/include/libusb-1.0/libusb.h: 1524

LIBUSB_CAP_HAS_HOTPLUG = 0x0001# /usr/include/libusb-1.0/libusb.h: 1524

LIBUSB_CAP_HAS_HID_ACCESS = 0x0100# /usr/include/libusb-1.0/libusb.h: 1524

LIBUSB_CAP_SUPPORTS_DETACH_KERNEL_DRIVER = 0x0101# /usr/include/libusb-1.0/libusb.h: 1524

enum_libusb_log_level = c_int# /usr/include/libusb-1.0/libusb.h: 1545

LIBUSB_LOG_LEVEL_NONE = 0# /usr/include/libusb-1.0/libusb.h: 1545

LIBUSB_LOG_LEVEL_ERROR = 1# /usr/include/libusb-1.0/libusb.h: 1545

LIBUSB_LOG_LEVEL_WARNING = 2# /usr/include/libusb-1.0/libusb.h: 1545

LIBUSB_LOG_LEVEL_INFO = 3# /usr/include/libusb-1.0/libusb.h: 1545

LIBUSB_LOG_LEVEL_DEBUG = 4# /usr/include/libusb-1.0/libusb.h: 1545

enum_libusb_log_cb_mode = c_int# /usr/include/libusb-1.0/libusb.h: 1569

LIBUSB_LOG_CB_GLOBAL = (1 << 0)# /usr/include/libusb-1.0/libusb.h: 1569

LIBUSB_LOG_CB_CONTEXT = (1 << 1)# /usr/include/libusb-1.0/libusb.h: 1569

enum_libusb_option = c_int# /usr/include/libusb-1.0/libusb.h: 1580

LIBUSB_OPTION_LOG_LEVEL = 0# /usr/include/libusb-1.0/libusb.h: 1580

LIBUSB_OPTION_USE_USBDK = 1# /usr/include/libusb-1.0/libusb.h: 1580

LIBUSB_OPTION_NO_DEVICE_DISCOVERY = 2# /usr/include/libusb-1.0/libusb.h: 1580

LIBUSB_OPTION_LOG_CB = 3# /usr/include/libusb-1.0/libusb.h: 1580

LIBUSB_OPTION_MAX = 4# /usr/include/libusb-1.0/libusb.h: 1580

libusb_log_cb = CFUNCTYPE(UNCHECKED(None), POINTER(libusb_context), enum_libusb_log_level, String)# /usr/include/libusb-1.0/libusb.h: 1661

# /usr/include/libusb-1.0/libusb.h: 1672
class union_anon_16(Union):
    pass

union_anon_16.__slots__ = [
    'ival',
    'log_cbval',
]
union_anon_16._fields_ = [
    ('ival', c_int),
    ('log_cbval', libusb_log_cb),
]

# /usr/include/libusb-1.0/libusb.h: 1668
class struct_libusb_init_option(Structure):
    pass

struct_libusb_init_option.__slots__ = [
    'option',
    'value',
]
struct_libusb_init_option._fields_ = [
    ('option', enum_libusb_option),
    ('value', union_anon_16),
]

# /usr/include/libusb-1.0/libusb.h: 1678
if _libs["usb-1.0"].has("libusb_init", "cdecl"):
    libusb_init = _libs["usb-1.0"].get("libusb_init", "cdecl")
    libusb_init.argtypes = [POINTER(POINTER(libusb_context))]
    libusb_init.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1679
if _libs["usb-1.0"].has("libusb_init_context", "cdecl"):
    libusb_init_context = _libs["usb-1.0"].get("libusb_init_context", "cdecl")
    libusb_init_context.argtypes = [POINTER(POINTER(libusb_context)), POINTER(struct_libusb_init_option), c_int]
    libusb_init_context.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1680
if _libs["usb-1.0"].has("libusb_exit", "cdecl"):
    libusb_exit = _libs["usb-1.0"].get("libusb_exit", "cdecl")
    libusb_exit.argtypes = [POINTER(libusb_context)]
    libusb_exit.restype = None

# /usr/include/libusb-1.0/libusb.h: 1681
if _libs["usb-1.0"].has("libusb_set_debug", "cdecl"):
    libusb_set_debug = _libs["usb-1.0"].get("libusb_set_debug", "cdecl")
    libusb_set_debug.argtypes = [POINTER(libusb_context), c_int]
    libusb_set_debug.restype = None

# /usr/include/libusb-1.0/libusb.h: 1683
if _libs["usb-1.0"].has("libusb_set_log_cb", "cdecl"):
    libusb_set_log_cb = _libs["usb-1.0"].get("libusb_set_log_cb", "cdecl")
    libusb_set_log_cb.argtypes = [POINTER(libusb_context), libusb_log_cb, c_int]
    libusb_set_log_cb.restype = None

# /usr/include/libusb-1.0/libusb.h: 1684
if _libs["usb-1.0"].has("libusb_get_version", "cdecl"):
    libusb_get_version = _libs["usb-1.0"].get("libusb_get_version", "cdecl")
    libusb_get_version.argtypes = []
    libusb_get_version.restype = POINTER(struct_libusb_version)

# /usr/include/libusb-1.0/libusb.h: 1685
if _libs["usb-1.0"].has("libusb_has_capability", "cdecl"):
    libusb_has_capability = _libs["usb-1.0"].get("libusb_has_capability", "cdecl")
    libusb_has_capability.argtypes = [uint32_t]
    libusb_has_capability.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1686
if _libs["usb-1.0"].has("libusb_error_name", "cdecl"):
    libusb_error_name = _libs["usb-1.0"].get("libusb_error_name", "cdecl")
    libusb_error_name.argtypes = [c_int]
    libusb_error_name.restype = c_char_p

# /usr/include/libusb-1.0/libusb.h: 1687
if _libs["usb-1.0"].has("libusb_setlocale", "cdecl"):
    libusb_setlocale = _libs["usb-1.0"].get("libusb_setlocale", "cdecl")
    libusb_setlocale.argtypes = [String]
    libusb_setlocale.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1688
if _libs["usb-1.0"].has("libusb_strerror", "cdecl"):
    libusb_strerror = _libs["usb-1.0"].get("libusb_strerror", "cdecl")
    libusb_strerror.argtypes = [c_int]
    libusb_strerror.restype = c_char_p

# /usr/include/libusb-1.0/libusb.h: 1690
if _libs["usb-1.0"].has("libusb_get_device_list", "cdecl"):
    libusb_get_device_list = _libs["usb-1.0"].get("libusb_get_device_list", "cdecl")
    libusb_get_device_list.argtypes = [POINTER(libusb_context), POINTER(POINTER(POINTER(libusb_device)))]
    libusb_get_device_list.restype = c_ptrdiff_t

# /usr/include/libusb-1.0/libusb.h: 1692
if _libs["usb-1.0"].has("libusb_free_device_list", "cdecl"):
    libusb_free_device_list = _libs["usb-1.0"].get("libusb_free_device_list", "cdecl")
    libusb_free_device_list.argtypes = [POINTER(POINTER(libusb_device)), c_int]
    libusb_free_device_list.restype = None

# /usr/include/libusb-1.0/libusb.h: 1694
if _libs["usb-1.0"].has("libusb_ref_device", "cdecl"):
    libusb_ref_device = _libs["usb-1.0"].get("libusb_ref_device", "cdecl")
    libusb_ref_device.argtypes = [POINTER(libusb_device)]
    libusb_ref_device.restype = POINTER(libusb_device)

# /usr/include/libusb-1.0/libusb.h: 1695
if _libs["usb-1.0"].has("libusb_unref_device", "cdecl"):
    libusb_unref_device = _libs["usb-1.0"].get("libusb_unref_device", "cdecl")
    libusb_unref_device.argtypes = [POINTER(libusb_device)]
    libusb_unref_device.restype = None

# /usr/include/libusb-1.0/libusb.h: 1697
if _libs["usb-1.0"].has("libusb_get_configuration", "cdecl"):
    libusb_get_configuration = _libs["usb-1.0"].get("libusb_get_configuration", "cdecl")
    libusb_get_configuration.argtypes = [POINTER(libusb_device_handle), POINTER(c_int)]
    libusb_get_configuration.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1699
if _libs["usb-1.0"].has("libusb_get_device_descriptor", "cdecl"):
    libusb_get_device_descriptor = _libs["usb-1.0"].get("libusb_get_device_descriptor", "cdecl")
    libusb_get_device_descriptor.argtypes = [POINTER(libusb_device), POINTER(struct_libusb_device_descriptor)]
    libusb_get_device_descriptor.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1701
if _libs["usb-1.0"].has("libusb_get_active_config_descriptor", "cdecl"):
    libusb_get_active_config_descriptor = _libs["usb-1.0"].get("libusb_get_active_config_descriptor", "cdecl")
    libusb_get_active_config_descriptor.argtypes = [POINTER(libusb_device), POINTER(POINTER(struct_libusb_config_descriptor))]
    libusb_get_active_config_descriptor.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1703
if _libs["usb-1.0"].has("libusb_get_config_descriptor", "cdecl"):
    libusb_get_config_descriptor = _libs["usb-1.0"].get("libusb_get_config_descriptor", "cdecl")
    libusb_get_config_descriptor.argtypes = [POINTER(libusb_device), uint8_t, POINTER(POINTER(struct_libusb_config_descriptor))]
    libusb_get_config_descriptor.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1705
if _libs["usb-1.0"].has("libusb_get_config_descriptor_by_value", "cdecl"):
    libusb_get_config_descriptor_by_value = _libs["usb-1.0"].get("libusb_get_config_descriptor_by_value", "cdecl")
    libusb_get_config_descriptor_by_value.argtypes = [POINTER(libusb_device), uint8_t, POINTER(POINTER(struct_libusb_config_descriptor))]
    libusb_get_config_descriptor_by_value.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1707
if _libs["usb-1.0"].has("libusb_free_config_descriptor", "cdecl"):
    libusb_free_config_descriptor = _libs["usb-1.0"].get("libusb_free_config_descriptor", "cdecl")
    libusb_free_config_descriptor.argtypes = [POINTER(struct_libusb_config_descriptor)]
    libusb_free_config_descriptor.restype = None

# /usr/include/libusb-1.0/libusb.h: 1709
if _libs["usb-1.0"].has("libusb_get_ss_endpoint_companion_descriptor", "cdecl"):
    libusb_get_ss_endpoint_companion_descriptor = _libs["usb-1.0"].get("libusb_get_ss_endpoint_companion_descriptor", "cdecl")
    libusb_get_ss_endpoint_companion_descriptor.argtypes = [POINTER(libusb_context), POINTER(struct_libusb_endpoint_descriptor), POINTER(POINTER(struct_libusb_ss_endpoint_companion_descriptor))]
    libusb_get_ss_endpoint_companion_descriptor.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1713
if _libs["usb-1.0"].has("libusb_free_ss_endpoint_companion_descriptor", "cdecl"):
    libusb_free_ss_endpoint_companion_descriptor = _libs["usb-1.0"].get("libusb_free_ss_endpoint_companion_descriptor", "cdecl")
    libusb_free_ss_endpoint_companion_descriptor.argtypes = [POINTER(struct_libusb_ss_endpoint_companion_descriptor)]
    libusb_free_ss_endpoint_companion_descriptor.restype = None

# /usr/include/libusb-1.0/libusb.h: 1715
if _libs["usb-1.0"].has("libusb_get_bos_descriptor", "cdecl"):
    libusb_get_bos_descriptor = _libs["usb-1.0"].get("libusb_get_bos_descriptor", "cdecl")
    libusb_get_bos_descriptor.argtypes = [POINTER(libusb_device_handle), POINTER(POINTER(struct_libusb_bos_descriptor))]
    libusb_get_bos_descriptor.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1717
if _libs["usb-1.0"].has("libusb_free_bos_descriptor", "cdecl"):
    libusb_free_bos_descriptor = _libs["usb-1.0"].get("libusb_free_bos_descriptor", "cdecl")
    libusb_free_bos_descriptor.argtypes = [POINTER(struct_libusb_bos_descriptor)]
    libusb_free_bos_descriptor.restype = None

# /usr/include/libusb-1.0/libusb.h: 1718
if _libs["usb-1.0"].has("libusb_get_usb_2_0_extension_descriptor", "cdecl"):
    libusb_get_usb_2_0_extension_descriptor = _libs["usb-1.0"].get("libusb_get_usb_2_0_extension_descriptor", "cdecl")
    libusb_get_usb_2_0_extension_descriptor.argtypes = [POINTER(libusb_context), POINTER(struct_libusb_bos_dev_capability_descriptor), POINTER(POINTER(struct_libusb_usb_2_0_extension_descriptor))]
    libusb_get_usb_2_0_extension_descriptor.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1722
if _libs["usb-1.0"].has("libusb_free_usb_2_0_extension_descriptor", "cdecl"):
    libusb_free_usb_2_0_extension_descriptor = _libs["usb-1.0"].get("libusb_free_usb_2_0_extension_descriptor", "cdecl")
    libusb_free_usb_2_0_extension_descriptor.argtypes = [POINTER(struct_libusb_usb_2_0_extension_descriptor)]
    libusb_free_usb_2_0_extension_descriptor.restype = None

# /usr/include/libusb-1.0/libusb.h: 1724
if _libs["usb-1.0"].has("libusb_get_ss_usb_device_capability_descriptor", "cdecl"):
    libusb_get_ss_usb_device_capability_descriptor = _libs["usb-1.0"].get("libusb_get_ss_usb_device_capability_descriptor", "cdecl")
    libusb_get_ss_usb_device_capability_descriptor.argtypes = [POINTER(libusb_context), POINTER(struct_libusb_bos_dev_capability_descriptor), POINTER(POINTER(struct_libusb_ss_usb_device_capability_descriptor))]
    libusb_get_ss_usb_device_capability_descriptor.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1728
if _libs["usb-1.0"].has("libusb_free_ss_usb_device_capability_descriptor", "cdecl"):
    libusb_free_ss_usb_device_capability_descriptor = _libs["usb-1.0"].get("libusb_free_ss_usb_device_capability_descriptor", "cdecl")
    libusb_free_ss_usb_device_capability_descriptor.argtypes = [POINTER(struct_libusb_ss_usb_device_capability_descriptor)]
    libusb_free_ss_usb_device_capability_descriptor.restype = None

# /usr/include/libusb-1.0/libusb.h: 1730
if _libs["usb-1.0"].has("libusb_get_ssplus_usb_device_capability_descriptor", "cdecl"):
    libusb_get_ssplus_usb_device_capability_descriptor = _libs["usb-1.0"].get("libusb_get_ssplus_usb_device_capability_descriptor", "cdecl")
    libusb_get_ssplus_usb_device_capability_descriptor.argtypes = [POINTER(libusb_context), POINTER(struct_libusb_bos_dev_capability_descriptor), POINTER(POINTER(struct_libusb_ssplus_usb_device_capability_descriptor))]
    libusb_get_ssplus_usb_device_capability_descriptor.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1734
if _libs["usb-1.0"].has("libusb_free_ssplus_usb_device_capability_descriptor", "cdecl"):
    libusb_free_ssplus_usb_device_capability_descriptor = _libs["usb-1.0"].get("libusb_free_ssplus_usb_device_capability_descriptor", "cdecl")
    libusb_free_ssplus_usb_device_capability_descriptor.argtypes = [POINTER(struct_libusb_ssplus_usb_device_capability_descriptor)]
    libusb_free_ssplus_usb_device_capability_descriptor.restype = None

# /usr/include/libusb-1.0/libusb.h: 1736
if _libs["usb-1.0"].has("libusb_get_container_id_descriptor", "cdecl"):
    libusb_get_container_id_descriptor = _libs["usb-1.0"].get("libusb_get_container_id_descriptor", "cdecl")
    libusb_get_container_id_descriptor.argtypes = [POINTER(libusb_context), POINTER(struct_libusb_bos_dev_capability_descriptor), POINTER(POINTER(struct_libusb_container_id_descriptor))]
    libusb_get_container_id_descriptor.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1739
if _libs["usb-1.0"].has("libusb_free_container_id_descriptor", "cdecl"):
    libusb_free_container_id_descriptor = _libs["usb-1.0"].get("libusb_free_container_id_descriptor", "cdecl")
    libusb_free_container_id_descriptor.argtypes = [POINTER(struct_libusb_container_id_descriptor)]
    libusb_free_container_id_descriptor.restype = None

# /usr/include/libusb-1.0/libusb.h: 1741
if _libs["usb-1.0"].has("libusb_get_platform_descriptor", "cdecl"):
    libusb_get_platform_descriptor = _libs["usb-1.0"].get("libusb_get_platform_descriptor", "cdecl")
    libusb_get_platform_descriptor.argtypes = [POINTER(libusb_context), POINTER(struct_libusb_bos_dev_capability_descriptor), POINTER(POINTER(struct_libusb_platform_descriptor))]
    libusb_get_platform_descriptor.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1744
if _libs["usb-1.0"].has("libusb_free_platform_descriptor", "cdecl"):
    libusb_free_platform_descriptor = _libs["usb-1.0"].get("libusb_free_platform_descriptor", "cdecl")
    libusb_free_platform_descriptor.argtypes = [POINTER(struct_libusb_platform_descriptor)]
    libusb_free_platform_descriptor.restype = None

# /usr/include/libusb-1.0/libusb.h: 1746
if _libs["usb-1.0"].has("libusb_get_bus_number", "cdecl"):
    libusb_get_bus_number = _libs["usb-1.0"].get("libusb_get_bus_number", "cdecl")
    libusb_get_bus_number.argtypes = [POINTER(libusb_device)]
    libusb_get_bus_number.restype = uint8_t

# /usr/include/libusb-1.0/libusb.h: 1747
if _libs["usb-1.0"].has("libusb_get_port_number", "cdecl"):
    libusb_get_port_number = _libs["usb-1.0"].get("libusb_get_port_number", "cdecl")
    libusb_get_port_number.argtypes = [POINTER(libusb_device)]
    libusb_get_port_number.restype = uint8_t

# /usr/include/libusb-1.0/libusb.h: 1748
if _libs["usb-1.0"].has("libusb_get_port_numbers", "cdecl"):
    libusb_get_port_numbers = _libs["usb-1.0"].get("libusb_get_port_numbers", "cdecl")
    libusb_get_port_numbers.argtypes = [POINTER(libusb_device), POINTER(uint8_t), c_int]
    libusb_get_port_numbers.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1750
if _libs["usb-1.0"].has("libusb_get_port_path", "cdecl"):
    libusb_get_port_path = _libs["usb-1.0"].get("libusb_get_port_path", "cdecl")
    libusb_get_port_path.argtypes = [POINTER(libusb_context), POINTER(libusb_device), POINTER(uint8_t), uint8_t]
    libusb_get_port_path.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1751
if _libs["usb-1.0"].has("libusb_get_parent", "cdecl"):
    libusb_get_parent = _libs["usb-1.0"].get("libusb_get_parent", "cdecl")
    libusb_get_parent.argtypes = [POINTER(libusb_device)]
    libusb_get_parent.restype = POINTER(libusb_device)

# /usr/include/libusb-1.0/libusb.h: 1752
if _libs["usb-1.0"].has("libusb_get_device_address", "cdecl"):
    libusb_get_device_address = _libs["usb-1.0"].get("libusb_get_device_address", "cdecl")
    libusb_get_device_address.argtypes = [POINTER(libusb_device)]
    libusb_get_device_address.restype = uint8_t

# /usr/include/libusb-1.0/libusb.h: 1753
if _libs["usb-1.0"].has("libusb_get_device_speed", "cdecl"):
    libusb_get_device_speed = _libs["usb-1.0"].get("libusb_get_device_speed", "cdecl")
    libusb_get_device_speed.argtypes = [POINTER(libusb_device)]
    libusb_get_device_speed.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1754
if _libs["usb-1.0"].has("libusb_get_max_packet_size", "cdecl"):
    libusb_get_max_packet_size = _libs["usb-1.0"].get("libusb_get_max_packet_size", "cdecl")
    libusb_get_max_packet_size.argtypes = [POINTER(libusb_device), c_ubyte]
    libusb_get_max_packet_size.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1756
if _libs["usb-1.0"].has("libusb_get_max_iso_packet_size", "cdecl"):
    libusb_get_max_iso_packet_size = _libs["usb-1.0"].get("libusb_get_max_iso_packet_size", "cdecl")
    libusb_get_max_iso_packet_size.argtypes = [POINTER(libusb_device), c_ubyte]
    libusb_get_max_iso_packet_size.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1758
if _libs["usb-1.0"].has("libusb_get_max_alt_packet_size", "cdecl"):
    libusb_get_max_alt_packet_size = _libs["usb-1.0"].get("libusb_get_max_alt_packet_size", "cdecl")
    libusb_get_max_alt_packet_size.argtypes = [POINTER(libusb_device), c_int, c_int, c_ubyte]
    libusb_get_max_alt_packet_size.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1761
if _libs["usb-1.0"].has("libusb_get_interface_association_descriptors", "cdecl"):
    libusb_get_interface_association_descriptors = _libs["usb-1.0"].get("libusb_get_interface_association_descriptors", "cdecl")
    libusb_get_interface_association_descriptors.argtypes = [POINTER(libusb_device), uint8_t, POINTER(POINTER(struct_libusb_interface_association_descriptor_array))]
    libusb_get_interface_association_descriptors.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1763
if _libs["usb-1.0"].has("libusb_get_active_interface_association_descriptors", "cdecl"):
    libusb_get_active_interface_association_descriptors = _libs["usb-1.0"].get("libusb_get_active_interface_association_descriptors", "cdecl")
    libusb_get_active_interface_association_descriptors.argtypes = [POINTER(libusb_device), POINTER(POINTER(struct_libusb_interface_association_descriptor_array))]
    libusb_get_active_interface_association_descriptors.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1765
if _libs["usb-1.0"].has("libusb_free_interface_association_descriptors", "cdecl"):
    libusb_free_interface_association_descriptors = _libs["usb-1.0"].get("libusb_free_interface_association_descriptors", "cdecl")
    libusb_free_interface_association_descriptors.argtypes = [POINTER(struct_libusb_interface_association_descriptor_array)]
    libusb_free_interface_association_descriptors.restype = None

# /usr/include/libusb-1.0/libusb.h: 1768
if _libs["usb-1.0"].has("libusb_wrap_sys_device", "cdecl"):
    libusb_wrap_sys_device = _libs["usb-1.0"].get("libusb_wrap_sys_device", "cdecl")
    libusb_wrap_sys_device.argtypes = [POINTER(libusb_context), intptr_t, POINTER(POINTER(libusb_device_handle))]
    libusb_wrap_sys_device.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1769
if _libs["usb-1.0"].has("libusb_open", "cdecl"):
    libusb_open = _libs["usb-1.0"].get("libusb_open", "cdecl")
    libusb_open.argtypes = [POINTER(libusb_device), POINTER(POINTER(libusb_device_handle))]
    libusb_open.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1770
if _libs["usb-1.0"].has("libusb_close", "cdecl"):
    libusb_close = _libs["usb-1.0"].get("libusb_close", "cdecl")
    libusb_close.argtypes = [POINTER(libusb_device_handle)]
    libusb_close.restype = None

# /usr/include/libusb-1.0/libusb.h: 1771
if _libs["usb-1.0"].has("libusb_get_device", "cdecl"):
    libusb_get_device = _libs["usb-1.0"].get("libusb_get_device", "cdecl")
    libusb_get_device.argtypes = [POINTER(libusb_device_handle)]
    libusb_get_device.restype = POINTER(libusb_device)

# /usr/include/libusb-1.0/libusb.h: 1773
if _libs["usb-1.0"].has("libusb_set_configuration", "cdecl"):
    libusb_set_configuration = _libs["usb-1.0"].get("libusb_set_configuration", "cdecl")
    libusb_set_configuration.argtypes = [POINTER(libusb_device_handle), c_int]
    libusb_set_configuration.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1775
if _libs["usb-1.0"].has("libusb_claim_interface", "cdecl"):
    libusb_claim_interface = _libs["usb-1.0"].get("libusb_claim_interface", "cdecl")
    libusb_claim_interface.argtypes = [POINTER(libusb_device_handle), c_int]
    libusb_claim_interface.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1777
if _libs["usb-1.0"].has("libusb_release_interface", "cdecl"):
    libusb_release_interface = _libs["usb-1.0"].get("libusb_release_interface", "cdecl")
    libusb_release_interface.argtypes = [POINTER(libusb_device_handle), c_int]
    libusb_release_interface.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1780
if _libs["usb-1.0"].has("libusb_open_device_with_vid_pid", "cdecl"):
    libusb_open_device_with_vid_pid = _libs["usb-1.0"].get("libusb_open_device_with_vid_pid", "cdecl")
    libusb_open_device_with_vid_pid.argtypes = [POINTER(libusb_context), uint16_t, uint16_t]
    libusb_open_device_with_vid_pid.restype = POINTER(libusb_device_handle)

# /usr/include/libusb-1.0/libusb.h: 1783
if _libs["usb-1.0"].has("libusb_set_interface_alt_setting", "cdecl"):
    libusb_set_interface_alt_setting = _libs["usb-1.0"].get("libusb_set_interface_alt_setting", "cdecl")
    libusb_set_interface_alt_setting.argtypes = [POINTER(libusb_device_handle), c_int, c_int]
    libusb_set_interface_alt_setting.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1785
if _libs["usb-1.0"].has("libusb_clear_halt", "cdecl"):
    libusb_clear_halt = _libs["usb-1.0"].get("libusb_clear_halt", "cdecl")
    libusb_clear_halt.argtypes = [POINTER(libusb_device_handle), c_ubyte]
    libusb_clear_halt.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1787
if _libs["usb-1.0"].has("libusb_reset_device", "cdecl"):
    libusb_reset_device = _libs["usb-1.0"].get("libusb_reset_device", "cdecl")
    libusb_reset_device.argtypes = [POINTER(libusb_device_handle)]
    libusb_reset_device.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1789
if _libs["usb-1.0"].has("libusb_alloc_streams", "cdecl"):
    libusb_alloc_streams = _libs["usb-1.0"].get("libusb_alloc_streams", "cdecl")
    libusb_alloc_streams.argtypes = [POINTER(libusb_device_handle), uint32_t, POINTER(c_ubyte), c_int]
    libusb_alloc_streams.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1791
if _libs["usb-1.0"].has("libusb_free_streams", "cdecl"):
    libusb_free_streams = _libs["usb-1.0"].get("libusb_free_streams", "cdecl")
    libusb_free_streams.argtypes = [POINTER(libusb_device_handle), POINTER(c_ubyte), c_int]
    libusb_free_streams.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1794
if _libs["usb-1.0"].has("libusb_dev_mem_alloc", "cdecl"):
    libusb_dev_mem_alloc = _libs["usb-1.0"].get("libusb_dev_mem_alloc", "cdecl")
    libusb_dev_mem_alloc.argtypes = [POINTER(libusb_device_handle), c_size_t]
    libusb_dev_mem_alloc.restype = POINTER(c_ubyte)

# /usr/include/libusb-1.0/libusb.h: 1796
if _libs["usb-1.0"].has("libusb_dev_mem_free", "cdecl"):
    libusb_dev_mem_free = _libs["usb-1.0"].get("libusb_dev_mem_free", "cdecl")
    libusb_dev_mem_free.argtypes = [POINTER(libusb_device_handle), POINTER(c_ubyte), c_size_t]
    libusb_dev_mem_free.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1799
if _libs["usb-1.0"].has("libusb_kernel_driver_active", "cdecl"):
    libusb_kernel_driver_active = _libs["usb-1.0"].get("libusb_kernel_driver_active", "cdecl")
    libusb_kernel_driver_active.argtypes = [POINTER(libusb_device_handle), c_int]
    libusb_kernel_driver_active.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1801
if _libs["usb-1.0"].has("libusb_detach_kernel_driver", "cdecl"):
    libusb_detach_kernel_driver = _libs["usb-1.0"].get("libusb_detach_kernel_driver", "cdecl")
    libusb_detach_kernel_driver.argtypes = [POINTER(libusb_device_handle), c_int]
    libusb_detach_kernel_driver.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1803
if _libs["usb-1.0"].has("libusb_attach_kernel_driver", "cdecl"):
    libusb_attach_kernel_driver = _libs["usb-1.0"].get("libusb_attach_kernel_driver", "cdecl")
    libusb_attach_kernel_driver.argtypes = [POINTER(libusb_device_handle), c_int]
    libusb_attach_kernel_driver.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1805
if _libs["usb-1.0"].has("libusb_set_auto_detach_kernel_driver", "cdecl"):
    libusb_set_auto_detach_kernel_driver = _libs["usb-1.0"].get("libusb_set_auto_detach_kernel_driver", "cdecl")
    libusb_set_auto_detach_kernel_driver.argtypes = [POINTER(libusb_device_handle), c_int]
    libusb_set_auto_detach_kernel_driver.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1873
for _lib in _libs.values():
    try:
        setup = (POINTER(struct_libusb_control_setup)).in_dll(_lib, "setup")
        break
    except:
        pass

# /usr/include/libusb-1.0/libusb.h: 1881
if _libs["usb-1.0"].has("libusb_alloc_transfer", "cdecl"):
    libusb_alloc_transfer = _libs["usb-1.0"].get("libusb_alloc_transfer", "cdecl")
    libusb_alloc_transfer.argtypes = [c_int]
    libusb_alloc_transfer.restype = POINTER(struct_libusb_transfer)

# /usr/include/libusb-1.0/libusb.h: 1882
if _libs["usb-1.0"].has("libusb_submit_transfer", "cdecl"):
    libusb_submit_transfer = _libs["usb-1.0"].get("libusb_submit_transfer", "cdecl")
    libusb_submit_transfer.argtypes = [POINTER(struct_libusb_transfer)]
    libusb_submit_transfer.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1883
if _libs["usb-1.0"].has("libusb_cancel_transfer", "cdecl"):
    libusb_cancel_transfer = _libs["usb-1.0"].get("libusb_cancel_transfer", "cdecl")
    libusb_cancel_transfer.argtypes = [POINTER(struct_libusb_transfer)]
    libusb_cancel_transfer.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 1884
if _libs["usb-1.0"].has("libusb_free_transfer", "cdecl"):
    libusb_free_transfer = _libs["usb-1.0"].get("libusb_free_transfer", "cdecl")
    libusb_free_transfer.argtypes = [POINTER(struct_libusb_transfer)]
    libusb_free_transfer.restype = None

# /usr/include/libusb-1.0/libusb.h: 1885
if _libs["usb-1.0"].has("libusb_transfer_set_stream_id", "cdecl"):
    libusb_transfer_set_stream_id = _libs["usb-1.0"].get("libusb_transfer_set_stream_id", "cdecl")
    libusb_transfer_set_stream_id.argtypes = [POINTER(struct_libusb_transfer), uint32_t]
    libusb_transfer_set_stream_id.restype = None

# /usr/include/libusb-1.0/libusb.h: 1887
if _libs["usb-1.0"].has("libusb_transfer_get_stream_id", "cdecl"):
    libusb_transfer_get_stream_id = _libs["usb-1.0"].get("libusb_transfer_get_stream_id", "cdecl")
    libusb_transfer_get_stream_id.argtypes = [POINTER(struct_libusb_transfer)]
    libusb_transfer_get_stream_id.restype = uint32_t

# /usr/include/libusb-1.0/libusb.h: 1923
for _lib in _libs.values():
    try:
        setup = (POINTER(struct_libusb_control_setup)).in_dll(_lib, "setup")
        break
    except:
        pass

# /usr/include/libusb-1.0/libusb.h: 2061
for _lib in _libs.values():
    try:
        i = (c_int).in_dll(_lib, "i")
        break
    except:
        pass

# /usr/include/libusb-1.0/libusb.h: 2086
for _lib in _libs.values():
    try:
        i = (c_int).in_dll(_lib, "i")
        break
    except:
        pass

# /usr/include/libusb-1.0/libusb.h: 2087
for _lib in _libs.values():
    try:
        offset = (c_size_t).in_dll(_lib, "offset")
        break
    except:
        pass

# /usr/include/libusb-1.0/libusb.h: 2088
for _lib in _libs.values():
    try:
        _packet = (c_int).in_dll(_lib, "_packet")
        break
    except:
        pass

# /usr/include/libusb-1.0/libusb.h: 2128
for _lib in _libs.values():
    try:
        _packet = (c_int).in_dll(_lib, "_packet")
        break
    except:
        pass

# /usr/include/libusb-1.0/libusb.h: 2145
if _libs["usb-1.0"].has("libusb_control_transfer", "cdecl"):
    libusb_control_transfer = _libs["usb-1.0"].get("libusb_control_transfer", "cdecl")
    libusb_control_transfer.argtypes = [POINTER(libusb_device_handle), uint8_t, uint8_t, uint16_t, uint16_t, POINTER(c_ubyte), uint16_t, c_uint]
    libusb_control_transfer.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2149
if _libs["usb-1.0"].has("libusb_bulk_transfer", "cdecl"):
    libusb_bulk_transfer = _libs["usb-1.0"].get("libusb_bulk_transfer", "cdecl")
    libusb_bulk_transfer.argtypes = [POINTER(libusb_device_handle), c_ubyte, POINTER(c_ubyte), c_int, POINTER(c_int), c_uint]
    libusb_bulk_transfer.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2153
if _libs["usb-1.0"].has("libusb_interrupt_transfer", "cdecl"):
    libusb_interrupt_transfer = _libs["usb-1.0"].get("libusb_interrupt_transfer", "cdecl")
    libusb_interrupt_transfer.argtypes = [POINTER(libusb_device_handle), c_ubyte, POINTER(c_ubyte), c_int, POINTER(c_int), c_uint]
    libusb_interrupt_transfer.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2199
if _libs["usb-1.0"].has("libusb_get_string_descriptor_ascii", "cdecl"):
    libusb_get_string_descriptor_ascii = _libs["usb-1.0"].get("libusb_get_string_descriptor_ascii", "cdecl")
    libusb_get_string_descriptor_ascii.argtypes = [POINTER(libusb_device_handle), uint8_t, POINTER(c_ubyte), c_int]
    libusb_get_string_descriptor_ascii.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2204
if _libs["usb-1.0"].has("libusb_try_lock_events", "cdecl"):
    libusb_try_lock_events = _libs["usb-1.0"].get("libusb_try_lock_events", "cdecl")
    libusb_try_lock_events.argtypes = [POINTER(libusb_context)]
    libusb_try_lock_events.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2205
if _libs["usb-1.0"].has("libusb_lock_events", "cdecl"):
    libusb_lock_events = _libs["usb-1.0"].get("libusb_lock_events", "cdecl")
    libusb_lock_events.argtypes = [POINTER(libusb_context)]
    libusb_lock_events.restype = None

# /usr/include/libusb-1.0/libusb.h: 2206
if _libs["usb-1.0"].has("libusb_unlock_events", "cdecl"):
    libusb_unlock_events = _libs["usb-1.0"].get("libusb_unlock_events", "cdecl")
    libusb_unlock_events.argtypes = [POINTER(libusb_context)]
    libusb_unlock_events.restype = None

# /usr/include/libusb-1.0/libusb.h: 2207
if _libs["usb-1.0"].has("libusb_event_handling_ok", "cdecl"):
    libusb_event_handling_ok = _libs["usb-1.0"].get("libusb_event_handling_ok", "cdecl")
    libusb_event_handling_ok.argtypes = [POINTER(libusb_context)]
    libusb_event_handling_ok.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2208
if _libs["usb-1.0"].has("libusb_event_handler_active", "cdecl"):
    libusb_event_handler_active = _libs["usb-1.0"].get("libusb_event_handler_active", "cdecl")
    libusb_event_handler_active.argtypes = [POINTER(libusb_context)]
    libusb_event_handler_active.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2209
if _libs["usb-1.0"].has("libusb_interrupt_event_handler", "cdecl"):
    libusb_interrupt_event_handler = _libs["usb-1.0"].get("libusb_interrupt_event_handler", "cdecl")
    libusb_interrupt_event_handler.argtypes = [POINTER(libusb_context)]
    libusb_interrupt_event_handler.restype = None

# /usr/include/libusb-1.0/libusb.h: 2210
if _libs["usb-1.0"].has("libusb_lock_event_waiters", "cdecl"):
    libusb_lock_event_waiters = _libs["usb-1.0"].get("libusb_lock_event_waiters", "cdecl")
    libusb_lock_event_waiters.argtypes = [POINTER(libusb_context)]
    libusb_lock_event_waiters.restype = None

# /usr/include/libusb-1.0/libusb.h: 2211
if _libs["usb-1.0"].has("libusb_unlock_event_waiters", "cdecl"):
    libusb_unlock_event_waiters = _libs["usb-1.0"].get("libusb_unlock_event_waiters", "cdecl")
    libusb_unlock_event_waiters.argtypes = [POINTER(libusb_context)]
    libusb_unlock_event_waiters.restype = None

# /usr/include/libusb-1.0/libusb.h: 2212
if _libs["usb-1.0"].has("libusb_wait_for_event", "cdecl"):
    libusb_wait_for_event = _libs["usb-1.0"].get("libusb_wait_for_event", "cdecl")
    libusb_wait_for_event.argtypes = [POINTER(libusb_context), POINTER(struct_timeval)]
    libusb_wait_for_event.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2214
if _libs["usb-1.0"].has("libusb_handle_events_timeout", "cdecl"):
    libusb_handle_events_timeout = _libs["usb-1.0"].get("libusb_handle_events_timeout", "cdecl")
    libusb_handle_events_timeout.argtypes = [POINTER(libusb_context), POINTER(struct_timeval)]
    libusb_handle_events_timeout.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2216
if _libs["usb-1.0"].has("libusb_handle_events_timeout_completed", "cdecl"):
    libusb_handle_events_timeout_completed = _libs["usb-1.0"].get("libusb_handle_events_timeout_completed", "cdecl")
    libusb_handle_events_timeout_completed.argtypes = [POINTER(libusb_context), POINTER(struct_timeval), POINTER(c_int)]
    libusb_handle_events_timeout_completed.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2218
if _libs["usb-1.0"].has("libusb_handle_events", "cdecl"):
    libusb_handle_events = _libs["usb-1.0"].get("libusb_handle_events", "cdecl")
    libusb_handle_events.argtypes = [POINTER(libusb_context)]
    libusb_handle_events.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2219
if _libs["usb-1.0"].has("libusb_handle_events_completed", "cdecl"):
    libusb_handle_events_completed = _libs["usb-1.0"].get("libusb_handle_events_completed", "cdecl")
    libusb_handle_events_completed.argtypes = [POINTER(libusb_context), POINTER(c_int)]
    libusb_handle_events_completed.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2220
if _libs["usb-1.0"].has("libusb_handle_events_locked", "cdecl"):
    libusb_handle_events_locked = _libs["usb-1.0"].get("libusb_handle_events_locked", "cdecl")
    libusb_handle_events_locked.argtypes = [POINTER(libusb_context), POINTER(struct_timeval)]
    libusb_handle_events_locked.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2222
if _libs["usb-1.0"].has("libusb_pollfds_handle_timeouts", "cdecl"):
    libusb_pollfds_handle_timeouts = _libs["usb-1.0"].get("libusb_pollfds_handle_timeouts", "cdecl")
    libusb_pollfds_handle_timeouts.argtypes = [POINTER(libusb_context)]
    libusb_pollfds_handle_timeouts.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2223
if _libs["usb-1.0"].has("libusb_get_next_timeout", "cdecl"):
    libusb_get_next_timeout = _libs["usb-1.0"].get("libusb_get_next_timeout", "cdecl")
    libusb_get_next_timeout.argtypes = [POINTER(libusb_context), POINTER(struct_timeval)]
    libusb_get_next_timeout.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2229
class struct_libusb_pollfd(Structure):
    pass

struct_libusb_pollfd.__slots__ = [
    'fd',
    'events',
]
struct_libusb_pollfd._fields_ = [
    ('fd', c_int),
    ('events', c_short),
]

libusb_pollfd_added_cb = CFUNCTYPE(UNCHECKED(None), c_int, c_short, POINTER(None))# /usr/include/libusb-1.0/libusb.h: 2250

libusb_pollfd_removed_cb = CFUNCTYPE(UNCHECKED(None), c_int, POINTER(None))# /usr/include/libusb-1.0/libusb.h: 2262

# /usr/include/libusb-1.0/libusb.h: 2264
if _libs["usb-1.0"].has("libusb_get_pollfds", "cdecl"):
    libusb_get_pollfds = _libs["usb-1.0"].get("libusb_get_pollfds", "cdecl")
    libusb_get_pollfds.argtypes = [POINTER(libusb_context)]
    libusb_get_pollfds.restype = POINTER(POINTER(struct_libusb_pollfd))

# /usr/include/libusb-1.0/libusb.h: 2266
if _libs["usb-1.0"].has("libusb_free_pollfds", "cdecl"):
    libusb_free_pollfds = _libs["usb-1.0"].get("libusb_free_pollfds", "cdecl")
    libusb_free_pollfds.argtypes = [POINTER(POINTER(struct_libusb_pollfd))]
    libusb_free_pollfds.restype = None

# /usr/include/libusb-1.0/libusb.h: 2267
if _libs["usb-1.0"].has("libusb_set_pollfd_notifiers", "cdecl"):
    libusb_set_pollfd_notifiers = _libs["usb-1.0"].get("libusb_set_pollfd_notifiers", "cdecl")
    libusb_set_pollfd_notifiers.argtypes = [POINTER(libusb_context), libusb_pollfd_added_cb, libusb_pollfd_removed_cb, POINTER(None)]
    libusb_set_pollfd_notifiers.restype = None

libusb_hotplug_callback_handle = c_int# /usr/include/libusb-1.0/libusb.h: 2283

enum_anon_17 = c_int# /usr/include/libusb-1.0/libusb.h: 2298

LIBUSB_HOTPLUG_EVENT_DEVICE_ARRIVED = (1 << 0)# /usr/include/libusb-1.0/libusb.h: 2298

LIBUSB_HOTPLUG_EVENT_DEVICE_LEFT = (1 << 1)# /usr/include/libusb-1.0/libusb.h: 2298

libusb_hotplug_event = enum_anon_17# /usr/include/libusb-1.0/libusb.h: 2298

enum_anon_18 = c_int# /usr/include/libusb-1.0/libusb.h: 2308

LIBUSB_HOTPLUG_ENUMERATE = (1 << 0)# /usr/include/libusb-1.0/libusb.h: 2308

libusb_hotplug_flag = enum_anon_18# /usr/include/libusb-1.0/libusb.h: 2308

libusb_hotplug_callback_fn = CFUNCTYPE(UNCHECKED(c_int), POINTER(libusb_context), POINTER(libusb_device), libusb_hotplug_event, POINTER(None))# /usr/include/libusb-1.0/libusb.h: 2340

# /usr/include/libusb-1.0/libusb.h: 2378
if _libs["usb-1.0"].has("libusb_hotplug_register_callback", "cdecl"):
    libusb_hotplug_register_callback = _libs["usb-1.0"].get("libusb_hotplug_register_callback", "cdecl")
    libusb_hotplug_register_callback.argtypes = [POINTER(libusb_context), c_int, c_int, c_int, c_int, c_int, libusb_hotplug_callback_fn, POINTER(None), POINTER(libusb_hotplug_callback_handle)]
    libusb_hotplug_register_callback.restype = c_int

# /usr/include/libusb-1.0/libusb.h: 2395
if _libs["usb-1.0"].has("libusb_hotplug_deregister_callback", "cdecl"):
    libusb_hotplug_deregister_callback = _libs["usb-1.0"].get("libusb_hotplug_deregister_callback", "cdecl")
    libusb_hotplug_deregister_callback.argtypes = [POINTER(libusb_context), libusb_hotplug_callback_handle]
    libusb_hotplug_deregister_callback.restype = None

# /usr/include/libusb-1.0/libusb.h: 2406
if _libs["usb-1.0"].has("libusb_hotplug_get_user_data", "cdecl"):
    libusb_hotplug_get_user_data = _libs["usb-1.0"].get("libusb_hotplug_get_user_data", "cdecl")
    libusb_hotplug_get_user_data.argtypes = [POINTER(libusb_context), libusb_hotplug_callback_handle]
    libusb_hotplug_get_user_data.restype = POINTER(c_ubyte)
    libusb_hotplug_get_user_data.errcheck = lambda v,*a : cast(v, c_void_p)

# /usr/include/libusb-1.0/libusb.h: 2409
if _libs["usb-1.0"].has("libusb_set_option", "cdecl"):
    _func = _libs["usb-1.0"].get("libusb_set_option", "cdecl")
    _restype = c_int
    _errcheck = None
    _argtypes = [POINTER(libusb_context), enum_libusb_option]
    libusb_set_option = _variadic_function(_func,_restype,_argtypes,_errcheck)

# /usr/include/libusb-1.0/libusb.h: 171
try:
    LIBUSB_API_VERSION = 0x0100010A
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 179
try:
    LIBUSBX_API_VERSION = LIBUSB_API_VERSION
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 329
try:
    LIBUSB_DT_DEVICE_SIZE = 18
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 330
try:
    LIBUSB_DT_CONFIG_SIZE = 9
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 331
try:
    LIBUSB_DT_INTERFACE_SIZE = 9
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 332
try:
    LIBUSB_DT_ENDPOINT_SIZE = 7
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 333
try:
    LIBUSB_DT_ENDPOINT_AUDIO_SIZE = 9
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 334
try:
    LIBUSB_DT_HUB_NONVAR_SIZE = 7
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 335
try:
    LIBUSB_DT_SS_ENDPOINT_COMPANION_SIZE = 6
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 336
try:
    LIBUSB_DT_BOS_SIZE = 5
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 337
try:
    LIBUSB_DT_DEVICE_CAPABILITY_SIZE = 3
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 338
try:
    LIBUSB_DT_INTERFACE_ASSOCIATION_SIZE = 8
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 341
try:
    LIBUSB_BT_USB_2_0_EXTENSION_SIZE = 7
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 342
try:
    LIBUSB_BT_SS_USB_DEVICE_CAPABILITY_SIZE = 10
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 343
try:
    LIBUSB_BT_SSPLUS_USB_DEVICE_CAPABILITY_SIZE = 12
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 344
try:
    LIBUSB_BT_CONTAINER_ID_SIZE = 20
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 345
try:
    LIBUSB_BT_PLATFORM_DESCRIPTOR_MIN_SIZE = 20
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 348
try:
    LIBUSB_DT_BOS_MAX_SIZE = (((LIBUSB_DT_BOS_SIZE + LIBUSB_BT_USB_2_0_EXTENSION_SIZE) + LIBUSB_BT_SS_USB_DEVICE_CAPABILITY_SIZE) + LIBUSB_BT_CONTAINER_ID_SIZE)
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 354
try:
    LIBUSB_ENDPOINT_ADDRESS_MASK = 0x0f
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 355
try:
    LIBUSB_ENDPOINT_DIR_MASK = 0x80
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 369
try:
    LIBUSB_TRANSFER_TYPE_MASK = 0x03
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 473
try:
    LIBUSB_ISO_SYNC_TYPE_MASK = 0x0c
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 494
try:
    LIBUSB_ISO_USAGE_TYPE_MASK = 0x30
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 1170
try:
    LIBUSB_CONTROL_SETUP_SIZE = sizeof(struct_libusb_control_setup)
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 1330
try:
    LIBUSB_ERROR_COUNT = 14
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 1634
try:
    LIBUSB_OPTION_WEAK_AUTHORITY = LIBUSB_OPTION_NO_DEVICE_DISCOVERY
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 2312
try:
    LIBUSB_HOTPLUG_NO_FLAGS = 0
except:
    pass

# /usr/include/libusb-1.0/libusb.h: 2316
try:
    LIBUSB_HOTPLUG_MATCH_ANY = (-1)
except:
    pass

libusb_device_descriptor = struct_libusb_device_descriptor# /usr/include/libusb-1.0/libusb.h: 578

libusb_endpoint_descriptor = struct_libusb_endpoint_descriptor# /usr/include/libusb-1.0/libusb.h: 632

libusb_interface_association_descriptor = struct_libusb_interface_association_descriptor# /usr/include/libusb-1.0/libusb.h: 680

libusb_interface_association_descriptor_array = struct_libusb_interface_association_descriptor_array# /usr/include/libusb-1.0/libusb.h: 724

libusb_interface_descriptor = struct_libusb_interface_descriptor# /usr/include/libusb-1.0/libusb.h: 739

libusb_interface = struct_libusb_interface# /usr/include/libusb-1.0/libusb.h: 787

libusb_config_descriptor = struct_libusb_config_descriptor# /usr/include/libusb-1.0/libusb.h: 802

libusb_ss_endpoint_companion_descriptor = struct_libusb_ss_endpoint_companion_descriptor# /usr/include/libusb-1.0/libusb.h: 850

libusb_bos_dev_capability_descriptor = struct_libusb_bos_dev_capability_descriptor# /usr/include/libusb-1.0/libusb.h: 879

libusb_bos_descriptor = struct_libusb_bos_descriptor# /usr/include/libusb-1.0/libusb.h: 900

libusb_usb_2_0_extension_descriptor = struct_libusb_usb_2_0_extension_descriptor# /usr/include/libusb-1.0/libusb.h: 925

libusb_ss_usb_device_capability_descriptor = struct_libusb_ss_usb_device_capability_descriptor# /usr/include/libusb-1.0/libusb.h: 951

libusb_ssplus_sublink_attribute = struct_libusb_ssplus_sublink_attribute# /usr/include/libusb-1.0/libusb.h: 1029

libusb_ssplus_usb_device_capability_descriptor = struct_libusb_ssplus_usb_device_capability_descriptor# /usr/include/libusb-1.0/libusb.h: 1062

libusb_container_id_descriptor = struct_libusb_container_id_descriptor# /usr/include/libusb-1.0/libusb.h: 1087

libusb_platform_descriptor = struct_libusb_platform_descriptor# /usr/include/libusb-1.0/libusb.h: 1112

libusb_control_setup = struct_libusb_control_setup# /usr/include/libusb-1.0/libusb.h: 1141

libusb_context = struct_libusb_context# /usr/include/libusb-1.0/libusb.h: 1174

libusb_device = struct_libusb_device# /usr/include/libusb-1.0/libusb.h: 1175

libusb_device_handle = struct_libusb_device_handle# /usr/include/libusb-1.0/libusb.h: 1176

libusb_version = struct_libusb_version# /usr/include/libusb-1.0/libusb.h: 1181

libusb_iso_packet_descriptor = struct_libusb_iso_packet_descriptor# /usr/include/libusb-1.0/libusb.h: 1428

libusb_transfer = struct_libusb_transfer# /usr/include/libusb-1.0/libusb.h: 1458

libusb_init_option = struct_libusb_init_option# /usr/include/libusb-1.0/libusb.h: 1668

libusb_pollfd = struct_libusb_pollfd# /usr/include/libusb-1.0/libusb.h: 2229

# No inserted files

# No prefix-stripping

