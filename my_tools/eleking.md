# eleking
[tldr](https://github.com/tldr-pages/tldr) をターミナルで表示するためのツール。
オフラインで実行出来るツールが当時無かったので作った。

`go get` でインストールする。
```
$ go get github.com/kimitoboku/eleking
```

デフォルトでは、tldrのリポジトリを見に行く
```
$ eleking tar
https://raw.github.com/tldr-pages/tldr/master/pages/common/tar.md
tar
 Archiving utility.
 Optional compression with gzip / bzip.
 Create an archive from files:
  tar cf target.tar file1 file2 file3

 Create a gzipped archive:
  tar czf target.tar.gz file1 file2 file3

 Extract an archive in a target folder:
  tar xf source.tar -C folder

 Extract a gzipped archive in the current directory:
  tar xzf source.tar.gz

 Extract a bzipped archive in the current directory:
  tar xjf source.tar.bz2

 Create a compressed archive, using archive suffix to determine the compression program:
  tar caf target.tar.xz file1 file2 file3

 List the contents of a tar file:
  tar tvf source.tar
```

設定ファイルを見るとオフラインで確認出来る。
```
$ mkdir $HOME/.config/tldr
$ cd $_
$ git clone https://github.com/tldr-pages/tldr.git
$ vim config.json
{
    "Documetns": ["dir/md/path", "/home/example/.config/tldr/tldr/pages/linux"]
}
$ eleking ls
ls
 List directory contents.
 List files one per line:
  ls -1

 List all files, including hidden files:
  ls -a

 Long format list (permissions, ownership, size and modification date) of all files:
  ls -la

 Long format list with size displayed using human readable units (KB, MB, GB):
  ls -lh

 Long format list sorted by size (descending):
  ls -lS

 Long format list of all files, sorted by modification date (oldest first):
  ls -ltr
```
一応、カラーリングリングもするようになってるけど、色は自分のターミナルに併せてあるので、自分用。
