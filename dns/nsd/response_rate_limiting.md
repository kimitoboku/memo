# Response Rate Limiting
NSDはデフォルトでReponse Rate Limiting (RRL) がONになっている。
RRLは、DNSコンテンツサーバがDNS amp攻撃の踏み台とならないために存在する機能である。
DNS amp攻撃は、UDPパケットの送信元IPアドレスを攻撃対象のIPアドレスにし、DNSのレスポンスを攻撃対象に向ける攻撃手法である。
RRLは、この攻撃の緩和手法である。
DNSコンテンツサーバへの問い合わせは通常は、DNSキャッシュサーバが行う、つまり、通常は問い合わせをキャッシュしているはずである。
それを利用して、同じ送信元のIPアドレスから、同じレコードに対して大量の問い合わせがあった場合に、コンテンツサーバにおいてRate Limitingを行う機能である。
NSDのRRLには以下のようなオプションがある。
```
rrl-size: 1000000
rrl-ratelimit: 200
rrl-ipv4-prefix-length: 24
rrl-ipv6-prefix-length: 64
rrl-slip: 2
rrl-whitelist-ratelimit: 2000
```

`rrl-size` はRRLのカウントを行うハッシュテーブルのサイズを表している。
大きいとそもぶんメモリを食う

`rrl-ratelimit` は最も大事な何qps(query per second)でRate Limitを発動するかの閾値を決定している。
`0` を設定するとRRLが無効になる。

`rrl-ipv4-prefix-length` と `rrl-ipv6-prefix-length` はそれぞれ、RRLのカウントをどのプレフィックスの長さでまとめるかを表している。

`rrl-whitelist-ratelimit` は `rrl-ratelimit` とは異なる値を設定して、RRLの制限を一部緩くしたホワイトリストに対する最大qpsを指定する。
ホワイトリストは `zone`　説の中で分類タイプとともに例えば以下のように設定する。
```
zone:
  name: example.com
  zonefile: example.com.zone
  rrl-whitelist: nxdomain
```
といった形で設定する、これにより、 `example.com` への問い合わせの結果が `NXDOMAIN` だったレスポンスに対しては、 `rrl-whitelist-ratelimit` のqpsで制限される。
また、このタイプにはnxdomain, error, referral, any, rrsig, wildcard, nodata, dnskey, positive, allが使用出来る。


`rrl-slip` はSLIP応答(TCPにフォールバックしろという応答)を返すまでのパケット数である。
DNS amp攻撃は基本的にUDPで行われるので、TCPにはRRLは行われない。
`rrl-slip` はUDPでRate Limitに引っかかった場合にその後、nパケット目にSLIP応答を返すという設定になる。
デフォルトの `2` の場合は1回目は破棄して、2回目のパケットでSLIP応答を返す。
毎回返したい場合は `1` を設定すればいい。
返したくない場合は　`0` を指定する。

まぁ、なんでこんなながながと書いたかというと、NSDのベンチマークを取ろうとして、RRLに気付かずに30分くらいはまったからですね。
