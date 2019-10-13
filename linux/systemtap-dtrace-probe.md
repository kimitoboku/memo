# SystemTapでDtraceのプローブが入ったソースコードをコンパイル

dtraceのプローブが付いたプログラムをLinuxでビルドするにはSystemTapを用いる。
以下のようなdtrace向けのプログラムを用意する。
```c
#include<stdio.h>
#include "provider.h"


int main() {
    int val;
    scanf("%d", &val);
    DTRACE_PROBE1(my_prob, start__process__val, val);
    val *= 2;
    val += 1;
    DTRACE_PROBE1(my_prob, end__process__val, val);
    printf("%d\n", val);
    return 0;
}
```

また、以下のようなdtrace向けのプローブの定義ファイルも用意する。
```
provider my_prob {
    probe start__process__val(int);
    probe end__process__val(int);
};
```

SystemTapを用いてこれをビルドする。
```
$ sudo zypper install systemtap-sdt-devel
$ dtrace -C -h -s provider.d -o provider.h
$ gcc -c my_prob.c -o my_prob.o
$ dtrace -C -G -s provider.d -o provider.o my_prob.o
$ gcc -o my_prob my_prob.o provider.o
$ /usr/share/bcc/tools/tplist -l ./my_prob
b'./my_prob' b'my_prob':b'start__process__val'
b'./my_prob' b'my_prob':b'end__process__val'
$ 
```

`systemtap-sdt-devel` をインストールすると、dtraceコマンドと `/usr/include/sys/sdt.h` など dtraceの互換レイヤーもインスト−ルされる。
それらを用いてビルドすると、LinuxではeBPFなどでアタッチ出来るUSDTプローブ付きでビルドすることが出来る。


ソースコードは以下のページにある。
[GitHub - kimitoboku/usdt_example](https://github.com/kimitoboku/usdt_example)



# PostgreSQLをUSDTプローブ付きでビルドする
PostgreSQLもdtraceのプローブを提供しているので同様にSystemTapでビルドすることが出来る。

```
$ sudo zypper install systemtap-sdt-devel
$ git clone https://github.com/postgres/postgres.git
$ cd postgres
$ ./configure --enable-dtrace --enable-debug
$ make
$ sudo make install 
$ sudo /usr/share/bcc/tools/tplist -l /usr/local/pgsql/bin/postgres
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'clog__checkpoint__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'clog__checkpoint__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'multixact__checkpoint__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'multixact__checkpoint__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'subtrans__checkpoint__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'subtrans__checkpoint__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'twophase__checkpoint__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'twophase__checkpoint__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'transaction__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'transaction__commit'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'transaction__abort'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'wal__buffer__write__dirty__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'wal__buffer__write__dirty__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'wal__switch'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'checkpoint__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'checkpoint__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'wal__insert'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'statement__status'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'buffer__flush__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'buffer__flush__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'buffer__read__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'buffer__read__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'buffer__write__dirty__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'buffer__write__dirty__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'buffer__sync__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'buffer__sync__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'buffer__sync__written'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'buffer__checkpoint__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'buffer__checkpoint__sync__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'buffer__checkpoint__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'lock__wait__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'lock__wait__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'deadlock__found'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'lwlock__wait__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'lwlock__wait__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'lwlock__acquire'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'lwlock__condacquire'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'lwlock__condacquire__fail'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'lwlock__acquire__or__wait'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'lwlock__acquire__or__wait__fail'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'lwlock__release'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'smgr__md__read__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'smgr__md__read__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'smgr__md__write__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'smgr__md__write__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'query__parse__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'query__parse__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'query__rewrite__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'query__rewrite__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'query__plan__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'query__plan__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'query__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'query__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'query__execute__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'query__execute__done'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'sort__start'
b'/usr/local/pgsql/bin/postgres' b'postgresql':b'sort__done'
```


