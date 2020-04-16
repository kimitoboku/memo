---
layout: post
title: Go言語で2次元のmapを使いたい時
---

複数のキーを持つ2次元の辞書のようなデータ構造を使いたい時がある．
変数の定義自体は，Go言語で以下のように行える．

```go
var map2d map[string]map[string]string
```

ただ，1次元のmapのようにそのまま使用する事が出来ない．
```
map2d["hoge"]["huga"] = "poyo"
```
などと代入しようとすると， `panic: assignment to entry in nil map` となってエラーになってしまう．
これは， mapの中のmapへのポインタがnilになっているために発生します．

これを解決するには，初期化を正しく行う必要があります．
```go
var map2d map[string]map[string]string


if _, ok := m["hoge"]; !ok {
    map2d["hoge"] = make(map[string]string)
}
map2d["hoge"]["huga"] = "poyo"
```

これは面倒なので，対策としては，map in mapを諦めるのが良いと思います．
```go
type mapKeys strcut {
    key1 string
    key2 string
}

var map2d map[mapKeys]string

map[mapKeys{"hoge", "huga"}] = "poyo"
```
これで1次元のmapなのでエラーはでないし，要素2つをKeyにとれてる，

自分のアイデアではないが，自分用のメモとして，記録．

参考リンク
- [Goで多次元マップ（複数のキーからなるマップ）を実現したいときにはどうするか - Qiita](https://qiita.com/ruiu/items/476f65e7cec07fd3d4d7)
