---
title: Pythonのyamlのローダについて
layout: post
---

Pythonでyamlを読み込む場合には `PyYAML` というライブラリを使用する．
この時に何も考えずに，`load` を行おうとすると，Warrningが出力される．
なので，loadと同時に `Loader` を指定してあげる必要がある．

```python
import yaml
yaml_dict = yaml.load(fp, Loader=yaml.SafeLoader)
```

この時に， `Load` には3つの種類がある．

## SafeLoader
`SafeLoader` は最も安全なLoaderでYAMLのサブセットが動作する．
外部からyamlの入力を受け付ける場合はどは，これを使用する．


## FullLoader
`FullLoader` 現在のデフォルトのローダで，基本的にはフル機能のYAMLを受け付ける．
一部の任意のコード実行を行えるような動作は使用出来ない．
現在のデフォルトのローダらしい．(でもワーニングは出る)


## UnsafeLoader
`UnsafeLoader` は元々のローダでフルパワーのYAMLを処理出来る．
なので，任意コードも実行出来たりするらしい．
ふるふる機能なので，本当に必要な時は使えば良いらしい．
