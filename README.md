# pi4-hw-smoketest

Quick smoke test for Python hardware access on a Raspberry Pi 4: confirms the venv, a PyPI package, GPIO (gpiozero + lgpio) and the I2C bus all work without sudo.

## What it does

1. Prints the Python version and architecture
2. Reports the gpiozero pin factory (expected: `LGPIOFactory`)
3. Blinks GPIO17 (physical pin 11) three times
4. Scans I2C bus 1 and lists any device addresses found

## Requirements

- Raspberry Pi OS Trixie (Python 3.13)
- I2C enabled: `sudo raspi-config nonint do_i2c 0`, then reboot
- User in the `gpio` and `i2c` groups
- Hardware libraries from apt (not pip):

```
sudo apt install -y python3-venv i2c-tools python3-gpiozero python3-lgpio python3-smbus2
```

- [uv](https://docs.astral.sh/uv/)

## Run

The venv must include system site-packages so it can see the apt-installed GPIO/I2C libraries:

```
uv venv --system-site-packages
uv sync
uv run main.py
```

Example output with nothing wired:

```
Python 3.13.5 on aarch64
GPIO pin factory: LGPIOFactory
GPIO17 toggled OK
I2C bus 1 devices: none
```

## Wiring notes

- GPIO is 3.3 V and **not** 5 V tolerant – check breakout boards' pull-up voltage
- I2C bus 1: pin 3 = SDA (GPIO2), pin 5 = SCL (GPIO3); the Pi has on-board 1.8 kΩ pull-ups
- An LED on GPIO17 needs a series resistor (e.g. 330 Ω) to GND

## Troubleshooting

- `No module named gpiozero` – venv created without `--system-site-packages`
- Permission denied on `/dev/gpiochip0` or `/dev/i2c-1` – check `groups`, log out and back in
- `/dev/i2c-1` missing – enable I2C and reboot
