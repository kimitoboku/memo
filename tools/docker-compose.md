---
layout: post
title: docker-compose
---

# docker-composeでコンテナに静的にIPアドレスの割り当て
以下ようにnetworkを作成してそれを元にsubnetからアドレスを割り当てる．
networksは同名がなければ生成される．
同名ということが大事なので，ここの設定だけ変えてしまうと，動作しなくて困ったりする．
ここの設定を変更したらネットワークをデストロイしよう．

```yml
version: '2'
services:
  master:
    image: nsd
    hostname: dns-master
    networks:
      app_net:
        ipv4_address: 172.31.0.1
  slave:
    image: nsd
    hostname: dns-slave
    networks:
      app_net:
        ipv4_address: 172.31.0.2

networks:
  app_net:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.31.0.0/24
```