import ctypes
import os
import sys



def is_termux():
    return 'TERMUX_VERSION' in os.environ

def has_termux_api():
    return 'TERMUX_API_VERSION' in os.environ

def get_termux_device(path: str) -> int:
    """
    Calls libtermux-api#run_api_command to get a file descriptor.

    Useful when combined with core.Context.wrap_sys_device.
    """

    run_api_command = ctypes.CDLL('libtermux-api.so').run_api_command
    run_api_command.argtypes = [ ctypes.c_int, ctypes.POINTER(ctypes.c_char_p) ]
    run_api_command.restype = ctypes.c_int

    args = f"{sys.argv[0]} Usb -a open --ez request true --es device {path}"
    argb = args.encode('utf8').split(b' ')
    argv = (ctypes.c_char_p * len(argb))(*argb)
    usb_fd = run_api_command(len(argv), argv)

    if usb_fd == -1:
        raise RuntimeError("Termux:API returned no file descriptor")

    return usb_fd

def termux_compatibility_hook(path: str):
    """
    Set TERMUX_USB_FD for to the result of get_termux_device for the Termux
    patch of libusb; required to manipulate USB devices on Android.
    """

    os.environ['TERMUX_USB_FD'] = str(get_termux_device(path))



__all__ = [
    "is_termux",
    "has_termux_api",
    "get_termux_device",
    "termux_compatibility_hook",
]
