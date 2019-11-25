---
layout: post
title: PowerDNSのALIASレコードについて(使わない方が良いと思うよ)
---


現在のRFCではZone ApexにCNAMEを指定する事が出来ない．
これはCNAMEが他のレコードと共存出来ないとう制限に起因する．
Zone Apexでは必ずNSレコードが存在するために，CNAMEと共存する事が出来ない．

現在，この問題に対処するためにZone Apexにもエイリアスを張る事の出来る，ANAMEというレコードが提案されて，IETFで議論されている， [^1]

ただ，このような需要を満すために，AWSやPowerDNSには独自のAliasレコードという物が存在する． [^2] [^3]
AliasレコードはCNAMEのようにZone Apexに別名を指定する事が出来る．
ただ，名前解決時にはCNAMEのように返答する事は出来ないので，権威サーバ側でエイリアスのドメイン名に対して名前解決を行い，AレコードとしてIPアドレスの応答を行う．
これで，一見して，Zone Apexにエリイアスが張れたように見える．

PowerDNSは，この機能は，Resolverが動作していないと使用する事が出来ない．
なので， `pdns.conf` で以下のように設定を行う必要がある．
```
resolver=[::1]:5300
expand-alias=yes
```
でも，ここで問題がある．
PowerDNSを外に公開するコンテンツサーバとして使用したくないという問題である．
そこで，多くの場合，公開するコンテンツサーバにゾーン転送を行う．
ゾーン転送を行なった場合にこれは，PowerDNSの独自ゾーンなのでAliasレコードとしてゾーン転送が出来ない可能性があるという事である．(受け付け先もPowerDNSなら出来る)
そのために以下の設定を `pdns.conf` に起こなう必要がある．
```
outgoing-axfr-expand-alias=yes
```
この設定が `yes` の場合，ゾーン転送時に名前解決を行い， `A` もしくは `AAAA` レコードとしてゾーン転送が行なわれる．
この次点で，勘の良い人は気付くと思うが，名前解決はゾーン転送の時に行なわれたっきりになってしまうのだ．
頻繁にゾーン転送が行なわれるようなサーバなら問題ないかもしれないが，そうでない事も多い．
そうすると，これはSOAレコードの `expire` までは更新されない事になってしまう．
これは幾つか問題がある．
`CNAME` を使いたい場合というのはドメイン名の先を `CDN` に向けて，サービスの可用性を上げたいといった事が考えられる．
しかし，この `ALIAS` では，例えば，エイリアス先のレコードが何かしらの理由で変更された場合にも，追従する事が出来ない．
つまり， CDNを利用した可用性の向上を邪魔してしまう事になる．
また， `CDN` を用いた，レコードの返答による地理分散も1度名前解決を行なったっきりとなるので，利用する事が出来ない．
これは，ゾーン転送でない場合にも同様である．

以上の事から， `ALIAS` レコードは個人的には使用するべきではないと思う．
使用するにしても， PowerDNSをコンテンツサーバとして外部に公開するといった状況でのみ使用するべきだと思う．

また，PowerDNSにつて書いたがAWSのRoute 53も問題を抱えており，こちらはさらに酷く，TTLを一切守ってくれないので，こちらは絶対に使用を避けた方が良い．



[^1]: [Address-specific DNS aliases (ANAME)](https://tools.ietf.org/id/draft-ietf-dnsop-aname-03.html)
[^2]: [Using ALIAS records — PowerDNS Authoritative Server documentation](https://doc.powerdns.com/authoritative/guides/alias.html)
[^3]: [Route 53 のエイリアスレコードの作成](https://aws.amazon.com/jp/premiumsupport/knowledge-center/route-53-create-alias-records/)
