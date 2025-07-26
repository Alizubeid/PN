from requests import get, exceptions
from colorama import Fore
import argparse
import time


def check_proxy(url_proxy: str):
    try:
        if url_proxy.startswith("socks"):
            proxies = {"http": url_proxy, "https": url_proxy}
        elif url_proxy.startswith("http"):
            proxies = {"http": url_proxy}
        elif url_proxy.startswith("http"):
            proxies = {"http": url_proxy, "https": url_proxy}
        elif url_proxy.startswith("ftp"):
            proxies = {"ftp": url_proxy}

        start = time.time()
        response = get(
            "http://www.gstatic.com/generate_204", proxies=proxies, timeout=3
        )
        end = int((time.time() - start) * 1000)
        if response.status_code == 204:
            print(
                Fore.LIGHTGREEN_EX
                + "[+] {} => {} ms".format(url_proxy, end)
                + Fore.RESET
            )

    except exceptions.ConnectionError:
        print(Fore.LIGHTRED_EX + f"[!] {url_proxy} : ConnectionError" + Fore.RESET)

    except exceptions.Timeout:
        print(Fore.LIGHTYELLOW_EX + f"[!] {url_proxy} : TimeOut" + Fore.RESET)


parser = argparse.ArgumentParser("ProxyChecker")
parser.add_argument(
    "-p",
    "--proxy",
    help="""
set the proxy url |
example : [protocol]://[ip]:[port]
""",
    default="socks5://127.0.0.1:9050",
)
parser.add_argument("-f", "--file")

if __name__ == "__main__":
    get_args = parser.parse_args()
    if proxy := get_args.proxy:
        if "," in proxy:
            for each in proxy.split(","):
                check_proxy(each)
        else:
            check_proxy(proxy)
    if file_path := get_args.file:
        with open(file_path) as proxy_list_file:
            proxy_list = [
                proxy.replace("\n", "") for proxy in proxy_list_file.readlines()
            ]
        for proxy in proxy_list:
            check_proxy(proxy)
