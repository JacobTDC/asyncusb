# asyncusb

The goal of this library is to be an efficient and pythonic asynchronous usb library written in pure python.

Here's an example that sends some data to a predetermined device endpoint.

```python
import asyncio
from asyncusb.core import *

async def main():
    with Context() as ctx:
        devices = ctx.get_device_list()

        # Inspect device attributes and choose a device. We'll just take the
        # first device for the purposes of this example.
        dev = devices[0]

        async with dev.open() as handle:
            # Handle kernel drivers automatically.
            handle.set_auto_detach_kernel_driver(True)

            # Claim the interface for the duration of this with block. This
            # example assumes we're using interface 1.
            with handle.bind_interface(1):
                # Create and submit the transfer. This example assumes
                # we're just sending some data to endpoint 0x02.
                transfer = handle.fill_bulk_transfer(0x02, b'hello world!')
                transfer.submit()

                # Wait for transfer completion. If we don't, the dev.open()
                # context manager might cancel our transfer before it
                # finishes!
                await transfer.wait()

asyncio.run(main())
```

That's it! No manual resouce cleanup is required, as all cleanup is handled by the context managers.

## Built-in Termux Compatibility

There are two built-in methods for accessing devices on Termux. The simplest method is using the `termux_compatibility_hook` method from the compat module, like so:

```python
dev_path = "/dev/bus/usb/001/002"

# This function gets the device from Termux:API and sets the TERMUX_USB_FD
# environment variable for the Termux patch of libusb.
termux_compatibility_hook(dev_path)

# Then use the context as normal.
with Context() as ctx:
    devices = ctx.get_device_list()

    # ...
```

This only allows using one device per Context, however. For more advanced cases, `termux_get_device` and `Context.wrap_sys_device` can be used, in conjunction with the `no_discovery` context option, like so:

```python
dev_path = "/dev/bus/usb/001/002"

# Get the system device handle (a file descriptor) from Termux:API.
sys_dev = termux_get_device(dev_path)

# Create a context with the 'no_discovery' option. This creates the context
# without searching for devices. This also means that ctx.get_device_list()
# will return an empty list.
with Context(no_discovery=True) as ctx:

    # Open the device.
    async with ctx.wrap_sys_device(sys_dev) as handle:

        # Get a Device instance, if needed.
        dev = handle.get_device()

        # ...
```

These methods aren't just limited to this library. `termux_compatibility_hook` will work for any library that uses libusb, and `termux_get_device` will work for any library that implements a way to call `libusb_wrap_sys_device`.

The compat module also provides other functions, such as `is_termux()`, `has_termux_api()`, and `termux_list_devices()`.

---

### Current Features:
  * async event handling
  * thread-safe transfer creation and submission
  * automated resource handling
  * Termux compatibility

###  Planned Features:
  * async endpoint read/write streams
