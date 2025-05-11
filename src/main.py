from machine import I2C, Pin
from machine_i2c_lcd import I2cLcd
from rotary_irq_rp2 import RotaryIRQ
from controllers import MainController

def _boot_lcd() -> I2cLcd:
    """Bootstraps 16x2 LCD screen"""
    i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
    i2c_addr = i2c.scan()[0]
    lcd = I2cLcd(i2c, i2c_addr, 2, 16)
    # lcd.backlight_on()
    # lcd.show_cursor()
    # lcd.blink_cursor_on()
    return lcd

def _boot_rotary_encoder() -> RotaryIRQ:
    """Bootstraps rotary encoder for user controls"""
    return RotaryIRQ(15, 14, incr=1, range_mode=RotaryIRQ.RANGE_BOUNDED, reverse=True)

def main():
    # driver dependencies
    lcd = _boot_lcd()
    re = _boot_rotary_encoder()

    # inject dependencies into main controller
    controller = MainController(lcd, re)

    # run the event loop
    controller.event_loop()

if __name__ == '__main__':
    main()
