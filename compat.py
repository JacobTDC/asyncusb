import ctypes
import os
import sys


def is_termux():
    return 'TERMUX_VERSION' in os.environ

def has_termux_api():
    return 'TERMUX_API_VERSION' in os.environ


def termux_compatibility_hook(path: str):
    """
    Calls libtermux-api#run_api_command to get a file descriptor and
    set TERMUX_USB_FD for the Termux patch of libusb; required to
    manipulate USB devices on Android.
    """

    run_api_command = ctypes.CDLL('libtermux-api.so').run_api_command
    run_api_command.argtypes = [ ctypes.c_int, ctypes.POINTER(ctypes.c_char_p) ]
    run_api_command.restype = ctypes.c_int

    #os.environ['TERMUX_EXPORT_FD'] = "true"

    #args = f"{sys.argv[0]} Usb -a open --ez request true"
    #if path is not None:
    #    args += f" --es device {path}"
    #elif vendorId is not None and productId is not None:
    #    args += f" --es vendorId {vendorId} --es productId {productId}"
    #else:
    #    raise TypeError("no device provided")

    args = f"{sys.argv[0]} Usb -a open --ez request true --es device {path}"
    argb = args.encode('utf8').split(b' ')
    argv = (ctypes.c_char_p * len(argb))(*argb)
    usb_fd = run_api_command(len(argv), argv)

    if usb_fd == -1:
        raise RuntimeError("Termux:API returned no file descriptor")

    os.environ['TERMUX_USB_FD'] = str(usb_fd)



__all__ = [
    "is_termux",
    "has_termux_api",
    "termux_compatibility_hook",
]
