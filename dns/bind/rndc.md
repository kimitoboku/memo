---
layout: post
title: rndcでよく使うやつ
---


# rndc reconfig
`named.conf` と新しく追加されたゾーン情報をリロードする．
新しく追加されたゾーンの `type` が `slave` の場合は， `masters` からゾーン転送を行う
Bindの場合は， `masters` が複数ある場合は，最もシリアルの高いマスターを選択してくれる．
また，設定ファイルからゾーンが削除された場合には，ゾーンを管理から外す．

# rndc reload
`named.conf` とこれまでも保持していたゾーンの情報をリロードする，
ゾーンの `type` が `slave` の場合には `masters` のシリアルと比較して，保持しているシリアルよりも値が大きければ， `masters` からゾーン転送を行う．
Bindの場合は， `masters` が複数ある場合は，最もシリアルの高いマスターを選択してくれる．


# rndc reload ZONE
指定したゾーンの情報をリロードする．
ゾーンの `type` が `slave` の場合には `masters` のシリアルと比較して，保持しているシリアルよりも値が大きければ， `masters` からゾーン転送を行う．
Bindの場合は， `masters` が複数ある場合は，最もシリアルの高いマスターを選択してくれる．


# rndc status
Bindのステータスを表示する．
uptimeだとかquerylogの有効無効が確認出来る．


# rndc querylog
クエリログがonの場合はoffに，offの場合はonにする．
クエリを保存するファイルは `named.conf` にて設定したデイレクトリが使われるので，確認しよう．


# rndc flush
サーバのキャッシュを統べて削除する．

# rndc flushname $LABEL
`$LABEL` にmatchするcacheの削除を行う。
あくまでもラベルにmatchする物だけなので `www.$LABEL` といったレコードのCacheの削除は出来ない。
`unbound-control flush_zone $LABLE` とは挙動が違うので注意(`unbound-control` の場合はゾーン単位なので以下のCacheも削除される)

# rndc stas
サーバの統計情報をファイルに出力する．
標準出力に出してくれればもっと使いやすかったのに．
デフォルトでは `/lvar/named/` 以下に 出力される．
