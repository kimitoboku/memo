---
layout: post
---


# gelworm
問い合わせてきたリゾルバのIPアドレスを返すDNSサーバ
DNSをロードバランスしてる時に、正しく分散されているか確認するために使う。

`go get` でインストール
```
$ go get github.com/kimitoboku/gelworm
```

実行は、バイナリを実行するだけ。
```
$ gelworm
$ dig @localhost -p 15353 www.example.com -4

; <<>> DiG 9.10.6 <<>> @localhost -p 15353 www.example.com -4
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 23324
;; flags: qr rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;www.example.com.		IN	A

;; ANSWER SECTION:
www.example.com.	3600	IN	A	127.0.0.1

;; Query time: 0 msec
;; SERVER: 127.0.0.1#15353(127.0.0.1)
;; WHEN: Thu Aug 08 17:56:04 JST 2019
;; MSG SIZE  rcvd: 64
```
