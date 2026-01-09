import asyncio
import collections.abc
import errno
import select
import threading
from collections import deque
from contextlib import contextmanager, asynccontextmanager
from codecs import decode
from ctypes import POINTER, addressof, byref, c_int, c_ubyte, pointer
from enum import Enum, IntEnum, Flag, auto
from functools import wraps
from itertools import takewhile
from packaging.version import Version
from struct import Struct
from typing import Callable, Generator
from warnings import warn
from weakref import WeakSet, WeakValueDictionary, finalize, ref

from . import _libusb
from ._types import ImmutableStructProxyMeta, ImmutableStructProxy



# Get the current version of libusb in a comparable format for internal use.
_libusb_version_ptr = _libusb.libusb_get_version()
if not _libusb_version_ptr:
    raise RuntimeError("unable to get libusb version")
_libusb_version = (_libusb_version_ptr.contents.major << 48) + \
                  (_libusb_version_ptr.contents.minor << 32) + \
                  (_libusb_version_ptr.contents.micro << 16) + \
                  (_libusb_version_ptr.contents.nano  <<  0)
_libusb_version_string = f"{_libusb_version_ptr.contents.major}.{_libusb_version_ptr.contents.minor}.{_libusb_version_ptr.contents.micro}.{_libusb_version_ptr.contents.nano}{_libusb_version_ptr.contents.rc}"

def get_libusb_version() -> Version:
    """Get the version identifier for the installed version of libusb."""
    return Version(_libusb_version_string)



class LogLevel(IntEnum):
    """
    An enum representing the different log levels for libusb, to be provided
    to Context.set_debug(). See LIBUSB_LOG_LEVEL_* and libusb_set_debug.
    """
    NONE =    _libusb.LIBUSB_LOG_LEVEL_NONE     # 0
    ERROR =   _libusb.LIBUSB_LOG_LEVEL_ERROR    # 1
    WARNING = _libusb.LIBUSB_LOG_LEVEL_WARNING  # 2
    INFO =    _libusb.LIBUSB_LOG_LEVEL_INFO     # 3
    DEBUG =   _libusb.LIBUSB_LOG_LEVEL_DEBUG    # 4



class USBClass(IntEnum):
    """An enum representing the defined USB class codes."""
    PER_INTERFACE =       _libusb.LIBUSB_CLASS_PER_INTERFACE        # 0x00
    AUDIO =               _libusb.LIBUSB_CLASS_AUDIO                # 0x01
    COMM =                _libusb.LIBUSB_CLASS_COMM                 # 0x02
    HID =                 _libusb.LIBUSB_CLASS_HID                  # 0x03
    PHYSICAL =            _libusb.LIBUSB_CLASS_PHYSICAL             # 0x05
    PTP =                 _libusb.LIBUSB_CLASS_PTP                  # 0x06
    IMAGE =               _libusb.LIBUSB_CLASS_IMAGE                # 0x06
    PRINTER =             _libusb.LIBUSB_CLASS_PRINTER              # 0x07
    MASS_STORAGE =        _libusb.LIBUSB_CLASS_MASS_STORAGE         # 0x08
    HUB =                 _libusb.LIBUSB_CLASS_HUB                  # 0x09
    DATA =                _libusb.LIBUSB_CLASS_DATA                 # 0x0A
    SMART_CARD =          _libusb.LIBUSB_CLASS_SMART_CARD           # 0x0B
    CONTENT_SECURITY =    _libusb.LIBUSB_CLASS_CONTENT_SECURITY     # 0x0D
    VIDEO =               _libusb.LIBUSB_CLASS_VIDEO                # 0x0E
    PERSONAL_HEALTHCARE = _libusb.LIBUSB_CLASS_PERSONAL_HEALTHCARE  # 0x0F
    BILLBOARD =                                                     0x11
    BRIDGE =                                                        0x12
    I3C =                                                           0x3C
    DIAGNOSTIC_DEVICE =   _libusb.LIBUSB_CLASS_DIAGNOSTIC_DEVICE    # 0xDC
    WIRELESS =            _libusb.LIBUSB_CLASS_WIRELESS             # 0xE0
    MISCELLANEOUS =       _libusb.LIBUSB_CLASS_MISCELLANEOUS        # 0xEF
    APPLICATION =         _libusb.LIBUSB_CLASS_APPLICATION          # 0xFE
    VENDOR_SPEC =         _libusb.LIBUSB_CLASS_VENDOR_SPEC          # 0xFF



# TODO: remove experimental RequestType classes or move to seperate submodule
class RequestTypeFlags:
    __slots__ = ()

    def __or__(self, other):
        if type(self) is type(other):
            if isinstance(self, RequestTypeUnion):
                return other
            else:
                return RequestTypeUnion(other.value)

        elif isinstance(self, RequestTypeUnion):
            if isinstance(other, RequestDirection):
                value = self._value & 0b01111111 | other.value
            elif isinstance(other, RequestType):
                value = self._value & 0b10011111 | other.value
            elif isinstance(other, RequestRecipient):
                value = self._value & 0b11100000 | other.value
            else:
                raise TypeError("other must be instance of RequestTypeFlags")

            return RequestTypeUnion(value)

        elif isinstance(other, RequestTypeFlags):
            return RequestTypeUnion(self.value | other.value)

        else:
            raise TypeError("other must be an instance of RequestTypeFlags")

    def __int__(self):
        return self.value

    def __index__(self):
        return self.value

class RequestTypeUnion(RequestTypeFlags):
    """
    A combination of RequestDirection, RequestType, and RequestRecipient.
    The result is a value appropriate for the bmRequestType field.
    """
    __slots__ = ('_value')
    __key = object()

    def __init__(self, value):
        self._value = value

    def __eq__(self, other):
        return type(self) is type(other) and self._value == other._value

    def __hash__(self):
        return hash((self.__key, self._value))

    def __repr__(self):
        params = []
        params.append(RequestDirection(self._value & 0b10000000).name)
        params.append(RequestType(     self._value & 0b01100000).name)
        params.append(RequestRecipient(self._value & 0b00011111).name)
        return f"<RequestTypeUnion.{'|'.join(params)}: {int(self)}>"

    @property
    def value(self):
        return self._value

    @property
    def direction(self):
        return RequestDirection(self._value & 0b10000000)

    @property
    def type(self):
        return RequestType(self._value & 0b01100000)

    @property
    def recipient(self):
        return RequestRecipient(self._value & 0b00011111)

class RequestDirection(RequestTypeFlags, Enum):
    """The direction bit field for bmRequestType."""
    OUT =   _libusb.LIBUSB_ENDPOINT_OUT                 # (0<<7)
    IN =    _libusb.LIBUSB_ENDPOINT_IN                  # (1<<7)

class RequestType(RequestTypeFlags, Enum):
    """The type bit field for bmRequestType."""
    STANDARD =  _libusb.LIBUSB_REQUEST_TYPE_STANDARD    # (0<<5)
    CLASS =     _libusb.LIBUSB_REQUEST_TYPE_CLASS       # (1<<5)
    VENDOR =    _libusb.LIBUSB_REQUEST_TYPE_VENDOR      # (2<<5)
    RESERVED =  _libusb.LIBUSB_REQUEST_TYPE_RESERVED    # (3<<5)

class RequestRecipient(RequestTypeFlags, Enum):
    """The recipient bit field for bmRequestType."""
    DEVICE =    _libusb.LIBUSB_RECIPIENT_DEVICE         # (0<<0)
    INTERFACE = _libusb.LIBUSB_RECIPIENT_INTERFACE      # (1<<0)
    ENDPOINT =  _libusb.LIBUSB_RECIPIENT_ENDPOINT       # (2<<0)
    OTHER =     _libusb.LIBUSB_RECIPIENT_OTHER          # (3<<0)



class USBError(Exception):
    """The base USB exception type."""
    pass

class IOError(USBError):
    """A generic I/O error."""
    pass

class AccessError(USBError, PermissionError):
    """
    An error raised when access to a device is denied. It could be that the
    user lacks the necessary permissions, or the device is already in use
    elsewhere (such as the kernel driver).

    This is an OSError subclass because it is almost always caused by a
    system EACCES (on POSIX systems).
    """
    pass

