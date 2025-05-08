from network import WLAN
from utime import sleep_ms
from machine_i2c_lcd import I2cLcd
from rotary_irq_rp2 import RotaryIRQ
from models import WiFiNetwork
from views import ViewBase, MainView, NetworkDetailsView, DataView, NETWORK_PROP_NAMES
from network import WLAN

# _NETWORK_PROP_MAP = {nm: i for i, nm in enumerate(NETWORK_PROP_NAMES)}

class ControllerBase:
    def __init__(self, lcd: I2cLcd):
        self._lcd = lcd
    
    def increment_opt(self) -> None:
        self._view.current_opt += 1
    
    def decrement_opt(self) -> None:
        self._view.current_opt -= 1

class MainController(ControllerBase):
    def __init__(self, lcd: I2cLcd, network_list: list):
        super().__init__(lcd)
        self._view = MainView(self._lcd, network_list)

class NetworkDetailsController(ControllerBase):
    def __init__(self, view: NetworkDetailsView, lcd: I2cLcd):
        super().__init__(view, lcd)

class DataController(ControllerBase):
    def __init__(self, view: DataView, lcd: I2cLcd):
        super().__init__(view, lcd)

_ACTIVE_CTL = None
_RE_LAST_VAL: int = 0
_RE = None

def _re_listener():
    value = _RE.value()
    if value - _RE_LAST_VAL > 0:
        _ACTIVE_CTL.increment_opt()
    else:
        _ACTIVE_CTL.decrement_opt()
    
    _RE_LAST_VAL = value

class UserController:
    def __init__(self, lcd: I2cLcd, re: RotaryIRQ):
        self._lcd = lcd

        self._nic = WLAN(WLAN.IF_STA)
        self._nic.active(True)
        network_list = self._nic.scan()

        _RE = re
        _RE.add_listener(_re_listener)
        _RE.set(min_val=0,
                max_val=len(network_list) - 1,
                incr=1,
                range_mode=RotaryIRQ.RANGE_BOUNDED)
        
        _ACTIVE_CTL = MainController(self._lcd, network_list)





class DeviceController:
    """Main controller for the device, only one instance may exist"""
    _active_view = None
    _singleton = None

    def __init__(self, lcd: I2cLcd, re: RotaryIRQ, nic: WLAN):
        if DeviceController._singleton is not None:
            raise RuntimeError('see DeviceController usage')
        
        self._lcd: I2cLcd = lcd
        self._re: RotaryIRQ = re
        self._nic: WLAN = nic
        DeviceController._singleton = self
        # self._re.add_listener()

    def scan_for_networks(self):
        self._lcd.clear()
        # self._lcd.hide_cursor()
        line1 = '*** SCANNING ***'
        line2 = '***** AREA *****'

        for c in f'{line1}{line2}':
            self._lcd.putchar(c)
            sleep_ms(16)
        
        # sleep_ms(512)

        


        # self._lcd.putstr(f'{line1}{line2}')
        wlan_data = self._nic.scan()

        line1 = "we're in...     "
        line2 = '**** FOUND! ****'

        

        networks = [WiFiNetwork(n) for n in wlan_data]
        self._active_view = MainView(self._lcd, networks)

        for row in reversed(range(2)):
            for column in reversed(range(16)):
                self._lcd.move_to(column, row)
                self._lcd.putchar(' ')
                sleep_ms(8)
        
        self._lcd.clear()

        for c in "we're in . . .  ":
            self._lcd.putchar(c)
            sleep_ms(128)
        
        # sleep_ms(256)

        self._lcd.clear()
        self._lcd.putstr(str(self._active_view))
        self._lcd.move_to(1, 0)
    


