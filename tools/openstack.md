---
layout: post
---

OpenStackのCLIのやつ．
OpenStack自体はToolじゃない所に書くがそのうちやいのやいのする．

## IPアドレスからBindしてるPortの情報を所得．
```
$ openstack port list --fixed-ip ip-address=192.1.2.1
```
これで得られたPort IDで見る．
```
$ openstack port show {port id}
```

まとめるとこんな感じ
```
$ openstack port show $(openstack port list --fixed-ip ip-address=192.1.2.1 -f value -c ID)
```



## 設定の読み込み
openstackコマンドは `$HOME/.config/openstack/clouds.yml` や環境変数を読み込んで，アカウントや実行対象のリージョンを指定出来る．
自分は切り替えに便利なので，環境変数を指定している．
以下のようなシェルスクリプトを用意して，操作するリージョンに応じて読み込んでる．
本当はこれらを良い感じに設定ファイルからよみこむようなのを作ってさくさく切り替えたいけど，それだとほとんど， `clouds.yml` でよくないかという気がするので考えなかった事にする．
```shell
if [ -v _OLD_VIRTUAL_PS1 ]; then
    deactivate_openstack
fi


export OS_AUTH_URL=""
export OS_IDENTITY_API_VERSION=""
export OS_PASSWORD=""
export OS_PROJECT_DOMAIN_NAME=""
export OS_PROJECT_NAME=""
export OS_REGION_NAME=""
export OS_USER_DOMAIN_NAME=""
export OS_USERNAME=""
export LOCAL_OS_TOKEN=$(openstack token issue --format value --column id)
alias curl='curl -H "X-Auth-Token: $LOCAL_OS_TOKEN"'

_OLD_VIRTUAL_PS1="${PS1:-}"
export PS1="(OS $OS_REGION_NAME) ${PS1:-}"

deactivate_openstack () {
    if [ -n "${_OLD_VIRTUAL_PS1:-}" ] ; then
        PS1="${_OLD_VIRTUAL_PS1:-}"
        export PS1
        unset _OLD_VIRTUAL_PS1
    fi
    unset OS_AUTH_URL
    unset OS_IDENTITY_API_VERSION
    unset  OS_PASSWORD
    unset OS_PROJECT_DOMAIN_NAME
    unset OS_PROJECT_NAME
    unset OS_REGION_NAME
    unset OS_USER_DOMAIN_NAME
    unset OS_USERNAME
    unset LOCAL_OS_TOKEN
    unalias curl
    unset deactivate_openstack
}
```
