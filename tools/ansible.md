---
layout: post
title: ansible
---

よく使われる構成管理ツール
初回のデプロイには便利だけど，その後の継続利用とかにはちょっと，何があるんじゃないかというお気持ち．



特定のホストにだけPlaybookを適応は `l` オプション
```
$ ansible-playbook playbook.yml -l TARGET_HOST
```


ステップ実行は `--step` (1つのtaskごとにy/nで実行するかどうかを確認出来る)
```
$ ansible-playbook playbook.yml --step
```

特定のtask移行を実行は `--start-at=` オプション
```
$ ansible-playbook playbook.yml --start-at="Task Name"
```
