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


## gitでpatchファイルの作成

gitは現在からの差分込みでcommit毎のpatchを作成する事が出来る
git format-patch機能を利用すればコミットメッセージなど込みのpatchを作成する事が出来る。

```
$ : logを確認
$ git log -n 4
commit b9375d6752a03fc29d1ac8c8deee2f9844cc48b9 (HEAD -> master, origin/master, origin/HEAD)
Author: Kento Kawakami <kimitoboku@techack.net>
Date:   Fri Sep 9 16:32:17 2022 +0900

    Add mulit hosts file in one inventory

commit 57809fc213cd0071647cfc19e6bd1891ac5204cd
Author: Kento Kawakami <kimitoboku@techack.net>
Date:   Tue Sep 6 12:18:33 2022 +0900

    Add how to check MySQL acl

commit 62b91c4141aee331b4b2fee70f683a8077171c07
Author: Kento KAWAKAMI <emaxser@bonprosoft.com>
Date:   Sat Apr 9 13:37:33 2022 +0900

    fix format

commit d95cb079c2aeef6e925896aecda48614d26b9b1b
Author: Kento KAWAKAMI <emaxser@bonprosoft.com>
Date:   Sat Apr 9 13:35:05 2022 +0900

    Add new useal options

$ : patchを作成
$ git format-patch 62b91c4141aee331b4b2fee70f683a8077171c07
0001-Add-how-to-check-MySQL-acl.patch
0002-Add-mulit-hosts-file-in-one-inventory.patch

$ : Patchの適用
$ git am 0001-Add-how-to-check-MySQL-acl.patch
$ git am 0002-Add-mulit-hosts-file-in-one-inventory.patch
```

diffからpatchコマンドから適用出来るpatchを作成する事も出来る。
diffコマンドでは通常だとunstageの変更を出す事が出来る。
もちろんmasterとの差分など普通のdiffコマンドのように使えば良い。

```
$ : patchの作成
$ git diff > hoge.patch

$ : patchの適用
$ patch -p1 < hoge.patch
```
