![wlansies](https://github.com/islandu/wlansies/blob/main/.github/images/mascot.png)

# wlansies
Scan for WiFi networks in your area with about $10 USD worth of hardware (Raspberry Pi Pico W, 16x2 LCD screen, rotary encoder).

## Installation
_Note: These instructions assume you have already flashed MicroPython firmware onto your Pico W_

To use the `deploy.sh` script in this repository, you will need to have `mpremote` installed.
```bash
python3 -m pip install mpremote
```

Connect the screen and encoder to the Pico W board, then connect the Pico W's serial port to your workstation. To smoke test the connection, make sure the character device appears in your file system.

```bash
ls -la /dev/ttyACM0
```

If the character device is visible, you're good to go. Now all you have to do is deploy the code.

```bash
./deploy.sh
```

## Debugging
To debug the device, first connect to the MicroPython REPL on your Pico W board.

```bash
mpremote repl
```

While connected to the MicroPython REPL, import the `main()` function and run it to view debug logs while the device is operating.


```python
>>> from main import main
>>> main()
```

