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
