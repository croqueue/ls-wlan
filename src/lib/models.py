from binascii import hexlify

# [ ] 0123456789AB
# [ ] BA9876543210
# [ ] 6789AB012345
# [ ] REFRESH

# [ ] SSID
# [ ] CHANNEL
# [ ] RSSI
# [ ] SECURITY
# [ ] HIDDEN


class WiFiNetwork:
    def __init__(self, wlan_data: tuple):
        self._ssid: str = wlan_data[0].decode('utf-8')
        self._hw_addr: str = hexlify(wlan_data[1]).decode('utf-8')
        self._channel = wlan_data[2]
        self._rssi: int = wlan_data[3]
        self._security: str = _SECURITY_TABLE[wlan_data[4]]
        self._hidden: bool = wlan_data[5] == 1
    
    def __str__(self) -> str:
        return self._hw_addr
    
    @property
    def ssid(self) -> str:
        return self._ssid
    
    @property
    def hardware_address(self) -> str:
        return self._hw_addr
    
    @property
    def channel(self):
        return self._channel
    
    @property
    def rssi(self) -> int:
        return self._rssi
    
    @property
    def security_type(self) -> str:
        return self._security
    
    @property
    def is_hidden(self) -> bool:
        return self._hidden

_SECURITY_TABLE = [
    'None',
    'WEP',
    'WPA-PSK',
    'WPA2-PSK',
    'WPA/WPA2-PSK'
]
