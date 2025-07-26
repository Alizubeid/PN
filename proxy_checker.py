import requests
from time import time
from colorama import Fore


class ProxyChecker:
    online_list = []

    def __init__(self, timeout: int = 5):
        self.proxy: str = None
        self.host_or_ip: str = None
        self.protocol: str = None
        self.proxies: dict = None
        self.timeout = timeout
        self.is_valid = False

    def set_proxy(self, proxy):
        self.proxy = proxy
        self.is_valid = True

    def set_defualts(self):
        if self.is_valid:
            protocol_and_host = self.proxy.split("://")
            self.protocol = protocol_and_host[0]
            self.host_or_ip = protocol_and_host[1]

    def proxies_types_from_protocol_type(self) -> dict:
        return {
            "https": {
                "http": f"http://{self.host_or_ip}",
                "https": f"https://{self.host_or_ip}",
            },
            "socks": {
                "http": f"{self.proxy}",
                "https": f"{self.proxy}",
            },
            "http": {"http": f"http://{self.host_or_ip}"},
        }

    def set_proxies(self):
        if self.proxy.startswith("socks"):
            proxies = self.proxies_types_from_protocol_type().get("socks")
        else:
            proxies = self.proxies_types_from_protocol_type().get(self.protocol)

        if proxies:
            self.proxies = proxies
        else:
            self.is_valid = False

    def validation(self):
        self.set_defualts()
        self.set_proxies()
        return self.is_valid

    def send_requests(self):
        if self.is_valid:
            try:
                start = time()
                response = requests.get(
                    "http://www.gstatic.com/generate_204",
                    proxies=self.proxies,
                    timeout=self.timeout,
                )
                delay = int((time() - start) * 1000)
                if response.status_code == 204:
                    self.add_to_list(self.proxy, delay=delay)
                    print(
                        Fore.LIGHTGREEN_EX
                        + f"[+] {self.proxy} => {delay}ms"
                        + Fore.RESET
                    )
            except requests.exceptions.ConnectionError:
                print(
                    Fore.LIGHTRED_EX
                    + f"[-] {self.proxy} connection error"
                    + Fore.RESET
                )
            except requests.exceptions.Timeout:
                print(
                    Fore.LIGHTYELLOW_EX
                    + f"[!] {self.proxy} timeout error"
                    + Fore.RESET
                )

    def add_to_list(self, proxy, delay):
        self.online_list.append((proxy, delay))

    def sort_result_by_delay(self):
        self.online_list.sort(key=lambda x: x[1])

    def text_result(self) -> str:
        if self.is_valid:
            return "\n".join([proxy for proxy, delay in self.online_list])

    def save_proxy_list(self, file_path: str = "online.txt"):
        if self.is_valid:
            with open(file_path, "w") as output_file:
                output_file.write(self.text_result())