class NoDeviceError(USBError, OSError):
    """
    An error raised when IO is attempted on a non-present device. The device
    may not exist, or may have been disconnected.

    This is an OSError subclass because it is almost always caused by a
    system ENODEV (on POSIX systems).
    """
    pass

class NotFoundError(USBError):
    """
    An error raised if the requested device or resource could not be found.
    """
    pass

class ResourceBusyError(USBError):
    """
    An error raised when IO is attempted on a device or resource that is
    currently in use, and as such, can't be accessed by a new request.
    """
    pass

class OverflowError(USBError, OSError):
    """
    An error raised when more data is received from a device than space was
    allocated for the transfer.

    This is an OSError subclass because it is almost always caused by a
    system EOVERFLOW (on POSIX systems).
    """
    pass

class PipeError(USBError, BrokenPipeError):
    """
    An error raised when a USB pipe error is encountered, usually due to a
    halt or stall condition.

    This is an OSError subclass because it is almost always caused by a
    system EPIPE (on POSIX systems).
    """
    pass

class NotSupportedError(USBError, NotImplementedError):
    """
    An error raised when an operation is not supported by the system, device
    drivers, or installed libusb version.
    """
    pass



_errmap = {
    _libusb.LIBUSB_ERROR_IO: (IOError,),
    _libusb.LIBUSB_ERROR_INVALID_PARAM: (ValueError,),
    _libusb.LIBUSB_ERROR_ACCESS: (AccessError, errno.EACCES),
    _libusb.LIBUSB_ERROR_NO_DEVICE: (NoDeviceError, errno.ENODEV),
    _libusb.LIBUSB_ERROR_NOT_FOUND: (NotFoundError,),
    _libusb.LIBUSB_ERROR_BUSY: (ResourceBusyError,),
    _libusb.LIBUSB_ERROR_TIMEOUT: (TimeoutError,),
    _libusb.LIBUSB_ERROR_OVERFLOW: (OverflowError, errno.EOVERFLOW),
    _libusb.LIBUSB_ERROR_PIPE: (PipeError, errno.EPIPE),
    _libusb.LIBUSB_ERROR_INTERRUPTED: (InterruptedError, errno.EINTR),
    _libusb.LIBUSB_ERROR_NO_MEM: (MemoryError,),
    _libusb.LIBUSB_ERROR_NOT_SUPPORTED: (NotSupportedError,),
    _libusb.LIBUSB_ERROR_OTHER: (USBError,)
}

# Used to map and message errors encountered from libusb.
def _error(e, message = None, /, *args, **kwargs):
    if not message:
        message = _libusb.libusb_strerror(e).decode('utf8')

    if e in _errmap:
        errtype, *errargs = _errmap[e]
        return errtype(*errargs, message)
    else:
        return RuntimeError(message)

# Catch, map, and raise errors from libusb.
def _catch(e, message = None):
    if e < 0:
        raise _error(e, message)
    else:
        return e



class EndpointDirection(Enum):
    """An enum representing the directionality of an endpoint."""
    OUT = _libusb.LIBUSB_ENDPOINT_OUT   # 0x00
    IN =  _libusb.LIBUSB_ENDPOINT_IN    # 0x80



class EndpointType(Enum):
    """An enum representing the transfer type of an endpoint."""
    CONTROL =     _libusb.LIBUSB_ENDPOINT_TRANSFER_TYPE_CONTROL     # 0
    ISOCHRONOUS = _libusb.LIBUSB_ENDPOINT_TRANSFER_TYPE_ISOCHRONOUS # 1
    BULK =        _libusb.LIBUSB_ENDPOINT_TRANSFER_TYPE_BULK        # 2
    INTERRUPT =   _libusb.LIBUSB_ENDPOINT_TRANSFER_TYPE_INTERRUPT   # 3



class Endpoint(ImmutableStructProxy):
    """A wrapper for libusb_endpoint_descriptor."""

    __slots__ = ('_interface',)
    _struct_ = _libusb.struct_libusb_endpoint_descriptor
    _hidden_fields_ = ('bDescriptorType', 'bLength', 'extra', 'extra_length')

    def __init__(self, desc, interface):
        super().__init__(desc)
        self._interface = interface

    def __repr__(self):
        return f"<{type(self).__module__}.{type(self).__name__} 0x{self.bEndpointAddress:0{2}X}>"

    def __int__(self):
        """Returns self.bEndpointAddress."""
        return self.bEndpointAddress

    @property
    def extra(self) -> list[int]:
        return self._contents.extra[:self._contents.extra_length]

    @property
    def direction(self) -> EndpointDirection:
        """The directionality of this endpoint, as an EndpointDirection value."""
        return EndpointDirection(self.bEndpointAddress & _libusb.LIBUSB_ENDPOINT_DIR_MASK)

    @property
    def transfer_type(self) -> EndpointType:
        """The transfer type of this endpoint, as an EndpointType value."""
        return EndpointType(self.bmAttributes & 0b11)



class Interface(ImmutableStructProxy):
    """
    A wrapper for libusb_interface_descriptor.

    This class, unlike its relatives, does not support int(self). This is
    due to the fact that the interface is identified using a combination of
    both self.bInterfaceNumber and self.bAlternateSetting.

    For bNumEndpoints, use len(self.endpoints).
    """

    __slots__ = ('_config', '_endpoints')
    _struct_ = _libusb.struct_libusb_interface_descriptor
    _hidden_fields_ = ('bDescriptorType', 'bLength', 'bNumEndpoints', 'endpoint', 'extra', 'extra_length')

    def __init__(self, desc, config):
        super().__init__(desc)
        self._config = config
        self._endpoints = tuple( Endpoint(ept, self) for ept in self._contents.endpoint[:self._contents.bNumEndpoints] )

    def __repr__(self):
        return f"<{type(self).__module__}.{type(self).__name__} {self.bInterfaceNumber}[{self.bAlternateSetting}]>"

    @property
    def extra(self) -> list[int]:
        return self._contents.extra[:self._contents.extra_length]

    @property
    def endpoints(self) -> list[Endpoint]:
        """A list of Endpoints defined under this Interface."""
        return self._endpoints

    #@property
    #def interface_class(self) -> USBClass:
    #    """The defined class code of the interface."""
    #    return USBClass(self.bInterfaceClass)



class Configuration(ImmutableStructProxy):
    """
    A wrapper for libusb_config_descriptor.
    Configuration instances are not tied to their "parent" Context and will
    survive until garbage collection, even if the Context is closed.

    For bNumInterfaces, use len(self.interfaces).
    """

    __slots__ = ('__weakref__', '_interfaces', '_dev_speed')
    _struct_ = _libusb.struct_libusb_config_descriptor
    _hidden_fields_ = ('MaxPower', 'bDescriptorType', 'bLength', 'bNumInterfaces', 'extra', 'extra_length', 'interface')

    def __init__(self, desc_ptr, dev_speed):
        super().__init__(desc_ptr.contents)
        self._dev_speed = dev_speed
        finalize(self, _libusb.libusb_free_config_descriptor, desc_ptr)

        self._interfaces = tuple( tuple( Interface(alt, self) for alt in intf.altsetting[:intf.num_altsetting] ) for intf in self._contents.interface[:self._contents.bNumInterfaces] )

    def __int__(self):
        """Equivalent to self.bConfigurationValue."""
        return self.bConfigurationValue

    def __repr__(self):
        return f"<{type(self).__module__}.{type(self).__name__} {self.bConfigurationValue}: {self.max_power} mA>"

    @property
    def extra(self) -> list[int]:
        return self._contents.extra[:self._contents.extra_length]

    @property
    def interfaces(self) -> tuple[tuple[Interface]]:
        """
        A list (of lists) of Interfaces defined under this Configuration.
        Structured as self.interfaces[interface][altsetting].
        """
        return self._interfaces

    @property
    def max_power(self) -> int:
        """Maximum current draw of the Configuration, in milliamps."""

        if self._dev_speed >= Speed.HIGH:
            return self._contents.MaxPower * 2
        elif self._dev_speed >= Speed.SUPER:
            return self._contents.MaxPower * 8
        else:
            return self._contents.MaxPower



