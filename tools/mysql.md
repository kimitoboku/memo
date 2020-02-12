---
layout: post
title: MySQLのよく使うやつ
tags: sql, mysql
---

# Indexの確認

```
mysql> show index from domains;
```

# Tableの確認
```
mysql> show tables;
```

# クエリの回数の確認
```
mysql> show status where Variable_name = 'queries';
```

# データベースの一覧
```
show database;
```

# データベースの選択
```
use hoge;
```

# 現在使用しているデータベースの確認
```
select database();
```

# 作成したテーブルと同様のテーブルを作成するためのCREATE TABLEを確認する
```
show create table hoges;
```
