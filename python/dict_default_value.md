---
layout: post
title: リストの辞書でいい感じに初期値を扱いたい
---

Pythonで属性に併せて値を集計する場合に辞書でキーをstr，値をlistにする事が良くあると思う．
この時に値が無ければ空のリストを設定するという場合には以下ように良く書いたりしていた．
```python
dict_to_list = {}
if "hoge" not in dict_to_list:
    dict_to_list["hoge"] = []
dict_to_list["hoge"].append(1)
```

値を読み取るだけの場合だったら以下のように書けば，キーがない事を考えなくてもよくなる．
```python
d =  dict_to_list.get('hoge', [])
```
これを書き込みの場合でも行いたい．

ただこれをそのまま書いても，書き込みは出来ない．
```python
dict_to_list.get('hoge', []).append(1)
dict_to_list #=> {}
```

と思って探したら，setdefaultなる関数がdictにはあるらしい．
これを使うと以下ように書ける．
```python
dict_to_list.setdefault('hoge', []).append(1)
dict_to_list #=> {'hoge': [1]}
```
多分，日本で知らないのは自分だけだったかもしれないが，便利で感動したのでメモ．