class _PendingCollection:
    """
    Used to keep track of pending transfers and prevent garbage collection.
    Thread-safe add method.
    """

    __slots__ = ('_data', '_lock', '_waiters', '_loop')

    def __init__(self):
        self._data = set()
        self._lock = threading.Lock()
        self._waiters = deque()
        self._loop = asyncio.get_event_loop()

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def add(self, item):
        with self._lock:
            self._data.add(item)

    def remove(self, item):
        with self._lock:
            self._data.remove(item)
            if not self._data:
                for future in self._waiters:
                    if not future.done():
                        future.set_result(True)

    async def wait(self):
        with self._lock:
            if not self._data:
                return True

            future = self._loop.create_future()
            self._waiters.append(future)

        try:
            await future
            return True
        finally:
            self._waiters.remove(future)



class DeviceHandle:
    """
    A class that represents an open USB Device.

    Most methods, such as those that create new Transfer instances or
    perform device communication, are thread safe unless otherwise noted.

    All Transfer instances submitted to a handle should be allowed to finish
    before exiting or closing the handle. If there are still pending
    transfers when the handle is closed, they will be cancelled, and a
    warning will be displayed. Transfers cancelled in this way are not
    guaranteed to still be alive once the callback executes, and will raise
    an error if the callback attempts to resubmit them.
    """

    __slots__ = ('__weakref__', '_obj', '_transfers', '_closing', '_pending',
                 '_lock', '_context')

    def __init__(self, context):
        """
        Initializes a NULL DeviceHandle instance.

        New instances should not be created/initialized from user code.
        Device.open or Context.wrap_sys_device should be used, instead.
        """

        self._transfers = WeakSet()
        self._pending = _PendingCollection()
        self._obj = POINTER(_libusb.struct_libusb_device_handle)()
        self._closing = False
        self._lock = threading.Lock()
        self._context = context

    def __bool__(self):
        """
        Return bool(self).
        True if the DeviceHandle instance is open.
        """
        return not self._closing and bool(self._obj)


    def _open(self, device_ref):
        """
        Open this DeviceHandle; to be called by Device.open(). Returns an
        async function used to safely close the handle. The returned
        function is not thread safe.

        Calling this from user code is not supported.
        """

        loop = asyncio.get_running_loop()
        if loop is not self._context._loop:
            raise RuntimeError("DeviceHandle instances must be opened in the Context event loop")

        # Open the underlying libusb_device_handle.
        if device_ref is not None:
            _catch( _libusb.libusb_open(device_ref, self._obj) )

        # The function used to close the device handle, to be passed back
        # to the Device.open() context manager.
        async def close():
            if not self._context:
                raise RuntimeError("invalid context")

            with self._lock:
                # Prevent transfers from registering or submitting.
                self._closing = True

            # Cancel pending transfers. Relying on this behavior is
            # discouraged.
            if self._pending:
                warn(UserWarning("DeviceHandle instance closed on pending transfers; transfers will be cancelled"))
                for transfer in self._pending:
                    try:
                        transfer.cancel()
                    except err:
                        # Errors from transfer.cancel probably won't
                        # break anything, and it's more important that
                        # we continue.
                        warn(RuntimeWarning(err))

            # Ensure all transfers have completed.
            await self._pending.wait()

            # Free all attached transfers.
            while self._transfers:
                try:
                    self._transfers.pop()._free()
                except KeyError:
                    # This could occur if GC released objects.
                    break

            # Close the handle.
            _libusb.libusb_close(self._obj)
            del self._obj

        return close


    def _register_transfer(self, transfer):
        # Lock to ensure open state and single modification.
        with self._lock:
            if not self:
                raise RuntimeError("cannot register transfer to closed DeviceHandle")

            self._transfers.add(transfer)


    def is_closing(self) -> bool:
        """True if this DeviceHandle is closed or in the process of closing."""
        return self._closing


    def get_device(self):
        """Get the Device this handle is attached to."""
        return Device(_libusb.libusb_get_device(self._obj).contents,
                      self._context)


    def get_string(self, index: int) -> str:
        if index == 0:
            return None
        elif index < 0 or index > 255:
            raise ValueError("string descriptor index out of bounds")

        buffer = (c_ubyte * 255)()
        result = _libusb.libusb_control_transfer(
            self._obj, _libusb.LIBUSB_ENDPOINT_IN,
            _libusb.LIBUSB_REQUEST_GET_DESCRIPTOR,
            (_libusb.LIBUSB_DT_STRING << 8) | index, 0, buffer, 255, 0)

        if result == _libusb.LIBUSB_ERROR_PIPE:
            raise NotFoundError("invalid string descriptor")
        elif result < 0:
            raise _error(result)

        return decode(memoryview(buffer)[2:result], 'utf-16le')


    def control_transfer(self, bmRequestType: int, bRequest: int, wValue: int,
                         wIndex: int, buffer: collections.abc.Buffer | int,
                         timeout: int = 0, copy: bool = True) -> bytes:
        """
        control_transfer(bmRequestType, bRequest, wValue, wIndex,
                         data_or_length, timeout)
        control_transfer(bmRequestType, bRequest, wValue, wIndex,
                         writeable_buffer, timeout, False)

        Send a control transfer, and block until timeout or completion.

        Returns the data successfully transferred. This may be less than the
        original buffer size (in libusb terms, `len(bytes) == actual_length`).

        If copy is True (the default), the data from the provided buffer
        will be copied into a new buffer for transfer, without modifying the
        original buffer. Otherwise, the underlying memory address of the
        provided buffer will be passed to libusb, and any received data will
        be written into it.

        If the transfer timed out, a TimeoutError will be raised. In such
        case, it is not possible to determine the amount of data that did
        successfully transfer due to a limitation of libusb. If this is
        important, consider using no timeout, or submit a Transfer object.

        If the transfer size was larger than the operating system and/or
        hardware can support, a ValueError will be raised.
        """

        if buffer is None or isinstance(buffer, int):
            buffer = (c_ubyte * (buffer or 0))()
        else:
            with memoryview(buffer) as view:
                if copy:
                    buffer = (c_ubyte * view.nbytes).from_buffer_copy(view)
                else:
                    buffer = (c_ubyte * view.nbytes).from_buffer(view)

        result = _libusb.libusb_control_transfer(self._obj,
                                                 bmRequestType, bRequest,
                                                 wValue, wIndex, buffer,
                                                 len(buffer), timeout)

        # Perform special case error mapping.
        match result:
            case _libusb.LIBUSB_ERROR_PIPE:
                raise _error(result, "Unsupported control request")
            case _libusb.LIBUSB_ERROR_INVALID_PARAM:
                raise _error(result, "Transfer size too large")
            case _:
                _catch(result)

        return memoryview(buffer)[:result].tobytes()

    def bulk_transfer(self, endpoint: Endpoint | int,
                      buffer: collections.abc.Buffer | int,
                      timeout: int = 0, copy: bool = True) -> bytes:
        """
        bulk_transfer(endpoint, data_or_length, timeout)
        bulk_transfer(endpoint, writable_buffer, timeout, False)

        Send a bulk transfer, and block until timeout or completion.

        Returns the data successfully transferred. This may be less than the
        original buffer size (in libusb terms, `len(bytes) == actual_length`).

        If copy is True (the default), the data from the provided buffer
        will be copied into a new buffer for transfer, without modifying the
        original buffer. Otherwise, the underlying memory address of the
        provided buffer will be passed to libusb, and any received data will
        be written into it.

        If the transfer timed out, a TimeoutError will be raised, of which
        the `data` attribute will contain the successfully transfered data.

        If the transfer size was larger than the operating system and/or
        hardware can support, a ValueError will be raised.
        """

        if isinstance(endpoint, Endpoint):
            endpoint = int(endpoint)

        if buffer is None or isinstance(buffer, int):
            buffer = (c_ubyte * (buffer or 0))()
        else:
            with memoryview(buffer) as view:
                if copy:
                    buffer = (c_ubyte * view.nbytes).from_buffer_copy(view)
                else:
                    buffer = (c_ubyte * view.nbytes).from_buffer(view)

        transferred = c_int(0)
        result = _libusb.libusb_bulk_transfer(self._obj, endpoint, buffer,
                                              len(buffer), transferred, timeout)

        # Perform special case error mapping.
        match result:
            case _libusb.LIBUSB_ERROR_TIMEOUT:
                error = _error(result)
                error.data = bytes(buffer)[:transferred.value]
                raise error
            case _libusb.LIBUSB_ERROR_PIPE:
                raise _error(result, "Endpoint halted")
            case _libusb.LIBUSB_ERROR_INVALID_PARAM:
                raise _error(result, "Transfer size too large")
            case _:
                _catch(result)

        return memoryview(buffer)[:transferred.value].tobytes()


    def kernel_driver_active(self, interface: Interface | int):
        """Determine if a kernel driver is active on an interface."""

        if isinstance(interface, Interface):
            interface = interface.bInterfaceNumber
        return bool( _catch(_libusb.libusb_kernel_driver_active(self._obj,
                                                                interface) ))

    def detach_kernel_driver(self, interface: Interface | int):
        """
        Detach a kernel driver from an interface.

        If successful, you will then be able to claim the interface and
        perform I/O.
        """

        if isinstance(interface, Interface):
            interface = interface.bInterfaceNumber
        _catch( _libusb.libusb_detach_kernel_driver(self._obj, interface) )

    def attach_kernel_driver(self, interface: Interface | int):
        """
        Re-attach an interface's kernel driver, which was previously detached
        using detach_kernel_driver().
        """

        if isinstance(interface, Interface):
            interface = interface.bInterfaceNumber
        _catch( _libusb.libusb_attach_kernel_driver(self._obj, interface) )

    def set_auto_detach_kernel_driver(self, enable: bool):
        """
        Set if libusb should automatically handle detaching and reattaching
        kernel drivers.
        """
        _catch( _libusb.libusb_set_auto_detach_kernel_driver(self._obj, enable) )


    def claim_interface(self, interface: Interface | int):
        """
        Claim an interface.

        You must claim the interface you wish to use before you can perform
        I/O on any of its endpoints.

        If auto_detach_kernel_driver is set to True, the kernel driver will
        be detached if necessary, on failure the detach error is raised.
        """

        if isinstance(interface, Interface):
            interface = interface.bInterfaceNumber
        _catch( _libusb.libusb_claim_interface(self._obj, interface) )

    def release_interface(self, interface: Interface | int):
        """
        Release an interface.

        You should release all claimed interfaces before closing a device
        handle.

        This is a blocking function. A SET_INTERFACE control request will be
        sent to the device, resetting interface state to the first alternate
        setting.

        If auto_detach_kernel_driver is set to True, the kernel driver will
        be re-attached after releasing the interface.
        """

        if isinstance(interface, Interface):
            interface = interface.bInterfaceNumber
        _catch( _libusb.libusb_release_interface(self._obj, interface) )

    @contextmanager
    def bind_interface(self, interface: Interface | int) -> Generator[None, None, None]:
        """
        A utility context manager that calls claim_interface on entry and
        release_interface (ignoring NoDeviceErrors) on exit.
        """

        self.claim_interface(interface)

        try:
            yield
        finally:
            try:
                self.release_interface(interface)
            except NoDeviceError:
                pass


    def set_interface_alt_setting(self, interface: Interface | int,
                                  altsetting: int = None):
        """
        set_interface_alt_setting(interface_obj)
        set_interface_alt_setting(interface_num, alt_num)

        Activate an alternate setting for an interface.
        """

        if altsetting is None:
            if not isinstance(interface, Interface):
                raise TypeError("altsetting must be provided if interface is not an Interface object")

            altsetting = interface.bAlternateSetting
            interface = interface.bInterfaceNumber

        _catch( _libusb.libusb_set_interface_alt_setting(
            self._obj, interface, altsetting) )

    def reset(self):
        """
        Perform a USB port reset to reinitialize a device.

        The system will attempt to restore the previous configuration and
        alternate settings after the reset has completed.

        If the reset fails (with a NotFoundError), the descriptors change,
        or the previous state cannot be restored, the device will appear to
        be disconnected and reconnected. This means that the device handle
        is no longer valid (you should close it and rediscover the device).

        This is a blocking function which usually incurs a noticeable delay.
        """
        _catch( _libusb.libusb_reset_device(self._obj) )

    def clear_halt(self, endpoint: int | Endpoint):
        """Clear the halt/stall condition for an endpoint."""

        _catch( _libusb.libusb_clear_halt(self._obj, int(endpoint)) )

    def get_configuration(self) -> int:
        """
        Gets the value of the active configuration. Unlike
        Device.get_active_config, this is a blocking call that makes a
        request to the device instead of relying on the OS cache.

        Returns 0 if unconfigured.
        """

        config = c_int()
        _catch( _libusb.libusb_get_configuration(self._obj, config) )
        return config.value

    def set_configuration(self, config: int | Configuration):
        """Sets the active configuration for the device."""

        _catch( _libusb.libusb_set_configuration(self._obj, int(config)) )

    def check_connected(self) -> bool:
        """Returns True if the device is still connected, False otherwise."""

        try:
            self.control_transfer(0x80, 0x00, 0, 0, 2)
        except NoDeviceError:
            return False
        return True


    def cancel_all(self):
        """
        Cancel all registered transfers. Does not prevent them from
        resubmitting.

        Thread-safe.
        """

        # Lock to ensure the transfers collection isn't modified while
        # iterating.
        with self._lock:
            for transfer in self._transfers:
                transfer.cancel()

    def is_clear(self) -> bool:
        """
        True if there are no pending transfers for this handle. Not reliable
        if transfers are being managed from other threads.
        """
        return not self._pending

    async def wait_clear(self):
        """
        Wait until there are no pending transfers for this handle. Not
        reliable if transfers are being managed from other threads.

        Not thread-safe.
        """

        while self._pending:
            await self._pending.wait()


    def alloc_transfer(self, iso_packets: int = 0) -> 'Transfer':
        """Allocate a new Transfer for this DeviceHandle."""
        return Transfer(self, iso_packets)

    def fill_control_transfer(self, bmRequestType: int = 0,
                              bRequestCode: int = 0,
                              wValue: int = 0, wIndex: int = 0,
                              data: collections.abc.Buffer = None,
                              callback: Callable = None,
                              timeout: int = 0) -> 'Transfer':
        """
        A helper function to create a new Transfer for this DeviceHandle and
        populate the required fields for a control transfer.
        """

        transfer = self.alloc_transfer(0)
        transfer.type = TransferType.CONTROL
        transfer.endpoint = 0
        transfer.set_callback(callback)
        transfer.timeout = timeout

        transfer.buffer = ControlTransferBuffer(bmRequestType, bRequestCode, 
                                                wValue, wIndex, data)

        return transfer

    def fill_bulk_transfer(self, endpoint: int | Endpoint, buffer = None,
                           callback: Callable = None,
                           timeout: int = 0) -> 'Transfer':
        """
        A helper function to create a new Transfer for this DeviceHandle and
        populate the required fields for a bulk transfer.
        """

        transfer = self.alloc_transfer(0)
        transfer.type = TransferType.BULK
        transfer.endpoint = endpoint
        transfer.set_callback(callback)
        transfer.timeout = timeout

        if isinstance(buffer, TransferBuffer):
            transfer.buffer = buffer
        elif buffer is not None:
            transfer.buffer = TransferBuffer(buffer)

        return transfer

    def fill_interrupt_transfer(self, endpoint: int | Endpoint, buffer = None,
                                callback: Callable = None,
                                timeout: int = 0) -> 'Transfer':
        """
        A helper function to create a new Transfer for this DeviceHandle and
        populate the required fields for an interrupt transfer.
        """

        transfer = self.alloc_transfer(0)
        transfer.type = TransferType.INTERRUPT
        transfer.endpoint = endpoint
        transfer.set_callback(callback)
        transfer.timeout = timeout

        if isinstance(buffer, TransferBuffer):
            transfer.buffer = buffer
        elif buffer is not None:
            transfer.buffer = TransferBuffer(buffer)

        return transfer



