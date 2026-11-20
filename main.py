import platform

from gpiozero import LED, Device
from rich import print
from smbus2 import SMBus

print(f"[bold green]Python {platform.python_version()} on {platform.machine()}[/]")

led = LED(17)   # GPIO17, physical pin 11 - safe to drive with nothing attached
print(f"GPIO pin factory: {Device.pin_factory.__class__.__name__}")
led.blink(on_time=0.2, off_time=0.2, n=3, background=False)
print("GPIO17 toggled OK")

found = []
with SMBus(1) as bus:
    for addr in range(0x03, 0x78):
        try:
            bus.read_byte(addr)
            found.append(f"0x{addr:02x}")
        except OSError:
            pass
print(f"I2C bus 1 devices: {found or 'none'}")
