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
        
        self._lcd: I2cLcd = lcd
        self._options: list = options_list
        self._current: int = 0
        self._parent: 'ViewBase' = parent_view
        self._back_label: str = ''

        # render initial page
        
        self._lcd.backlight_on()
        self._lcd.putstr(str(self))
        self._lcd.move_to(1, 0)
        self._lcd.show_cursor()
        self._lcd.blink_cursor_on()

    def __str__(self) -> str:
        page = self._current >> 1
        pos1 = page << 1
        pos2 = pos1 + 1
        line1 = self._option_view_str(pos1)        
        line2 = self._option_view_str(pos2)
        return f'{line1}{line2}'
    
    def get_selected_view(self) -> tuple[bool, 'ViewBase']:
        # 'BACK' selected
        if self._current == len(self._options):
            return False, self._parent
        
        return True, self._get_child_view()
    
    @property
    def option(self) -> int:
        return self._current
    
    @option.setter
    def option(self, value: int) -> None:
        self._update_ui(value, self._current)
        self._current = value
    
    @property
    def option_count(self) -> int:
        return len(self._options)

    @property
    def parent_view(self):
        return self._parent
    
    # HELPER METHODS

    def _get_child_view(self) -> 'ViewBase':
        raise NotImplementedError

    def _update_ui(self, new_opt: int, old_opt: int) -> None:
        new_pg, old_pg = new_opt >> 1, old_opt >> 1

        row1 = new_pg << 1
        row2 = row1 + 1

        if new_pg != old_pg:
            self._lcd.clear()
            self._lcd.putstr(self._option_view_str(row1))
            self._lcd.putstr(self._option_view_str(row2))
        
        self._lcd.move_to(1, new_opt & 1)

    def _option_view_str(self, pos: int) -> str:
        num_opts = len(self._options)
        if pos == num_opts:
            pad = ' ' * (12 - len(self._back_label[:12]))
            return f'[ ] {self._back_label[:12]}{pad}'
        elif pos == num_opts + 1:
            return ' ' * 16
        
        opt_name = str(self._options[pos])
        pad = ' ' * (12 - len(opt_name[:12]))
        return f'[ ] {opt_name[:12]}{pad}'

class NetworkListView(ViewBase):
    def __init__(self, lcd: I2cLcd, network_list: list):
        super().__init__(lcd, network_list)
        self._back_label = 'RE-SCAN'
    
    def _get_child_view(self) -> ViewBase:
        return NetworkDetailsView(self._lcd, self, self._current)

class NetworkDetailsView(ViewBase):
    def __init__(self, lcd: I2cLcd, parent_view: NetworkListView, network_index: int):
        super().__init__(lcd, NETWORK_PROP_NAMES, parent_view)
        self._details: WiFiNetwork = parent_view._options[network_index].data
    
    def _get_child_view(self) -> ViewBase:
        return DataView(self._lcd, self, self._details[self._current])

class DataView(ViewBase):
    def __init__(self, lcd: I2cLcd, parent_view: NetworkDetailsView, data: str):
        super().__init__(lcd, [data[:16]], parent_view)
    
    def _get_child_view(self):
        return self