class Speed(IntEnum):
    """An enum representing the speed of a USB device. See LIBUSB_SPEED_*."""
    UNKNOWN =    _libusb.LIBUSB_SPEED_UNKNOWN
    LOW =        _libusb.LIBUSB_SPEED_LOW
    FULL =       _libusb.LIBUSB_SPEED_FULL
    HIGH =       _libusb.LIBUSB_SPEED_HIGH
    SUPER =      _libusb.LIBUSB_SPEED_SUPER
    SUPER_PLUS = _libusb.LIBUSB_SPEED_SUPER_PLUS



class _DeviceMeta(ImmutableStructProxyMeta):
    """
    A scoped-singleton meta, where the scope is the address of the
    provided libusb_device (in a Context).
    """

    def __call__(self, device_ref, context):
        key = addressof(device_ref)

        if key in context._devices:
            return context._devices[key]
        else:
            with context._lock:
                instance = super().__call__(device_ref, context)
                context._devices[key] = instance
                return instance

class Device(ImmutableStructProxy, metaclass=_DeviceMeta):
    """
    A wrapper for libusb_device and libusb_device_descriptor.

    For bNumConfigurations, use len(device.configs).
    """

    __slots__ = ('__weakref__', '_obj', '_context', '_configs', '_speed',
                 '_unref')
    _struct_ = _libusb.struct_libusb_device_descriptor
    _hidden_fields_ = ('bDescriptorType', 'bLength', 'bNumConfigurations')

    def __init__(self, device_ref, context):
        super().__init__()

        # Hold reference.
        _libusb.libusb_ref_device(device_ref)

        self._obj = device_ref
        self._context = context
        self._speed = Speed(_libusb.libusb_get_device_speed(device_ref))

        # Populate the device descriptor.
        _catch( _libusb.libusb_get_device_descriptor(device_ref,
                                                     byref(self._contents)) )

        # Get configurations. Must be done after getting speed and populating
        # the underlying device descriptor.
        def config(index):
            config_ptr = POINTER(_libusb.struct_libusb_config_descriptor)()
            _catch( _libusb.libusb_get_config_descriptor(self._obj, index,
                                                         byref(config_ptr)) )
            return Configuration(config_ptr, self.speed)

        self._configs = tuple( config(i) for i in range(
            0, self._contents.bNumConfigurations) )

        # Schedule finalization within the Context, to be invoked
        # either at garbage collection or upon exiting the context.
        def unref(selfref, device_ref):
            self = selfref()
            if self is not None:
                del self._obj
                del self._context

            _libusb.libusb_unref_device(device_ref)

        self._unref = finalize(self, unref, ref(self), device_ref)

    def __repr__(self):
        return f"<{type(self).__module__}.{type(self).__name__} {self.idVendor:0{4}X}:{self.idProduct:0{4}X}>"

    def __bool__(self):
        """
        Return bool(self).
        Used to test if the device reference is still valid. Should return
        True if the parent Context hasn't been exited.
        """

        return hasattr(self, '_obj')

    @asynccontextmanager
    async def open(self) -> Generator[DeviceHandle, None, None]:
        """
        Open a DeviceHandle for I/O on this device.

        Not thread-safe. Must be called from the same thread as the Context
        event loop.
        """

        if not self:
            raise RuntimeError("invalid context")

        handle = DeviceHandle(self._context)
        close = handle._open(self._obj)

        # Allow garbage collection.
        del self

        try:
            yield handle
        finally:
            await asyncio.shield(close())

    @property
    def speed(self) -> Speed:
        """The speed of the device."""
        return self._speed

    @property
    def usb_version(self) -> float:
        """The USB specification release number, decoded from self.bcdUSB."""
        return (self.bcdUSB >> 12) * 10 + \
               (self.bcdUSB >> 8 & 15) + \
               (self.bcdUSB >> 4 & 15) * 0.1 + \
               (self.bcdUSB & 15) * 0.01

    @property
    def device_revision(self) -> float:
        """The device revision number, decoded from self.bcdDevice."""
        return (self.bcdDevice >> 12) * 10 + \
               (self.bcdDevice >> 8 & 15) + \
               (self.bcdDevice >> 4 & 15) * 0.1 + \
               (self.bcdDevice & 15) * 0.01

    #@property
    #def device_class(self) -> USBClass:
    #    """The defined USB class of the device."""
    #    return USBClass(self.bDeviceClass)

    @property
    def configs(self) -> tuple[Configuration]:
        """A tuple containing all the Configurations for this device."""
        return self._configs

    def get_active_config(self) -> Configuration:
        """
        Get the active Configuration for this device.

        Returns None if unconfigured.
        """

        if not self:
            raise RuntimeError("invalid context")

        # Get the config descriptor, obtain the bConfigurationValue,
        # and free the descriptor.
        config_ptr = POINTER(_libusb.struct_libusb_config_descriptor)()
        err = _libusb.libusb_get_active_config_descriptor(self._obj,
                                                          byref(config_ptr) )

        if err == _libusb.LIBUSB_ERROR_NOT_FOUND:
            return None
        else:
            _catch(err)

        value = config_ptr.contents.bConfigurationValue
        _libusb.libusb_free_config_descriptor(config_ptr)

        for config in self._configs:
            if config.bConfigurationValue == value:
                return config

    def get_parent(self) -> 'Device':
        """Get the parent device."""

        if not self:
            raise RuntimeError("invalid context")

        # Hold the device list.
        p_list = POINTER(POINTER(_libusb.libusb_device))()
        _catch( _libusb.libusb_get_device_list(self._context._obj, p_list) )

        try:
            parent = _libusb.libusb_get_parent(self._obj)

            if parent:
                return Device(parent.contents, self._context)
            else:
                return None
        finally:
            # Free the device list.
            _libusb.libusb_free_device_list(p_list, True)



