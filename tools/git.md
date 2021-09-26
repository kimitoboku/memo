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

## プロジェクトを検索
git grepを使えば、gitの管理対象のみを検索する事が出来る。
```
git grep "hoge"
```

defaultでは行番号がないので表示も出来る。
```
git grep -n "hoge"
```

また、特定のフォルダを対象にして検索も出来る。またフォルダ名に `:!` を除外して検索出来る。
```
git grep "hoge" -- tools/
git grep "hoge" -- :!tools/
```

また、特定のコミットでの検索も出来る。
```
git grep "git" 905c31761aae388b691ea72de8c2ec37704e05f7
```




