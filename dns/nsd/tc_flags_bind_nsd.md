---
layout: post
title: BindとNSDのTCグラフが付いている場合のレスポンスの違い
---

BindとNSDではTCグラフが付いたレスポンスの内容が異なる事に気が付いたので、まとめる。

# TL;DR
- BindはTCフラグが付いている場合に512バイトで収まるレコードをAnswerに付けて応答する
- NSDはTCフラグが付いている場合にはAnswerは空で応答する
- TCフラグ付きで帰ってきたら、AnswerにデータがあってもちゃんとTCPにフォールバックしよう

# DNS Authへの問い合わ
DNS Authへの問い合わせるために以下のようなコードを書いていた。
```python
import dns.resolver
import dns.query
import dns.name
import dns.rdatatype
import dns.message


def send_dns_query_test(dest_ip, name, rrt):
    qname = dns.name.from_text(name)
    rrtype = dns.rdatatype.from_text(rrt)
    qo = dns.message.make_query(qname, rrtype)
    try:
        resp = dns.query.udp(qo, dest_ip, timeout=2)
    except Exception as e:
        print(f"{dest_ip} {name} {rrt}")
        raise e
    return resp
```

このコードで問い合わせを行った時に、以下のようなレスポンスの違いを確認した。

以下のようなレコードをテスト用に作成する。

```
# dig @localhost test-text.example.com  -t TXT

; <<>> DiG 9.11.4-P2-RedHat-9.11.4-26.P2.el7_9.3 <<>> @localhost test-text.example.com -t TXT
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 42520
;; flags: qr aa rd; QUERY: 1, ANSWER: 6, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;test-text.example.com.         IN      TXT

;; ANSWER SECTION:
test-text.example.com.  3600    IN      TXT     "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
test-text.example.com.  3600    IN      TXT     "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
test-text.example.com.  3600    IN      TXT     "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
test-text.example.com.  3600    IN      TXT     "ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
test-text.example.com.  3600    IN      TXT     "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
test-text.example.com.  3600    IN      TXT     "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Mon Feb 15 15:25:10 JST 2021
;; MSG SIZE  rcvd: 746

```
このレコードはメッセージサイズが512 byteを超える状態になっている。

このレコードをBindとNSDでそれぞれ用意した。
なおBindのバージョンは `BIND 9.16.3 (Stable Release)`, NSDのバージョンは `4.3.3` を利用している。

まずNSDのホストに対して問い合わせを行うと以下のようなレスポンスが帰ってきた。

```
In [98]: send_dns_query_test("10.241.18.98", 'test-text.example.com', "TXT")
Out[98]: <DNS message, ID 45382>

In [99]: resp1 = send_dns_query_test("10.241.18.98", 'test-text.example.com', "TXT")

In [100]: print(resp1)
id 56724
opcode QUERY
rcode NOERROR
flags QR AA TC RD
;QUESTION
test-text.example.com. IN TXT
;ANSWER
;AUTHORITY
;ADDITIONAL

In [101]: resp1.answer
Out[101]: []

```
ResponseのFlagに `TC` が付いており、TCPへのフォールバックを要求している。

次にBindのホストに対して問い合わせを行った。

```
In [102]: resp2 = send_dns_query_test("10.241.18.99", 'test-text.example.com', "TXT")

In [103]: print(resp2)
id 19452
opcode QUERY
rcode NOERROR
flags QR AA TC RD
;QUESTION
test-text.example.com. IN TXT
;ANSWER
test-text.example.com. 3600 IN TXT "ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
test-text.example.com. 3600 IN TXT "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
test-text.example.com. 3600 IN TXT "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
test-text.example.com. 3600 IN TXT "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
;AUTHORITY
;ADDITIONAL

In [104]: resp2.answer
Out[104]: [<DNS test-text.example.com. IN TXT RRset: [<"ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc...>, <"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee...>, <"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb...>, <"fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff...>]>]

```
4つのレコードがAnswerに設定されて応答された。

再度、実行する。
```
In [105]: resp2 = send_dns_query_test("10.241.18.99", 'test-text.example.com', "TXT")

In [106]: print(resp2)
id 20860
opcode QUERY
rcode NOERROR
flags QR AA TC RD
;QUESTION
test-text.example.com. IN TXT
;ANSWER
test-text.example.com. 3600 IN TXT "ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
test-text.example.com. 3600 IN TXT "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
test-text.example.com. 3600 IN TXT "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
test-text.example.com. 3600 IN TXT "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
;AUTHORITY
;ADDITIONAL

In [107]: resp2.answer
Out[107]: [<DNS test-text.example.com. IN TXT RRset: [<"ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc...>, <"fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff...>, <"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa...>, <"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb...>]>]


```
先ほどと異なる、レスポンスが入って帰ってきた。
Bindではラウンドロビンされたレコードで512 byteに収まるように応答する事が分かった。


# まとめ
BindとNSDでレスポンスTCフラグが付いている場合の挙動の差を確認した。
普通のクエリはEDNSが有効になっているしなかなか気付きにくいが、レスポンスに差がある事から面白かったのでとりあえずまとめた。
TCフラグが付いてれば、TCPにFallBackするコードを書こう。

```
def send_dns_query(dest_ip, name, rrt):
    qname = dns.name.from_text(name)
    rrtype = dns.rdatatype.from_text(rrt)
    qo = dns.message.make_query(qname, rrtype)
    try:
        resp = dns.query.udp(qo, dest_ip, timeout=2)
        if resp.flags & dns.flags.TC:
            # if response has tc flags, DNS Response is bigger than 512 bytes
            resp = dns.query.tcp(qo, dest_ip, timeout=2)
    except Exception as e:
        print(f"{dest_ip} {name} {rrt}")
        raise e
    return resp
```