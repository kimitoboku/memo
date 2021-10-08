---
layout: post
title: IPアドレスでLongest Prefix Matchで値を取り出す
---

ネットワーク関係のToolを開発している時に、FIBとRIBを用いた経路の確認といった、IPアドレスのPrefixを用いたツールを作りたい場合がある。
多くの場合は、あるIPアドレスがどの経路に行くのかの確認を行いたい。
ただ、これを素直に実装するには区間木やTrie木などを自分で記述したりする必要があり、適当なツールを作りたいのに面倒な事になる。
Pythonなので、便利なライブラリを利用して調査をした結果、以下のライブラリが便利そうであったの使い方をまとめる。
- [jsommers/pytricia: A library for fast IP address lookup in Python.](https://github.com/jsommers/pytricia)

以下のように利用する。
```
In [1]: import pytricia

In [2]: pyt = pytricia.PyTricia()

In [3]: pyt['0.0.0.0/0'] = 'default'

In [4]: pyt['10.0.0.0/8'] = 'gateway'

In [5]: pyt['10.1.1.1/32']
Out[5]: 'gateway'
```
`pytricia` のインスタンスを作成する。
このインスタンスは辞書のように取り扱う事が出来る。
あとは、IPアドレスを通常の辞書の要素を得るように利用するだけで、Longest Prefix Matchでmatchした要素を得る事が出来る。
例えば、これで、LinuxのFIBを格納などを行えば、簡単な経路のシミュレータなどを数行で記述する事が出来る。