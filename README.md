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

### Current Features:
  * async event handling
  * thread-safe transfer creation and submission
  * automated resource handling
  * Termux compatibility

###  Planned Features:
  * async endpoint read/write streams
