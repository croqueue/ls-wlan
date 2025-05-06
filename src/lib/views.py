from models import WiFiNetwork
from machine_i2c_lcd import I2cLcd

NETWORK_PROP_NAMES = const((
    'SSID',
    'HW ADDRESS',
    'CHANNEL',
    'RSSI',
    'SECURITY',
    'IS HIDDEN'
))

class ViewBase:
    def __init__(self, lcd: I2cLcd, options_list: list, parent_view = None):
        # Note: objects in options_list must have __str__() implemented
        if not isinstance(options_list, list):
            raise TypeError('options_list must have type list')
        if len(options_list) == 0:
            raise ValueError('options_list cannot be empty')
        
        self._lcd = lcd
        self._options = options_list
        self._current = 0
        self._page: int = 0
        self._parent = parent_view

        # render initial page
        self._lcd.putstr(str(self))

    def __str__(self) -> str:
        pos1 = self._page << 1
        pos2 = pos1 + 1
        line1 = self._option_view_str(pos1)        
        line2 = self._option_view_str(pos2)
        return f'{line1}{line2}'
    
    @property
    def current_opt(self) -> int:
        return self._current
    
    @current_opt.setter
    def current_opt(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError('value must have type int')
        # can equal N because N is BACK
        if value < 0 or value > len(self._options_list):
            raise ValueError('value must be >=0 and <= number of options')
        self._current = value

    def _update_ui(self, new_opt: int, old_opt: int) -> None:
        new_pg, old_pg = new_opt >> 1, old_opt >> 1

        row1 = self._page << 1
        row2 = row1 + 1

        if new_pg != old_pg:
            self._lcd.clear()
            self._lcd.putstr(self._option_view_str(row1))
            self._lcd.putstr(self._option_view_str(row2))
        
        self._lcd.move_to(1, new_opt & 1)
    
    @property
    def parent_view(self):
        return self._parent

    @property
    def page(self) -> int:
        return self._page
    
    @page.setter
    def page(self, value: int):
        if not isinstance(value, int):
            raise TypeError('value must have type int')
        
        opt_index = value << 1

        if opt_index < 0 or opt_index > len(self._options):
            raise IndexError('value out of range')
        
        self._page = value
    
    # HELPER METHODS

    def _option_view_str(self, pos: int) -> str:
        num_opts = len(self._options)
        if pos == num_opts:
            return '[ ] BACK        '
        elif pos == num_opts + 1:
            return ' ' * 16
        
        opt_name = str(self._options[pos])
        pad = ' ' * (12 - len(opt_name))
        return f'[ ] {opt_name[:12]}{pad}'

class MainView(ViewBase):
    def __init__(self, lcd: I2cLcd, network_list: list):
        super().__init__(lcd, network_list)

class NetworkDetailsView(ViewBase):
    def __init__(self, lcd: I2cLcd, parent_view: MainView, network_index: int):
        super().__init__(lcd, NETWORK_PROP_NAMES, parent_view)

class DataView(ViewBase):
    def __init__(self, lcd: I2cLcd, parent_view: NetworkDetailsView, data: str):
        super().__init__(lcd, [data[:16]], parent_view)




