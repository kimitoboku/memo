---
layout: post
title: retryライブラリの使い方
---

Pythonで関数のリトライ処理を実行したくなったので，retry [^1] というライブラリを使い方を調べながら使った．
簡単に書けるし，リトライの制御をexceptionで出来るしめちゃくちゃ好みのライブラリだった．

## 簡単な使い方
自分が知りたかったのをまとめる

### 成功するまでリトライする
```python

import random

from retry import retry

@retry()
def retry_func():
    if random.random() > 0.5:
        retrun
    else:
        raise Exception


if __name__ = "__main__":
    retry_func()
```


### 特定の例外のみリトライする
```python

import random

from retry import retry

class ExceptionA(Exception):
    pass

class ExceptionB(Exception):
    pass


@retry(exceptions=(ExceptionA))
def retry_func():
    if random.random() > 0.5:
        raise ExceptionA
    elif random.random() > 0.3:
        raise ExceptionA
    else:
        retrun


if __name__ = "__main__":
    retry_func()
```

`ExceptionA` が来た時だけリトライする．
`exceptions` はタプルを引数にとるので，複数の例外でリトライしたい時にはタプルに入れていこう．


### 特定の回数までリトライスル

```python

import random

from retry import retry

class ExceptionA(Exception):
    pass

class ExceptionB(Exception):
    pass


@retry(exceptions=(ExceptionA), tries=3)
def retry_func():
    if random.random() > 0.5:
        raise ExceptionA
    elif random.random() > 0.3:
        raise ExceptionA
    else:
        retrun


if __name__ = "__main__":
    retry_func()
```

これで3枚までリトライしてくれる．


### リトライするのにちょっと待つ

```python

import random

from retry import retry

class ExceptionA(Exception):
    pass

class ExceptionB(Exception):
    pass


@retry(exceptions=(ExceptionA), tries=3， delay=1)
def retry_func():
    if random.random() > 0.5:
        raise ExceptionA
    elif random.random() > 0.3:
        raise ExceptionA
    else:
        retrun


if __name__ = "__main__":
    retry_func()
```


`delay` を使えば再試行をまってくれる．
単位は秒


### ディレイとかを引数で決めたい．

```python

import random

from retry import retry

class ExceptionA(Exception):
    pass

class ExceptionB(Exception):
    pass


def retry_func(retry_num, delay_time):

    @retry(exceptions=(ExceptionA), tries=retry_num， delay=delay_time)
    def retry_func():
        if random.random() > 0.5:
            raise ExceptionA
        elif random.random() > 0.3:
            raise ExceptionA
        else:
            retrun

    return retry_func()


if __name__ = "__main__":
    retry_func()
```
関数の中で関数作れば良いよ，


[^1]: [retry · PyPI](https://pypi.org/project/retry/)
