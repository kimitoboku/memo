---
layout: post
title: DNSのSOAレコードで指定されている値について
---

DNSでは `SOA` レコードとよばれるゾーンの管理情報などを指定するためのレコードが存在します．
`SOA` レコードのパラメータにはいくつか意味があるのですが，それぞれの意味をよく調べなおしたりするので，まとめます．

`SOA` レコードは以下のような形式です．
```
@ IN SOA　 ns1.example.com. mail.example.com. (
　　　　　　　 1575971717 ; Serial
　　　　　　　 3568 ; Refresh　
　　　　　　　 600 ; Retry
　　　　　　　 604800 ; Expire
　　　　　　　 3600 ; Negative TTL
　　　　　　　 )　
```

このパラメータのそれぞれの意味について解説します．
最初の `ns1.example.com.` やら `mail.example.com.` やらはネームサーバと管理者のメールアドレスです．
メールアドレスはこの場合 `mail@exmaple.com` になります．


## Serial
保持しているゾーンのバージョンを表わす値です．
値が大きければ大きいほど，新しいゾーンという事になります．
例えば，ゾーン転送をしているSlaveサーバがmasterに問合せた時には，このSerialの値を比較して，ゾーンに更新があるかどうかを判断します．
保持しているSerialの値がmasterサーバ提示しているゾーンよりも小さい場合，ゾーン転送が行なわれます．
なので，もし，このSerialの値をやりなおしたい場合は，Notifyなどでは更新することは出来ず，RefreshやExpireを待つ必要があります．


## Refresh
Notifyによらずに，ゾーンデータを再所得するまでの時間です．
前回のゾーン転送が行なわれた時間からの経過時間なので，もし，この値を同じ値で，多くのゾーンをホストしていると，Slaveサーバから，定期的に同時にゾーン転送が来る可能性があるので，注意が必要です．

## Retry
Refresh時にゾーン転送が失敗した場合に，再度問合せを行うまでの間隔です．


## Expire
RefreshやRetryを繰替えしてもゾーン転送が成功しなかった場合に，そのゾーンの情報を何時まで保持するのかという値です．
ゾーン転送が失敗し続けて，この値を向えると，そのコンテンツサーバからは指定のゾーンは名前解決が行えなくなります．
Masterサーバが死んだ場合に復旧するまでの制限時間と捉えても大丈夫です．


## Negative TTL
これは，NXDOMAINなどを返答した場合に，キャッシュサーバがどの程度，NXDOMAINといいったネガティブなデータを保持するのかという値です．
レコードが頻繁に変更される可能性がある場合はこの値は出来る限り，小さな値にしておくのが適当だと思います．
例えば，Googleなどはこの値が1分になっています．

```
$ dig google.com -t soa

; <<>> DiG 9.10.6 <<>> google.com -t soa
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 6021
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4000
;; QUESTION SECTION:
;google.com.                    IN      SOA

;; ANSWER SECTION:
google.com.             60      IN      SOA     ns1.google.com. dns-admin.google.com. 284949692 900 900 1800 60

;; ADDITIONAL SECTION:
ns1.google.com.         61056   IN      A       216.239.32.10
ns1.google.com.         78242   IN      AAAA    2001:4860:4802:32::a

;; Query time: 38 msec
;; SERVER: 10.32.220.132#53(10.32.220.132)
;; WHEN: Thu Dec 12 16:08:48 JST 2019
;; MSG SIZE  rcvd: 133

```
また，この値は `SOA` レコードと `Negative TTL` の短い方が採用されるので， 同じ値を設定しておたい方が確認が行ないやすく良いと思います．
