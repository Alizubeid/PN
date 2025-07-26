import argparse
import os
from proxy_checker import ProxyChecker

parser = argparse.ArgumentParser(description="Test")
parser.add_argument(
    "-p",
    "--proxy",
    default="socks5://127.0.0.1:9050",
)
parser.add_argument("-f", "--file", help="get proxy list file")
parser.add_argument("-t", "--timeout", type=int, help="set timeout")
parser.add_argument("-o", "--output", help="set output online proxy list file path")


if __name__ == "__main__":
    args = parser.parse_args()
    if timeout := args.timeout:
        proxy_checker_object = ProxyChecker(timeout)
    else:
        proxy_checker_object = ProxyChecker()

    if proxy := args.proxy:
        if "," in proxy:
            proxy_list = proxy.split(",")
            for each_proxy in proxy_list:
                proxy_checker_object.set_proxy(each_proxy)
                if proxy_checker_object.validation():
                    proxy_checker_object.send_requests()
        else:
            proxy_checker_object.set_proxy(proxy)
            if proxy_checker_object.validation():
                proxy_checker_object.send_requests()

    if proxy_list_file_path := args.file:
        if os.path.isfile(proxy_list_file_path):
            with open(proxy_list_file_path) as proxy_list_file:
                proxy_list = [
                    proxy.replace("\n", "") for proxy in proxy_list_file.readlines()
                ]
            for proxy in proxy_list:
                proxy_checker_object.set_proxy(proxy)
                if proxy_checker_object.validation():
                    proxy_checker_object.send_requests()
    
    proxy_checker_object.sort_result_by_delay()
    if output:=args.output:
        proxy_checker_object.save_proxy_list(output)
    else:
        proxy_checker_object.save_proxy_list()
