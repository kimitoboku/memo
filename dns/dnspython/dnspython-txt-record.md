---
layout: post
title: dnspythonで255文字を超えたりするTXTレコード(DKIM)を扱う場合の注意点
---

[dnspython](http://www.dnspython.org/)はPythonでDNSを扱う上で，もっともよく使用されているライブラリだと思います．
普通にクエリを投げたりする場合には，特に問題にはならないのですが，dnspythonを用いてコンテンツサーバを作成する場合などに，一部，ひっかかってしまうような挙動があります．
今回実験したdnspythonのバージョンは以下の通りです．
```
$ pip freeze | grep dns
dnspython==1.16.0
```


具体的には以下の部分です．
- 255文字より長いテキストをホストしたい場合
- `;` が入っているTXTレコードをホストしたい場合

まぁ，具体的に言うと，DKIMを追加したい場合にハマったという所です．

まず，255文字より長いテキストをホストしたい場合は， `""` で255文字以下になるようにテキストを分割する必要があります，
```python
In [16]: print(dns.rdataset.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, 0, 'a'*255))
0 IN TXT "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

In [17]: print(dns.rdataset.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, 0, 'a'*256))
SyntaxError: string too long
```
と，255文字を超えるテキストを入れると，エラーになってしまいます．
そこで，DNSの一般的な対処法として，255文字以下を1つの文字列として `""` でくくります．
```python
In [20]: print(dns.rdataset.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, 0, f"\"{'a'*255}\" \"{'b'*255}\""))
0 IN TXT "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
```
このようにすれば，255文字を超えるテキストを1つのレコードとしてホスト出来ます．
[RFC4408](https://www.ietf.org/rfc/rfc4408.txt)にて，スペースで分割されたTXT Recordは連結して取り合うべきだということになっているので，信じて行きましょう．
[Can I have a TXT or SPF record longer than 255 characters? - BIND 9](https://kb.isc.org/docs/aa-00356)


続いて， `;` が入っているTXTレコードの問題です．
これはdnspythonが `;` を区切り文字の1つとして認識してるために発生する問題です．
具体的には， `；` を入力したい場合は以下のように `""` で囲わないと，末尾と認識されてその前のテキストまでがrdataとなります．
```python
In [21]: print(dns.rdataset.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, 0, 'aaa; bbb'))
0 IN TXT "aaa"

In [22]: print(dns.rdataset.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, 0, '"aaa; bbb"'))
0 IN TXT "aaa; bbb"

```
また，少し面白い挙動だと，ミスで2回 `""` で括った場合には，括ってない場合と同様の挙動にもなります，
```python
In [25]: print(dns.rdataset.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, 0, '""aaa; bbb""'))
0 IN TXT "" "aaa"
```

ということで，DKIMをdnspythonで追加したい場合は，以下のように指定しましょう．
```python
In [26]: print(dns.rdataset.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, 0, '"v=DKIM1;k=rsa;p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDwDc+AabcditzcdHYwOooW7HmqsPFzZUUb1nNqMj7ozyv/Q0WwwGJ+bdS4a9tO9roiT+VyyyMfIBoTdMNEWoXUMHafPgkOFPl5YO52pZM40bdXY/qtfT2nglJqS53zFFqB36q" "HoN9lgPRwP/e+ScCPlwHkcfIwD58ISU/lC5Bx+wIDAQAB"'))
0 IN TXT "v=DKIM1;k=rsa;p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDwDc+AabcditzcdHYwOooW7HmqsPFzZUUb1nNqMj7ozyv/Q0WwwGJ+bdS4a9tO9roiT+VyyyMfIBoTdMNEWoXUMHafPgkOFPl5YO52pZM40bdXY/qtfT2nglJqS53zFFqB36q" "HoN9lgPRwP/e+ScCPlwHkcfIwD58ISU/lC5Bx+wIDAQAB"
```
