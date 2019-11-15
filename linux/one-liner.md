---
layout: post
title: 雑多ワンライナー達
---


# ファイルを行の長さでソート

```
$ cat hoge.txt
a
aaa
aa
aaaaaaaaa
aaaaa
$ cat hoge.txt | awk '{ print length, $0 }' | sort -n -s -r | cut -d" " -f2-
aaaaaaaaa
aaaaa
aaa
aa
a
```

`awk` で文字列と文字列の長さを出力して，文字列の長さでソートして， `cut` で文字列だけ取り出す．
