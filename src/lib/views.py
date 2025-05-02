from typing import Any, List
from models import WiFiNetwork, WiFiNetworkCache

class ViewBase:
    def __init__(self, options_list: List[Any]):
        # Note: objects in options_list must have __str__() implemented
        if not isinstance(options_list, list):
            raise TypeError('options_list must have type list')
        if len(options_list) == 0:
            raise ValueError('options_list cannot be empty')
        
        self._options: List[Any] = options_list
        self._pos: int = 0

    @property
    def current_option_page(self) -> str:
        if self._pos & 1:
            # render pos-1 and pos
            prev = str(self._options[self._pos - 1])
            current = str(self._options[self._pos])
            return f'{prev}{current}'
        
        # render pos and pos+1 (if present)
        if self._pos + 1 == len(self._options):
            current = str(self._options[self._pos])
            filler = ' ' * 16
            return f'{current}{filler}'
        
        
        current = str(self._options[self._pos])
        next = str(self._options[self._pos + 1])
        return f'{current}{next}'


    @property
    def position(self) -> int:
        return self._pos
    
    @position.setter
    def position(self, pos: int):
        if not isinstance(pos, int):
            raise TypeError('pos must have type int')
        if pos >= len(self._options) or pos < 0:
            raise IndexError('pos is out of range')

        self._pos = pos
    
    # HELPER METHODS

    def _option_view_str(self, pos: int) -> str:
        f"[ ] {str(self._options[pos])[:12]}"


class MainView(ViewBase):
    pass

class NetworkDetailsView(ViewBase):
    pass

class DataView(ViewBase):
    pass




