# Blacklist management tool

### Add IP addresses from a text file

```bash
$ ./blacklist --host 10.0.0.254 --user admin --password <secret> --file ./blacklist.txt
2024-06-27 15:14:57 SNS blacklist tool
2024-06-27 15:14:57 File blacklist.txt: 4 ip addresses
2024-06-27 15:14:57 Connecting to 10.0.0.254 on port 443 with user admin
2024-06-27 15:14:57 4 IP addresses added to the blacklist
2024-06-27 15:14:57 Disconnected from 10.0.0.254
```

### list current blacklist

```bash
$ ./blacklist --host 10.0.0.254 --user admin --password <secret> --list
101 code=00a01000 msg="Begin" format="section_line"
[Result]
src=4.3.2.1 dstrange=0.0.0.0-255.255.255.255 timeout=25
src=2.3.4.5 dstrange=0.0.0.0-255.255.255.255 timeout=25
src=5.4.3.2 dstrange=0.0.0.0-255.255.255.255 timeout=25
100 code=00a00100 msg="Ok"
```