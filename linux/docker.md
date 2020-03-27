---
layout: post
title: Docker
---

# ubuntu imageで基本的なツールをインストール
ubuntuのDocker Imageでは，Imageを小さくするために，開発などで良くしようするmanなどの基本的なコマンドはインストールされない．
ubuntuのimageをデプロイに使用する時は良いが，開発で使用するには少し不便．
そこで，ubuntuでDocker Imageからデフォルトでインストールされる物をインストールする `unminimize` というコマンドがある．
このコマンドを用いて，ubuntuのImageを作っておくと，開発環境としては便利．
ただ，このコマンドを打つだけでImageのサイズが400MBを越えてくるので，くれぐれもデプロイしないように気をつけよう．

```dockerfile
FROM ubuntu:18.04
RUN apt-get update && yes | unminimize
```
