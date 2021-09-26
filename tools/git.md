---
layout: post
title: git(tigも)
---


## tigでblame
blameは表示がちょっと複雑なので、tigで見るのが便利。
```
$ tig blame tools/ansible.md
```

## コミットメッセージの修正
やっちゃったコミットを修正出来る。
```
git commit --amend
```

あと、良くあるのが、メールアドレスとかの設定を忘れていた時とかで、その場合は以下のようにしてメールアドレスとかをリセットしてコミットしなおせる。
```
git commit --amend --reset-author
```


## git logを検索
git logは `-G` オプションでcommitの変更を検索出来る。
変更対象がどのタイミングで変更されたのか確認したい時にはblameよりも便利だったりする。

`-p` を付けると変更内容も確認出来るのでより分かりやすい。
```
$ git log -p -G'regex'
```

tigでも `-G` が使えるので便利。
```
tig -G'regex'
```