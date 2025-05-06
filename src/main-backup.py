import binascii
import network
import utime
import machine
from machine_i2c_lcd import I2cLcd
from rotary_irq_rp2 import RotaryIRQ

rotary_encoder = rotary_encoder = RotaryIRQ(
    15,     # clock pin
    14,     # data pin
    min_val=0,
    max_val=31,
    incr=1,
    reverse=True,
    range_mode=RotaryIRQ.RANGE_WRAP, # RANGE_UNBOUNDED and RANGE_BOUNDED
    pull_up=False,
    half_step=False,
    invert=False    
)

def boot_lcd() -> I2cLcd:
    """Brings the LCD screen online"""
    i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=400000)
    i2c_addr = i2c.scan()[0]
    return I2cLcd(i2c, i2c_addr, 2, 16)

lcd_screen = boot_lcd()

def on_encoder_pos_change():
    index = rotary_encoder.value()
    print(f'encoder val: {index}')
    x, y = index & 15, index >> 4
    lcd_screen.move_to(x, y)


def main() -> None:
    lcd_screen.backlight_on()
    lcd_screen.show_cursor()
    lcd_screen.blink_cursor_on()
    rotary_encoder.add_listener(on_encoder_pos_change)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        rotary_encoder.remove_listener(on_encoder_pos_change)
        lcd_screen.blink_cursor_off()
        lcd_screen.hide_cursor()
        lcd_screen.backlight_off()
    
    print('we done here')



def boot_nic(lcd: I2cLcd) -> network.WLAN:
    """Brings up the network interface"""
    lcd.clear()
    lcd.putstr('booting nic...\n')
    nic = network.WLAN(network.WLAN.IF_STA)
    nic.active(True)
    lcd.putstr('Success!')
    return nic

def scan_for_networks(nic: network.WLAN, lcd: I2cLcd) -> list:
    """Returns list of Wi-Fi networks in range"""
    networks = []
    
    try:
        lcd.clear()
        lcd.putstr('initWiFiScan... ')
        networks = nic.scan()
    except Exception as e:
        print('wlan scan error!')
        raise e
    
    utime.sleep_ms(1024)
    lcd.putstr("oOohH gOt SoMe!!")
    utime.sleep_ms(1024)
    return networks

def show_networks(networks: list, lcd: I2cLcd) -> None:
    """Pages through discovered Wi-Fi networks on the LCD screen"""
    for net_info in networks:        
        ssid = net_info[0].decode('ascii')
        bssid = binascii.hexlify(net_info[1]).decode('ascii').upper()
        lcd.clear()
        lcd.putstr(f'[{bssid}]  ')
        lcd.putstr(f'{ssid:<16}')
        utime.sleep_ms(1024)

# if __name__ == '__main__':
#     # Bootstrap LCD screen and network interface card
#     lcd = boot_lcd()
#     nic = boot_nic(lcd)
    
#     # Infinite loop (scan/show)
#     while True:
#         networks = scan_for_networks(nic, lcd)
#         show_networks(networks, lcd)
#         lcd.clear()
#         lcd.putstr('aLl DoNe???     ')
#         utime.sleep_ms(1024)
#         lcd.putstr('again!!!')
#         utime.sleep_ms(1024)

if __name__ == '__main__':
    main()
