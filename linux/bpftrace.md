---
layout: post
title: bpftraceの使い方
---

bpftraceはeBPFを用いたトレーシングツールです，
使用感としては，FreeBSDのdtraceに近い感じです．

# インストール
openSUSEのメインリポジトリにはまだ入ってないので，devel:toolsリポジトリを追加します．
```
$ sudo zypper addrepo https://download.opensuse.org/repositories/devel:/tools/openSUSE_Tumbleweed/devel:tools.repo
$ sudo zypper ref
$ sudo zypper install bpftrace
```

# トレース出来るプローブ一覧を出力する．
```
$ sudo bpftrace -l  | grep net | head
tracepoint:net:net_dev_start_xmit
tracepoint:net:net_dev_xmit
tracepoint:net:net_dev_xmit_timeout
tracepoint:net:net_dev_queue
tracepoint:net:netif_receive_skb
tracepoint:net:netif_rx
tracepoint:net:napi_gro_frags_entry
tracepoint:net:napi_gro_receive_entry
tracepoint:net:netif_receive_skb_entry
tracepoint:net:netif_receive_skb_list_entry
```
デフォルトではdebugfsを確認してLinuxのプローブを表示する．

バイナリのUSDTを確認したい場合は以下のようにusdtとバイナリを指定する．
```
$ sudo bpftrace -l 'usdt:/usr/local/pgsql/bin/postgres' | grep query
usdt:/usr/local/pgsql/bin/postgres:postgresql:query__parse__start
usdt:/usr/local/pgsql/bin/postgres:postgresql:query__parse__done
usdt:/usr/local/pgsql/bin/postgres:postgresql:query__rewrite__start
usdt:/usr/local/pgsql/bin/postgres:postgresql:query__rewrite__done
usdt:/usr/local/pgsql/bin/postgres:postgresql:query__plan__start
usdt:/usr/local/pgsql/bin/postgres:postgresql:query__plan__done
usdt:/usr/local/pgsql/bin/postgres:postgresql:query__start
usdt:/usr/local/pgsql/bin/postgres:postgresql:query__done
usdt:/usr/local/pgsql/bin/postgres:postgresql:query__execute__start
usdt:/usr/local/pgsql/bin/postgres:postgresql:query__execute__done
```

# システムコールの発行をプロセス毎にカウント
```
sudo bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'
```


# openされたファイルの一覧と数
```
sudo bpftrace -e 'kprobe:do_sys_open { @[str(arg1)] = count(); }'
```

# ファイルをopenしたプロセ名とその回数
```
sudo bpftrace -e 'kprobe:do_sys_open { @[comm] = count(); }'
```

# IPで受信したインターフェース名を受信ごとに表示
```
sudo bpftrace -e 'kprobe:ip_rcv { printf("%s\n", str(arg1)); }'
```

# プロセスがファイルを開いたら確認
```
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s %s\n", comm, str(args->filename)); }'
```

tracepointはフォーマットを確認出来る．
```
$ sudo cat /sys/kernel/debug/tracing/events/syscalls/sys_enter_openat/format
name: sys_enter_openat
ID: 642
format:
        field:unsigned short common_type;       offset:0;       size:2; signed:0;
        field:unsigned char common_flags;       offset:2;       size:1; signed:0;
        field:unsigned char common_preempt_count;       offset:3;       size:1; signed:0;
        field:int common_pid;   offset:4;       size:4; signed:1;

        field:int __syscall_nr; offset:8;       size:4; signed:1;
        field:int dfd;  offset:16;      size:8; signed:0;
        field:const char * filename;    offset:24;      size:8; signed:0;
        field:int flags;        offset:32;      size:8; signed:0;
        field:umode_t mode;     offset:40;      size:8; signed:0;

print fmt: "dfd: 0x%08lx, filename: 0x%08lx, flags: 0x%08lx, mode: 0x%08lx", ((unsigned long)(REC->dfd)), ((unsigned long)(REC->filename)), ((unsigned long)(REC->flags)), ((unsigned long)(REC->mode))

```