class TransferBuffer(collections.abc.MutableSequence):
    """
    A bytearray-like class for use with Transfer objects. Enforces thread
    and transit safety. Cannot be modified while in-transit.
    """

    __slots__ = ('_buffer', '_views', '_lock', '_acquired')

    def __init__(self, data: int | collections.abc.Buffer = 0):
        self._buffer = bytearray(data)
        self._views = WeakValueDictionary()
        self._lock = threading.Lock()
        self._acquired = False

    def __buffer__(self, flags):
        with self._lock:
            if self._acquired:
                raise RuntimeError("operation forbidden on locked buffer")

            view = memoryview(self._buffer)
            self._views[id(view)] = view
            return view

    def __release_buffer__(self, view):
        view.release()
        with self._lock:
            del self._views[id(view)]

    def _acquire(self):
        with self._lock:
            if self._views or self._acquired:
                raise RuntimeError("existing exports of data: object cannot be acquired")

            self._acquired = True
            return (len(self._buffer),
                    pointer(c_ubyte.from_buffer(self._buffer)))

    def _release(self):
        with self._lock:
            self._acquired = False

    @staticmethod
    def _modify(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with self._lock:
                if self._acquired:
                    raise RuntimeError("cannot modify locked buffer")
                return func(self, *args, **kwargs)
        return wrapper

    def __getitem__(self, key):
        return self._buffer[key]

    @_modify
    def __setitem__(self, key, value):
        self._buffer[key] = value

    @_modify
    def __delitem__(self, key):
        del self._buffer[key]

    def __len__(self):
        return len(self._buffer)

    @_modify
    def insert(self, index, item):
        self._buffer.insert(index, item)

    @_modify
    def extend(self, iterable):
        self._buffer.extend(iterable)

    @_modify
    def clear(self):
        self._buffer.clear()



class ControlTransferBuffer(TransferBuffer):
    """
    A subclass of TransferBuffer with a control setup packet.

    While the control setup packet *is* part of the underlying buffer that
    is passed to the transfer, the data contained within is only accessible
    via. the relevant attributes. This is to simplify usage and prevent
    accidental modification of the setup fields. If you need direct access
    to the setup packet, you can use a regular TransferBuffer instead.

    Likewise, functions such as len(self) only return the size of the data
    portion of the buffer. Should you need the actual, full length of the
    buffer, including the setup packet (for example, to compare to
    Transfer.transferred to check for short frames), you can get it using
    actual_length(), but it's also equivalent to len(self) + 8.

    If you need to inspect the full data of the underlying buffer, it can be
    retrieved as a bytes object using to_bytes().
    """

    __slots__ = ()
    _struct = Struct('<BBHHH')

    def __init__(self, bmRequestType: int = 0, bRequestCode: int = 0, wValue: int = 0, wIndex: int = 0, data: int | collections.abc.Buffer = None):
        if isinstance(data, int) or data is None:
            wLength = data or 0
            self._buffer = bytearray(8 + wLength)
        else:
            with memoryview(data) as view:
                wLength = view.nbytes
                self._buffer = bytearray(8 + wLength)
                self._buffer[8:] = view

        self._struct.pack_into(self._buffer, 0, bmRequestType, bRequestCode,
                               wValue, wIndex, wLength)

        self._views = WeakValueDictionary()
        self._lock = threading.Lock()
        self._acquired = False

    def __buffer__(self, flags):
        with self._lock:
            if self._acquired:
                raise RuntimeError("operation forbidden on locked buffer")

            view = memoryview(self._buffer)[8:]
            self._views[id(view)] = view
            return view

    def _resize(self):
        self._buffer[6:8] = int.to_bytes(len(self._buffer) - 8, length=2,
                                         byteorder='little', signed=False)

    def _translate(self, key):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return slice(start + 8, stop + 8, step)
        elif isinstance(key, int):
            if -len(self) <= key < len(self):
                return (key % len(self)) + 8
            else:
                raise IndexError("buffer index out of range")
        else:
            raise TypeError(f"buffer indices must be integers or slices, not {key.__class__.__name__}")

    def __getitem__(self, key):
        return self._buffer[self._translate(key)]

    @TransferBuffer._modify
    def __setitem__(self, key, value):
        self._buffer[self._translate(key)] = value
        self._resize()

    @TransferBuffer._modify
    def __delitem__(self, key):
        del self._buffer[self._translate(key)]
        self._resize()

    def __len__(self):
        return len(self._buffer) - 8

    @TransferBuffer._modify
    def insert(self, index, item):
        self._buffer.insert(index + 8, item)
        self._resize()

    @TransferBuffer._modify
    def extend(self, iterable_of_ints):
        self._buffer.extend(iterable_of_ints)
        self._resize()

    @TransferBuffer._modify
    def clear(self, /):
        del self._buffer[8:]
        self._resize()

    def to_bytes(self) -> bytes:
        """
        Returns the full byte representation of the underlying buffer,
        including the control setup packet.
        """

        return bytes(self._buffer)

    def actual_length(self) -> int:
        """
        Returns the actual length of the underlying buffer, including the
        control setup packet.
        """

        return len(self._buffer)

    @property
    def bmRequestType(self) -> int:
        return self._buffer[0]

    @bmRequestType.setter
    @TransferBuffer._modify
    def bmRequestType(self, value: int):
        self._buffer[0] = value

    @property
    def bRequestCode(self) -> int:
        return self._buffer[1]

    @bRequestCode.setter
    @TransferBuffer._modify
    def bRequestCode(self, value: int):
        self._buffer[1] = value

    @property
    def wValue(self) -> int:
        return int.from_bytes(self._buffer[2:4], byteorder='little',
                              signed=False)

    @wValue.setter
    @TransferBuffer._modify
    def wValue(self, value: int):
        self._buffer[2:4] = int.to_bytes(value, length=2, byteorder='little',
                                         signed=False)

    @property
    def wIndex(self) -> int:
        return int.from_bytes(self._buffer[4:6], byteorder='little',
                              signed=False)

    @wIndex.setter
    @TransferBuffer._modify
    def wIndex(self, value: int):
        self._buffer[4:6] = int.to_bytes(value, length=2, byteorder='little',
                                         signed=False)

    @property
    def wLength(self) -> int:
        return int.from_bytes(self._buffer[6:8], byteorder='little',
                              signed=False)



class TransferType(Enum):
    """An enum representing the transfer type."""
    CONTROL =     _libusb.LIBUSB_TRANSFER_TYPE_CONTROL      # 0
    ISOCHRONOUS = _libusb.LIBUSB_TRANSFER_TYPE_ISOCHRONOUS  # 1
    BULK =        _libusb.LIBUSB_TRANSFER_TYPE_BULK         # 2
    INTERRUPT =   _libusb.LIBUSB_TRANSFER_TYPE_INTERRUPT    # 3
    BULK_STREAM = _libusb.LIBUSB_TRANSFER_TYPE_BULK_STREAM  # 4



class TransferStatus(Enum):
    """An enum representing the transfer status."""

    # These copy the libusb transfer status values to simplify translation.
    COMPLETED = _libusb.LIBUSB_TRANSFER_COMPLETED # 0
    ERROR =     _libusb.LIBUSB_TRANSFER_ERROR     # 1
    TIMED_OUT = _libusb.LIBUSB_TRANSFER_TIMED_OUT # 2
    CANCELLED = _libusb.LIBUSB_TRANSFER_CANCELLED # 3
    STALL =     _libusb.LIBUSB_TRANSFER_STALL     # 4
    NO_DEVICE = _libusb.LIBUSB_TRANSFER_NO_DEVICE # 5
    OVERFLOW =  _libusb.LIBUSB_TRANSFER_OVERFLOW  # 6

    # We can then just use auto() for our additional values.
    PENDING =   auto()
    NEW =       auto()
    FREED =     auto()



class TransferFlag(Flag):
    """
    Flags to modify the behavior of transfers.

    SHORT_NOT_OK:
        Report short frames as errors. See libusb_transfer.flags.
    """

    SHORT_NOT_OK = auto()



class _TransferState(Flag):
    SUBMITTED = auto()
    PENDING = auto()



class Transfer:
    """
    The base class for asynchronous USB communication.

    Creating, modifying, submitting, and cancelling transfers may be done
    from any thread.

    Unlike in libusb, transfer lifecycles are bound to their DeviceHandle.
    Transfer instances are freed when the DeviceHandle they were created
    from closes (or when garbage collected). Freed transfers cannot be
    resubmitted or otherwise modified. Most properties are no longer
    available once freed, and will instead return None, with the exception
    of status, which becomes TransferStatus.FREED.
    """

    __slots__ = ('__weakref__', '_buffer', '_dev_handle', '_waiters', '_flags',
                 '_free_obj', '_lock', '_state', '_transfer', '_callback',
                 '_callback_loop')

    def __init__(self, dev_handle: DeviceHandle, /, iso_packets: int = 0):
        # Allocate a transfer.
        transfer_ptr = _libusb.libusb_alloc_transfer(iso_packets)
        if not transfer_ptr:
            raise RuntimeError("failed to allocate transfer")

        # Create a finalizer to free the transfer on garbage collect
        # or whenever freed explicitly.
        self._free_obj = finalize(self, _libusb.libusb_free_transfer,
                                  transfer_ptr)

        self._lock = threading.Lock()
        self._transfer = transfer_ptr.contents
        self._state = _TransferState(0)
        self._buffer = None
        self._callback = None
        self._callback_loop = None
        self._flags = TransferFlag(0)
        self._waiters = deque()

        # The underlying callback invoked by libusb. This will be executed
        # from the Context's event loop thread.
        @_libusb.libusb_transfer_cb_fn
        def callback(_, selfref = ref(self)):
            # This prevents the finalizer from keeping the instance alive.
            self = selfref()
            assert self is not None, "failed to obtain reference to self"

            # Release the lock held on the buffer.
            if self._buffer is not None:
                self._transfer.buffer = None
                self._transfer.length = 0
                self._buffer._release()

            # Update state and remove from pending collection.
            self._state &= ~_TransferState.PENDING
            self._dev_handle._pending.remove(self)

            ctx_loop = self._dev_handle._context._loop

            # Schedule the callback to execute (in the given loop).
            if self._callback is not None:
                if self._callback_loop is None:
                    ctx_loop.call_soon(self._callback, self)
                else:
                    self._callback_loop.call_soon_threadsafe(self._callback,
                                                             self)

            # The function used to set a future in a loop using
            # loop.call_soon_threadsafe.
            def set_future(future):
                if not future.done():
                    future.set_result(True)

            # Notify waiters (across threads).
            with self._lock:
                for future in self._waiters:
                    loop = future.get_loop()
                    if loop is ctx_loop:
                        set_future(future)
                    else:
                        loop.call_soon_threadsafe(set_future, future)

        self._transfer.callback = callback

        # Set and register self to the DeviceHandle. This should be at the
        # end in case the DeviceHandle closed during init to ensure we don't
        # have partially populated transfers attached to closed handles.
        # Alternatively, we could acquire the lock across the init block.
        self._dev_handle = dev_handle
        self._transfer.dev_handle = dev_handle._obj
        try:
            dev_handle._register_transfer(self)
        except:
            self._free()
            raise


    def __bool__(self):
        """
        Return bool(self).
        True if the transfer has not been freed.
        """
        return hasattr(self, '_transfer')


    @staticmethod
    def _none_if_freed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, '_transfer'):
                return func(self, *args, **kwargs)
            else:
                return None
        return wrapper

    @staticmethod
    def _acquire(func):
        """
        A decorator to prevent modification of a pending or freed transfer.
        Also acquires a lock.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with self._lock:
                if not self:
                    raise RuntimeError("operation forbidden on freed Transfer object")
                if _TransferState.PENDING in self._state:
                    raise RuntimeError("operation forbidden on pending Transfer object")
                return func(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def _permanent(func):
        """
        A decorator to prevent modification of certain properties on a
        previously submitted transfer. Also acquires a lock.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with self._lock:
                if not self:
                    raise RuntimeError("operation forbidden on freed Transfer object")
                if _TransferState.SUBMITTED in self._state:
                    raise RuntimeError(f"can't modify {func.__name__} property of submitted Transfer object")
                return func(self, *args, **kwargs)
        return wrapper


    @_acquire
    def submit(self):
        """
        Submit the transfer to the device.
        Cannot be called on a pending transfer.
        """

        # Acquire the lock on the handle to lock its state and make sure it
        # doesn't close during submission.
        with self._dev_handle._lock:
            if not self._dev_handle:
                raise RuntimeError("cannot submit transfer to closed DeviceHandle")

            # Set the SHORT_NOT_OK flag of the underlying transfer.
            if TransferFlag.SHORT_NOT_OK in self._flags:
                self._transfer.flags |= _libusb.LIBUSB_TRANSFER_SHORT_NOT_OK
            else:
                self._transfer.flags &= ~_libusb.LIBUSB_TRANSFER_SHORT_NOT_OK

            # Acquire a lock on the buffer.
            if self._buffer is not None:
                length, buffer = self._buffer._acquire()
                self._transfer.buffer = buffer
                self._transfer.length = length

            # Reset the transfer status and submit.
            self._transfer.status = 0
            _catch( _libusb.libusb_submit_transfer(byref(self._transfer)) )

            # Update the state of the transfer and add it to the collection of
            # pending transfers.
            self._state |= _TransferState.SUBMITTED | _TransferState.PENDING
            self._dev_handle._pending.add(self)


    @_none_if_freed
    def cancel(self):
        """
        Cancel the transfer. Does nothing if the transfer is not pending.

        It is possible for the finished transfer status to evaluate to a
        value other than CANCELLED (e.g. TIMED_OUT) even if explicitly
        cancelled, simply depending on event order.

        Thread-safe.
        """

        # Acquire the lock to ensure the transfer isn't freed during
        # cancellation.
        with self._lock:
            if _TransferState.PENDING in self._state:
                match _libusb.libusb_cancel_transfer(byref(self._transfer)):
                    case int(_libusb.LIBUSB_SUCCESS):
                        pass
                    case int(_libusb.LIBUSB_ERROR_NOT_FOUND):
                        pass
                    case err:
                        raise _error(err)


    async def wait(self):
        """
        Wait for the transfer to complete or cancel.

        Thread-safe.
        """

        # Acquire the lock to ensure the future and state are synced, and
        # that _waiters isn't being modified in two places at once.
        with self._lock:
            if not _TransferState.PENDING in self._state:
                return True

            future = asyncio.get_event_loop().create_future()
            self._waiters.append(future)

        # Drop lock to await without deadlocking single-threads.
        try:
            await future
            return True
        finally:
            with self._lock:
                self._waiters.remove(future)


    def _free(self):
        # Acquire the lock so we can safely free resources.
        with self._lock:
            # This is an assert, because it should never happen if the
            # library has been written correctly.
            assert _TransferState.PENDING not in self._state, "_free called on pending transfer"

            del self._transfer
            del self._buffer
            del self._flags
            del self._callback
            del self._callback_loop
            del self._dev_handle

            self._state = _TransferState(0)

            # Call the finalizer to free the underlying transfer.
            self._free_obj()
            del self._free_obj


    @_acquire
    def set_callback(self, callback: Callable[['Transfer'], None], loop = None):
        """
        Set the callback function to be invoked on completion. Optionally
        provide a loop to execute the callback from; defaults to the
        Context's event loop.

        The callback will execute regardless of the resulting status, even
        if explicitly cancelled.

        Loop should be an async loop that supports call_soon_threadsafe.
        """

        self._callback = callback
        self._callback_loop = loop


    @property
    @_none_if_freed
    def dev_handle(self) -> DeviceHandle:
        """DeviceHandle of the device that this transfer will be submitted to."""
        return self._dev_handle


    @property
    @_none_if_freed
    def endpoint(self) -> int:
        """
        The address of the endpoint that this transfer will be submitted to.

        If the transfer has been previously submitted (has any status other
        than TransferStatus.NEW), attempting to change this will raise
        a RuntimeError.
        """
        return self._transfer.endpoint

    @endpoint.setter
    @_permanent
    def endpoint(self, value: int | Endpoint):
        self._transfer.endpoint = int(value)


    @property
    @_none_if_freed
    def type(self) -> TransferType:
        """
        A TransferType value indicating the transfer type.

        If the transfer has been previously submitted (has any status other
        than TransferStatus.NEW), attempting to change this will raise
        a RuntimeError.
        """
        return TransferType(self._transfer.type)

    @type.setter
    @_permanent
    def type(self, value: TransferType):
        if isinstance(value, TransferType):
            self._transfer.type = value.value
        else:
            self._transfer.type = value


    @property
    @_none_if_freed
    def timeout(self) -> int:
        """
        The timeout for this transfer in milliseconds, 0 for no timeout.

        The transfer will finish with a status of TransferStatus.TIMED_OUT
        once this timeout is reached. Some data may still have transfered.
        """
        return self._transfer.timeout

    @timeout.setter
    @_acquire
    def timeout(self, value: int):
        self._transfer.timeout = value


    @property
    @_none_if_freed
    def flags(self) -> TransferFlag:
        """A combination of TransferFlag values."""
        return self._flags

    @flags.setter
    @_acquire
    def flags(self, value: int | TransferFlag):
        if isinstance(value, int):
            self._flags = TransferFlag(value)
        elif isinstance(value, TransferFlag):
            self._flags = value
        else:
            raise TypeError("flags must be an int or TransferFlag instance")


    @property
    @_none_if_freed
    def buffer(self) -> TransferBuffer:
        """A TransferBuffer containing the data to send."""
        return self._buffer

    @buffer.setter
    @_acquire
    def buffer(self, value: TransferBuffer):
        if not isinstance(value, TransferBuffer) and value is not None:
            raise TypeError("buffer must be a TransferBuffer object or None")

        self._buffer = value

    @buffer.deleter
    @_acquire
    def buffer(self):
        self._buffer = None


    @property
    @_none_if_freed
    def transferred(self) -> int:
        """The actual length of the data that was transferred."""
        return self._transfer.actual_length


    @property
    def status(self) -> TransferStatus:
        """A TransferStatus value indicating the status of the transfer."""

        if not hasattr(self, '_transfer'):
            return TransferStatus.FREED
        elif _TransferState.PENDING in self._state:
            return TransferStatus.PENDING
        elif _TransferState.SUBMITTED not in self._state:
            return TransferStatus.NEW
        else:
            return TransferStatus(self._transfer.status)



