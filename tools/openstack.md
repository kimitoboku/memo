# OpenStack

OpenStackのCLIのやつ．
OpenStack自体はToolじゃない所に書くがそのうちやいのやいのする．

## IPアドレスからBindしてるPortの情報を所得．
```
$ openstack port list --fixed-ip ip-address=192.1.2.1
```
これで得られたPort IDで見る．
```
$ openstack port show {port id}
```

まとめるとこんな感じ
```
$ openstack port show $(openstack port list --fixed-ip ip-address=192.1.2.1 -f value -c ID)
```
