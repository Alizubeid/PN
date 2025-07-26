# Proxy Checker
>simple tool for test online proxies
## clone the project
```sh
git clone https://github.com/Alizubeid/PN.git
cd PN
pip install -r ./requirments.txt
python main.py -h
```
## arguments
`-h`,`--help` show the help page.

`-p`,`--proxy` set proxy. example `[protocol]://[host_or_ip]:[port]`. accept `socks4`,`socks5`,`http` and `https` protocols. *separated by `,` allows you to check list of proxies.*
```sh
python main.py --proxy socks4://192.111.129.145:16894,socks4://199.58.184.97:4145,socks4://72.37.216.68:4145,socks4://184.181.217.201:4145
```

`-f`,`--file` set proxy list file path.


`-o`,`--output` set output file having online proxies (defualt `./online.txt`). and sorted by delay.

`-t`,`--timeout` set timeout (defualt `2`).