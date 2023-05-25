---
layout: post
title: HAproxyが記録するtimestamp
---

HAPRoxyのlog formatではtimestampとして利用出来る変数が複数存在する。
しかし、それぞれの詳細な意味をDocumentでは記述していくれていないのでまとめる。

## `%t`
tcp modeのdefaultのlogで利用されいるtimestamp。

`accept_date` が挿入される。
- [haproxy/log.c at 535dd920df1d5ecb175270037276e1e1290cb992 · haproxy/haproxy](https://github.com/haproxy/haproxy/blob/535dd920df1d5ecb175270037276e1e1290cb992/src/log.c#L2236-L2243)

`accept_date` は、sessionが作成されたタイミングの時刻が入る。
- [haproxy/session.c at 535dd920df1d5ecb175270037276e1e1290cb992 · haproxy/haproxy](https://github.com/haproxy/haproxy/blob/535dd920df1d5ecb175270037276e1e1290cb992/src/session.c#L49)

session開始時のtimestampをログとして利用したい場合には、 `%t` を利用すると良い。


`%Ts` や `%ms` は `accept_date` を秒やミリ秒に変換した値をtimestampとして返す。
- [haproxy/log.c at 535dd920df1d5ecb175270037276e1e1290cb992 · haproxy/haproxy](https://github.com/haproxy/haproxy/blob/535dd920df1d5ecb175270037276e1e1290cb992/src/log.c#L2294C4-L2327)

`%T` は `accept_date` をGMTに変換した値をtimestampとして返す。
- [haproxy/log.c at 535dd920df1d5ecb175270037276e1e1290cb992 · haproxy/haproxy](https://github.com/haproxy/haproxy/blob/535dd920df1d5ecb175270037276e1e1290cb992/src/log.c#L2256C47-L2263)

`%Tl` は `accept_date` をlocal timeに変換した値をtimestampとして返す。
- [haproxy/log.c at 535dd920df1d5ecb175270037276e1e1290cb992 · haproxy/haproxy](https://github.com/haproxy/haproxy/blob/535dd920df1d5ecb175270037276e1e1290cb992/src/log.c#L2275C31-L2282)


## `%tr` 
HTTP Requestのdefaultのlogで利用されているtimestamp。

`accept_date` に `t_idle` と `t_handshake` が足された値をtimestampとして利用する。
- [haproxy/log.c at 535dd920df1d5ecb175270037276e1e1290cb992 · haproxy/haproxy](https://github.com/haproxy/haproxy/blob/535dd920df1d5ecb175270037276e1e1290cb992/src/log.c#L2245-L2254)

`t_idle` はHTTPのストリームが作成された時刻から `accept_ts` と `t_handshake` が引かれた値が入る。
- [haproxy/mux_h1.c at 535dd920df1d5ecb175270037276e1e1290cb992 · haproxy/haproxy](https://github.com/haproxy/haproxy/blob/535dd920df1d5ecb175270037276e1e1290cb992/src/mux_h1.c#L3019-L3020)

`t_handshake` はsessionの作成が完了した時刻から `accept_ts` が引かれた値が入る。
- [haproxy/session.c at 535dd920df1d5ecb175270037276e1e1290cb992 · haproxy/haproxy](https://github.com/haproxy/haproxy/blob/535dd920df1d5ecb175270037276e1e1290cb992/src/session.c#L470) 

`accept_ts` は `accept_date`　と同様にsessionが新規に作成された時刻が入る。
- [haproxy/session.c at 535dd920df1d5ecb175270037276e1e1290cb992 · haproxy/haproxy](https://github.com/haproxy/haproxy/blob/535dd920df1d5ecb175270037276e1e1290cb992/src/session.c#L50)

Sessionの確立が完全に終わった時刻のtimestampが欲しい場合は `%tr` を利用すると良い。

`%trl` と `%trg` はそれぞれ、`%tr` をlocal timeやGMTに変換した物なので、これらは保存したい日時に併せて利用すると良い。
- [haproxy/log.c at 535dd920df1d5ecb175270037276e1e1290cb992 · haproxy/haproxy](https://github.com/haproxy/haproxy/blob/535dd920df1d5ecb175270037276e1e1290cb992/src/log.c#L2284-L2292)
- [haproxy/log.c at 535dd920df1d5ecb175270037276e1e1290cb992 · haproxy/haproxy](https://github.com/haproxy/haproxy/blob/535dd920df1d5ecb175270037276e1e1290cb992/src/log.c#L2265-L2273)