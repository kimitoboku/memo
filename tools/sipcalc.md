---
layout: post
title: sipcalc
---

IPアドレスのsubnetのレンジなどを計算出来るコマンド

インストール
```
$ brew install sipcalc
```

使い方
```
$ sipcalc 10.0.0.0/8
-[ipv4 : 10.0.0.0/8] - 0

[CIDR]
Host address            - 10.0.0.0
Host address (decimal)  - 167772160
Host address (hex)      - A000000
Network address         - 10.0.0.0
Network mask            - 255.0.0.0
Network mask (bits)     - 8
Network mask (hex)      - FF000000
Broadcast address       - 10.255.255.255
Cisco wildcard          - 0.255.255.255
Addresses in network    - 16777216
Network range           - 10.0.0.0 - 10.255.255.255
Usable range            - 10.0.0.1 - 10.255.255.254

```

IPv6にも使える
```
$ sipcalc -6 fc00::/7
-[ipv6 : fc00::/7] - 0

[IPV6 INFO]
Expanded Address        - fc00:0000:0000:0000:0000:0000:0000:0000
Compressed address      - fc00::
Subnet prefix (masked)  - fc00:0:0:0:0:0:0:0/7
Address ID (masked)     - 0:0:0:0:0:0:0:0/7
Prefix address          - fe00:0:0:0:0:0:0:0
Prefix length           - 7
Address type            - Unassigned
Network range           - fc00:0000:0000:0000:0000:0000:0000:0000 -
                          fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
```