# A reusable zero timeval.
_tv_zero = _libusb.struct_timeval()

class Context:
    """
    The context that all operations will be run under.
    I/O events are handled in the current/given event loop. Not thread-safe,
    except where otherwise noted.

    Setting the no_discovery option will disable scanning for devices during
    context initialization/entry.

    Context instances are single-entry.
    """

    __slots__ = ('_obj', '_loop', '_timed_events', '_devices', '_pollfds',
                 '_pollfd_added_cb', '_pollfd_removed_cb', '_opts', '_lock')

    def __init__(self, *, loop: asyncio.AbstractEventLoop = None,
                 no_discovery: bool = False):

        self._loop = loop or asyncio.get_event_loop()
        self._lock = threading.Lock()
        self._obj = POINTER(_libusb.struct_libusb_context)()
        self._devices = WeakValueDictionary()
        self._pollfds = set()

        # Parse libusb context options.
        opts = []

        if no_discovery:
            if _libusb_version < 0x10000001b0000: # 1.0.27
                raise NotSupportedError(f"no_discovery option requires libusb version ≥ 1.0.27, found {_libusb_version_string}")
            opts.append(_libusb.libusb_init_option(
                option=_libusb.LIBUSB_OPTION_NO_DEVICE_DISCOVERY))

        self._opts = (_libusb.libusb_init_option * len(opts))(*opts)

        # Create the pollfd notifier C callbacks. We have to set them as
        # attributes to prevent premature garbage collection.
        self._pollfd_added_cb = _libusb.libusb_pollfd_added_cb(
                self.__set_pollfd)
        self._pollfd_removed_cb = _libusb.libusb_pollfd_removed_cb(
                lambda fd, user_data: self.__set_pollfd(fd, 0, user_data))

    def __handle_events(self):
        _catch( _libusb.libusb_handle_events_timeout(self._obj, _tv_zero) )

    def __enter__(self):
        # Ensure this context hasn't been previously entered or used.
        if getattr(self, '_obj', True):
            raise RuntimeError("cannot reenter single-use Context instance")

        # Inititalize the underlying context (with options).
        if _libusb_version >= 0x10000001b0000:   # 1.0.27
            _catch( _libusb.libusb_init_context(byref(self._obj),
                                                self._opts, len(self._opts)) )
        else:
            _catch( _libusb.libusb_init(byref(self._obj)) )

        # Detect if we need to take timeouts into consideration while
        # polling file descriptors.
        if not _libusb.libusb_pollfds_handle_timeouts(self._obj):
            # Create the timeval here to make it reusable.
            tv = _libusb.struct_timeval()

            def handle_events_timed():
                def recurse():
                    self.__handle_events()
                    handle_events_timed()

                # Get next timeout, in seconds.
                _catch( _libusb.libusb_get_next_timeout(self._obj, tv) )
                timeout = tv.tv_sec + tv.tv_usec / 1000000

                # Schedule next call, and save the TimerHandle to allow for
                # cancellation (when the user exits the context).
                self._timed_events = self._loop.call_later(timeout, recurse)

            handle_events_timed()

        # Get current pollfds for the context.
        pollfds = _libusb.libusb_get_pollfds(self._obj)
        try:
            for ptr in takewhile(bool, pollfds):
                # Register the pollfds using our logic.
                self.__set_pollfd(ptr.contents.fd, ptr.contents.events)
        finally:
            _libusb.libusb_free_pollfds(pollfds)

        # Set callbacks for pollfd changes.
        _libusb.libusb_set_pollfd_notifiers(self._obj,
                                    self._pollfd_added_cb,
                                    self._pollfd_removed_cb,
                                    None)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Finalize device references.
        for device in self._devices.values():
            device._unref()
        self._devices.clear()

        # Unset pollfd callbacks.
        _libusb.libusb_set_pollfd_notifiers(self._obj,
                                    _libusb.libusb_pollfd_added_cb(0),
                                    _libusb.libusb_pollfd_removed_cb(0),
                                    None)

        # Unregister all pollfds.
        for fd in list(self._pollfds):
            self.__set_pollfd(fd, 0)

        # Cancel timed events (if scheduled).
        if hasattr(self, '_timed_events'):
            self._timed_events.cancel()

        # Close the libusb_context.
        _libusb.libusb_exit(self._obj)

        # Delete the context pointer to signify that this instance is no
        # longer usable.
        del self._obj

    def __bool__(self):
        return bool(getattr(self, '_obj', False))

    def __set_pollfd(self, fd, events, user_data = None):
        """
        Adds fd to the polling list to listen for events. If events is zero,
        removes fd from the polling list.
        """

        if events & select.POLLIN:
            self._loop.add_reader(fd, self.__handle_events)
        else:
            self._loop.remove_reader(fd)

        if events & select.POLLOUT:
            self._loop.add_writer(fd, self.__handle_events)
        else:
            self._loop.remove_writer(fd)

        if events & (select.POLLIN | select.POLLOUT):
            self._pollfds.add(fd)
        else:
            self._pollfds.discard(fd)

    @staticmethod
    def _in_context(func):
        """A decorator to "enforce" calling methods in a context."""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self:
                raise RuntimeError("method must be called within a context")
            return func(self, *args, **kwargs)
        return wrapper

    @_in_context
    def set_debug(self, log_level: LogLevel):
        """Set the log level of the underlying libusb_context."""

        if _libusb_version < 0x1000000160000: # 1.0.22
            _libusb.libusb_set_debug(self._obj, log_level)
        else:
            _libusb.libusb_set_option(self._obj, _libusb.LIBUSB_OPTION_LOG_LEVEL,
                                      log_level)

    @_in_context
    def get_device_list(self) -> list[Device]:
        """
        Get a list of Devices.

        Thread-safe.
        """

        # Get the device list.
        p_list = POINTER(POINTER(_libusb.libusb_device))()
        length = _catch( _libusb.libusb_get_device_list(self._obj, p_list) )

        try:
            # Cast device pointers into Device class.
            return [ Device(dev.contents, self) for dev in p_list[:length] ]
        finally:
            # Free the device list (and unref the devices, as they have been
            # referenced by the Device class).
            _libusb.libusb_free_device_list(p_list, True)

    @_in_context
    @asynccontextmanager
    async def wrap_sys_device(self, sys_dev: int) -> Generator[DeviceHandle, None, None]:
        """
        Open a DeviceHandle for I/O from a system device handle.

        This method is most useful in conjunction with setting the
        no_discovery option on the Context, for systems where the process
        might not have permission to access all devices, like Android.

        Closing the returned handle will not close the system handle.

        The device will also be added to the result of get_device_list for
        as long as the handle remains open.

        Device instances created for this handle (from
        DeviceHandle.get_device) should not be opened. Doing so will most
        likely raise an error, but could result in undefined behavior.

        Not thread-safe. Must be called from the same thread as the Context
        event loop.
        """

        if _libusb_version < 0x1000000170000: # 1.0.23
            raise NotSupportedError(f"wrap_sys_device requires libusb version ≥ 1.0.23, found {_libusb_version_string}")

        handle = DeviceHandle(self)
        _catch( _libusb.libusb_wrap_sys_device(self._obj, sys_dev,
                                               handle._obj) )
        try:
            close = handle._open(None)
        except:
            _libusb.libusb_close(handle._obj)
            raise

        try:
            yield handle
        finally:
            await asyncio.shield(close())





__all__ = [
    'get_libusb_version',
    'LogLevel',
    'USBClass',
    'RequestTypeFlags',
    'RequestTypeUnion',
    'RequestDirection',
    'RequestType',
    'RequestRecipient',
    'USBError',
    'IOError',
    'AccessError',
    'NoDeviceError',
    'NotFoundError',
    'ResourceBusyError',
    'OverflowError',
    'PipeError',
    'NotSupportedError',
    'EndpointDirection',
    'EndpointType',
    'Endpoint',
    'Interface',
    'Configuration',
    'DeviceHandle',
    'Speed',
    'Device',
    'TransferBuffer',
    'ControlTransferBuffer',
    'TransferType',
    'TransferStatus',
    'TransferFlag',
    'Transfer',
    'Context',
]
