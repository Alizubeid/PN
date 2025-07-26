from requests import get, exceptions
from colorama import Fore
import argparse
import time


def check_proxy(url_proxy: str):
    # It is expected that we may encounter timeout or connection failure errors.
    try:
        # accept [http, https, socks, ftp] protocols
        if url_proxy.startswith("socks"):
            proxies = {"http": url_proxy, "https": url_proxy}
        elif url_proxy.startswith("http"):
            proxies = {"http": url_proxy}
        elif url_proxy.startswith("http"):
            proxies = {"http": url_proxy, "https": url_proxy}
        elif url_proxy.startswith("ftp"):
            proxies = {"ftp": url_proxy}
        # 'start' and 'end' variables show the delay
        start = time.time()

        # check the proxy is online or not
        response = get(
            "http://www.gstatic.com/generate_204", proxies=proxies, timeout=3
        )
        end = int((time.time() - start) * 1000)

        # print seccuss message if proxy is online
        if response.status_code == 204:
            print(
                Fore.LIGHTGREEN_EX
                + "[+] {} => {} ms".format(url_proxy, end)
                + Fore.RESET
            )

    except exceptions.ConnectionError:
        # print connection error
        print(Fore.LIGHTRED_EX + f"[!] {url_proxy} : ConnectionError" + Fore.RESET)

    except exceptions.Timeout:
        # print time out error
        print(Fore.LIGHTYELLOW_EX + f"[!] {url_proxy} : TimeOut" + Fore.RESET)

# set argparse arguments
parser = argparse.ArgumentParser("ProxyChecker")
parser.add_argument(
    "-p",
    "--proxy",
    help="""
set the proxy url |
example : [protocol]://[ip]:[port] | also you can put list of proxy if you separated them with \",\" like socks4://127.0.0.1:9050,socks5://127.0.0.1:9051,http://119.3.113.150:9094
""",
    default="socks5://127.0.0.1:9050",
)
parser.add_argument("-f", "--file",help="set proxy list file path ")


if __name__ == "__main__":
    # get arguments from user
    get_args = parser.parse_args()
    # check proxy list
    if proxy := get_args.proxy:
        if "," in proxy:
            for each in proxy.split(","):
                check_proxy(each)
        else:
            check_proxy(proxy)
    # check proxy list file
    if file_path := get_args.file:
        with open(file_path) as proxy_list_file:
            proxy_list = [
                proxy.replace("\n", "") for proxy in proxy_list_file.readlines()
            ]
        for proxy in proxy_list:
            check_proxy(proxy)
