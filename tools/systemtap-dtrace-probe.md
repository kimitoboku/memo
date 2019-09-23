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
