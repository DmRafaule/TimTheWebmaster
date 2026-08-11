import random
from time import time
from typing import List, Literal


class Proxy:
    """container for a proxy"""

    def __init__(self, ip, type_="datacenter", protocol_="http", status_="unchecked", weight_=1000) -> None:
        self.ip: str = ip
        self.weight = weight_
        self.protocol: Literal["http", "https", "socks4", "socks5"] = protocol_
        self.type: Literal["datacenter", "residential", "isp", "mobile"] = type_
        self.status: Literal["alive", "unchecked", "dead"] = status_
        _, _, self.subnet, self.host = ip.split(":")[0].split('.')
        self.port = ip.split(":")[1]
        self.last_used: int = None

    def __repr__(self) -> str:
        return self.ip

    def __str__(self) -> str:
        return self.ip


class Rotator:
    """weighted random proxy rotator"""

    def __init__(self, proxies: List[Proxy]):
        self.proxies = proxies
        self._last_subnet = None

    def _weigh_proxy(self, proxy: Proxy):

        proxy.weight = 1000

        if proxy.subnet == self._last_subnet:
            proxy.weight -= 500
        
        match(proxy.status):
            case "alive":
                proxy.weight += 100
            case "dead":
                proxy.weight -= 300
            case "unchecked":
                proxy.weight += 200

        match(proxy.type):
            case "residential":
                proxy.weight += 250
            case "datacenter":
                proxy.weight += 150
            case "isp":
                proxy.weight += 200
            case "mobile":
                proxy.weight += 300
    
        if proxy.last_used: 
            _seconds_since_last_use = time() - proxy.last_used
            proxy.weight += _seconds_since_last_use


        return proxy.weight

    def get(self):
        proxy_weights = [self._weigh_proxy(p) for p in self.proxies]
        proxy = random.choices(
            self.proxies,
            weights=proxy_weights,
            k=1,
        )[0]
        proxy.last_used = time()
        self.last_subnet = proxy.subnet
        return proxy
