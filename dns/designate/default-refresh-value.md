# DesignateのデフォルトのRefreshの値について
Designateでは，ゾーンの作成時に設定ファイルに指定されたデフォルトの値によって，RefreshやRetryやNegative TTLなどを決定する．
例えば， `designate.conf` で， `default_soa_minimum` を設定することでゾーン作成時に，Negative TTLがこの値に設定される．
```
default_ttl = 3600
default_soa_retry = 600
default_soa_expire = 86400
default_soa_minimum = 600
```

SOAのデフォルト値の中で， Refreshのみ設定方法が異なる．
```
default_soa_refresh_min = 3500
default_soa_refresh_max = 3600
```
Designateはゾーンの作成時にこのmaxとminの間の中からランダムで値を決定する．[^gen_refresh]
これは，コメントがないので確かな事は分からないがおそらく，ゾーン転送のリフレッシュを分散するために行なわれている．
同一の時間に設定してあると，ゾーンの更新の少ないゾーンに対しては，refresh値に応じて再度，ゾーン転送要求が行なわれる．
PowerDNSなどをバックエンドにしている場合，PowerDNSはゾーン転送をデフォルトでは1つのスレッドで順番に行うため[^pdns_zoen_thread]，ゾーン転送がキューに詰ってしまうことになる．
これを防止するために，おそらくランダムにrefreshの値を設定してるのだと思う．


[^gen_refresh]: [designate/service.py at 526b8dca991f2635dd36b19badcf1655c0aef67e · openstack/designate](https://github.com/openstack/designate/blob/526b8dca991f2635dd36b19badcf1655c0aef67e/designate/central/service.py#L823-L834)
[^pdns_zoen_thread]： 'retrieval-threads' の値を設定すれば変更することが出来る
