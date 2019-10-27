---
layout: post
---

自分のtmux環境のメモ

tmux.conf、マウスをonにしてヒストリー増やして、タブのインデックスを1から
```
set -g prefix C-t
unbind C-b
set -g default-terminal "screen-256color"
set -sg escape-time 1
set-option -g history-limit 1000000
set-option -g mouse on
set -g base-index 1
setw -g pane-base-index 1
```

## macOS
クリップボードの共有的なの
```
brew install reattach-to-user-namespace
```
