# Pythonでopen関数の引数にFalseが渡ったの動作

Pythonには組み込み関数でファイルを開くopen関数が存在する．
open関数は以下のような引数をもつ．

```python
open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
```

自分は，このopen関数の最初の引数であるfileにはファイルパスしか渡せないと思っていた．
しかし，公式ドキュメントには以下のように記述されている．
>file は:term:path-like object で、開くファイルの (絶対または現在のワーキングディレクトリに対する相対) パス名を与えるものか、または、ラップするファイルの整数のファイルディスクリプタです。(ファイルディスクリプタが与えられた場合は、それは closefd が False に設定されていない限り、返された I/O オブジェクトが閉じられるときに閉じられます。)

つまり，open関数の第一引数は，ファイルパスかファイルディスクリプタの番号になる．

ここで，open関数にFalseを渡した場合を考える．
```python
f = open(False, "r")
line = f.readline()
```

これはなぜかというと，Falseが整数型にキャストされるためである．
open関数の内部で，ファイルディスクリプタかファイルパスか判定するために，数値として取り扱えるかの確認を行っている．
そのタイミングで以下のようにFalseがintにキャストされる．

```python
int(False)
# => 0
```
こうなると，あとはopen関数にすう0番のファイルディスクリプタが渡された事になる．
つまり，標準入力がファイルディスクリプタに渡される．
例えば，PythonのREPLで以下のように実行することが出来る．
```consle
 $ python
Python 3.6.5 (default, Apr 20 2018, 15:25:53) 
[GCC 7.3.1 20180323 [gcc-7-branch revision 258812]] on linux
Type "help", "copyright", "credits" or "license" for more information.
>> f = open(False)
>> f.close()
>>> 
 $ 

```

標準入力を掴み，それをcloseする．
REPL上での標準入力は，キーボードであり，REPLの入力である．
よって，標準入力が閉じられたタイミングで，REPLも終了する．

また固定番のファイルディスクリプタは以下である．

| number |        |
|--------|--------|
|      0 | stdin  |
|      1 | stdout |
|      2 | stderr |


こういうなんとなく動作するミスって全然気付かないよね。
