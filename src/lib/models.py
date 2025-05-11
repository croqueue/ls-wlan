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
        self._hw_addr: str = hexlify(wlan_data[1]).decode('utf-8').upper()
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
    
    @property
    def data(self) -> tuple:
        return (
            ('SSID', self._ssid),
            ('HW ADDRESS', self._hw_addr),
            ('CHANNEL', self._channel),
            ('RSSI', self._rssi),
            ('SECURITY', self._security),
            ('HIDDEN?', str(self._hidden))
        )

class WiFiNetworkCache:
    def __init__(self, wlan_data_list: list):
        self._table = [WiFiNetwork(n) for n in wlan_data_list]
    
    def __len__(self) -> int:
        return len(self._table)
    
    def __getitem__(self, i: int) -> WiFiNetwork:
        return self._table[i]

    def addresses(self):
        for n in self._table:
            yield str(n)




# STATIC DATA

# _SECURITY_TABLE = (
#     'None',
#     'WEP',
#     'WPA-PSK',
#     'WPA2-PSK',
#     'WPA/WPA2-PSK',
#     'IDK'
# )

_SECURITY_TABLE = (
    'Open',     # 0
    'WEP',  # 1
    'WPA',      # 2
    'WPA + WEP',         # 3
    'WPA2',         # 4
    'WPA2 + WEP',         # 5
    'WPA/WPA2',         # 6
    'WPA/WPA2 + WEP',         # 7
)