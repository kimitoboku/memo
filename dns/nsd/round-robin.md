---
layout: post
title: NSDで応答をラウンドロビンする
tags: nsd, DNS
---

DNSでロードバランスなどで負数のAレコードの応答を行う場合に，その応答をラウンドロビンして欲しい場合がある．
NSDでは昔はこの機能に対応する予定はないと言っていまいたが，現在は対応しています．
NSDにおけるラウンドロビンの設定は以下のように行います．
```
server:
    round-robin: yes
```
これで，返答されるレコードがラウンドロビンされます．
デフォルトでは `no` になっています．

ただ，NSDのラウンドロビンはレコードセット毎に行なわれるわけではないです．
NSDのラウンドロビンの実装は以下のようになっています． [^1]
```c
	static int round_robin_off = 0;
	int do_robin = (round_robin && section == ANSWER_SECTION &&
		query->qtype != TYPE_AXFR && query->qtype != TYPE_IXFR);
	uint16_t start;
	rrset_type *rrsig;

	assert(rrset->rr_count > 0);

	truncation_mark = buffer_position(query->packet);

	if(do_robin && rrset->rr_count)
		start = (uint16_t)(round_robin_off++ % rrset->rr_count);
	else	start = 0;
```
ラウンドロビンのループの回数のカウントは `rrset` の中ではなく， staticに `round_robin_off` の加算という形で行われています．
なので，同じレコードセットを連続して問合せても他の問合せが間に入る事で，ラウンドロビンを行なっていないように見えてしまう事があります．
まぁ，実際の所は誤差程度のものですが，知ってるとひっかかりにくくなるかなぁと思います．


[^1]: [nsd/packet.c at 70346a38458274a40c429f0b831b57ebebe6160b · NLnetLabs/nsd](https://github.com/NLnetLabs/nsd/blob/70346a38458274a40c429f0b831b57ebebe6160b/packet.c#L136-L148)
