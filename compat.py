import ctypes
import json
import os
import socket
import sys
from contextlib import contextmanager
from multiprocessing import Process
from shutil import which
from struct import Struct
from uuid import uuid4



class TermuxApi:
    _cred_struct = Struct('3i')

    def __init__(self):
        try:
            self._call = ctypes.CDLL('libtermux-api.so').contact_plugin
            self._call.argtypes = (ctypes.c_int,
                                   ctypes.POINTER(ctypes.c_char_p),
                                   ctypes.c_char_p,
                                   ctypes.c_char_p)
        except OSError:
            self._call = None

    def _run_command(self, args):
        """
        This is a reimplementation of libtermux-api#run_api_command to work
        around the fact that the C library leaks file descriptors and only
        outputs to stdout.
        """

        if not self._call:
            raise RuntimeError("failed to load library 'libtermux-api.so'")

        # Format arguments to pass to the library call.
        argb = args.encode().split(b' ')
        argv = (ctypes.c_char_p * (len(argb) + 1))(sys.argv[0].encode(), *argb)

        # Create socket address (can be anything unique per-invocation;
        # we'll go with UUIDs, as per the original library).
        in_addr = str(uuid4()).encode()

        # Create the socket.
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as in_sock:
            # Bind the socket to the address (abstract).
            in_sock.bind(b'\0' + in_addr)
            in_sock.listen()

            # Begin communication with the plugin. Passes in our arguments
            # and socket addresses (no out address, as we don't need it).
            p = Process(target=self._call, args=(len(argv), argv,
                                                 in_addr, b''))
            p.start()
            p.join()
            p.close()

            while True:
                # Wait for and accept a connection.
                with in_sock.accept()[0] as client_in_sock:
                    # Get the socket credentials.
                    creds = client_in_sock.getsockopt(socket.SOL_SOCKET,
                                                      socket.SO_PEERCRED,
                                                      self._cred_struct.size)
                    pid, uid, gid = self._cred_struct.unpack(creds)

                    # Only allow connections from the same uid. This
                    # probably isn't necessary (and isn't done in the actual
                    # library), but better safe than sorry!
                    if uid != os.getuid():
                        continue

                    # Get a single file descriptor (if given).
                    _, fds, _, _ = socket.recv_fds(client_in_sock, 0, 1)
                    fd = fds[0] if fds else None

                    # Convert the socket to a file-object and return it and the
                    # file descriptor (if any).
                    return fd, client_in_sock.makefile(mode='r')

    def run_command(self, args):
        fd, read = self._run_command(args)
        with read:
            return fd, read.read()

    def run_command_json(self, args):
        fd, read = self._run_command(args)
        with read:
            return fd, json.load(read)



_termux_api = TermuxApi()

def is_termux():
    """Check if we're running in a Termux environment."""
    return 'TERMUX_VERSION' in os.environ or which('termux-info') is not None

def has_termux_api():
    """Check if the termux-api package is installed."""
    return _termux_api._call is not None

def termux_list_devices() -> list[str]:
    """Get a list of USB device paths using Termux:API."""

    _, devs = _termux_api.run_command_json("Usb -a list")
    return devs

def termux_get_device(path: str) -> int:
    """
    Get a file descriptor from a USB device path using Termux:API.

    Useful when combined with core.Context(no_discovery=True) and
    context.wrap_sys_device(fd). Otherwise, it's recommended to use
    termux_compatibility_hook instead.
    """

    args = f"Usb -a open --ez request true --es device {path}"
    usb_fd, err = _termux_api.run_command(args)

    if usb_fd == None:
        raise RuntimeError(f"Termux:API: {err.strip()}")

    return usb_fd

def termux_compatibility_hook(path: str):
    """
    Set TERMUX_USB_FD to the result of termux_get_device for the Termux
    patch of libusb; allows using this library "normally" on Android.
    """

    os.environ['TERMUX_USB_FD'] = str(termux_get_device(path))



__all__ = [
    "is_termux",
    "has_termux_api",
    "termux_list_devices",
    "termux_get_device",
    "termux_compatibility_hook",
]
