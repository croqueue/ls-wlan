from network import WLAN
from machine_i2c_lcd import I2cLcd
from rotary_irq_rp2 import RotaryIRQ
from models import WiFiNetwork
from views import ViewBase, NetworkListView, NetworkDetailsView, DataView, NETWORK_PROP_NAMES

class ControllerBase:
    def __init__(self, view: ViewBase, parent_ctl: 'ControllerBase' = None):
        self._view: ViewBase = view
        self._parent: 'ControllerBase' = parent_ctl
    
    def get_selected_controller(self) -> 'ControllerBase':
        global _RE
        is_child, view = self._view.get_selected_view()
        controller = self._get_child_controller(view) if is_child else self._parent
        # reset encoder range for next controller
        _RE.set(min_val=0, max_val=controller.option_count)
        return controller
    
    def _get_child_controller(self, view: ViewBase) -> 'ControllerBase':
        raise NotImplementedError
    
    @property
    def option(self) -> int:
        return self._view.option
    
    @option.setter
    def option(self, value: int) -> None:
        self._view.option = value
    
    @property
    def option_count(self) -> int:
        return self._view.option_count

    @property
    def view(self) -> ViewBase:
        return self._view

class NetworkListController(ControllerBase):
    def __init__(self, view: NetworkListView):
        super().__init__(view)
    
    def _get_child_controller(self, view: NetworkDetailsView) -> ControllerBase:
        return NetworkDetailsController(view, self)

class NetworkDetailsController(ControllerBase):
    def __init__(self, view: NetworkDetailsView, parent_ctl: NetworkListController):
        super().__init__(view, parent_ctl)
    
    def _get_child_controller(self, view: DataView) -> ControllerBase:
        return DataController(view, self)

class DataController(ControllerBase):
    def __init__(self, view: DataView, parent_ctl: NetworkDetailsController):
        super().__init__(view, parent_ctl)
    
    def _get_child_controller(self, view: DataView) -> ControllerBase:
        return self


_ACTIVE_CTL = None
_RE = None

def _re_listener():
    value = _RE.value()
    print(f'option: {value}')
    _ACTIVE_CTL.option = value
    # button listener will have to...
    # _ACTIVE_CTL = _ACTIVE_CTL.get_selected_controller()
    

class MainController:
    def __init__(self, lcd: I2cLcd, re: RotaryIRQ):
        global _RE
        global _ACTIVE_CTL

        self._lcd = lcd
        self._nic = WLAN(WLAN.IF_STA)
        self._nic.active(True)
        network_list = [WiFiNetwork(data) for data in self._nic.scan()]

        _RE = re
        _RE.add_listener(_re_listener)
        _RE.set(min_val=0, max_val=len(network_list))

        view = NetworkListView(self._lcd, network_list)
        _ACTIVE_CTL = NetworkListController(view)
    
    def event_loop(self) -> None:
        """"""
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self._teardown_peripherals()
            print('exiting gracefully')
        except Exception as e:
            self._teardown_peripherals()
            print('general failure')
            raise e
    
    def _teardown_peripherals(self) -> None:
        _RE.remove_listener(_re_listener)
        self._lcd.clear()
        self._lcd.blink_cursor_off()
        self._lcd.backlight_off()

