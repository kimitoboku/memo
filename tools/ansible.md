---
layout: post
title: ansible
---

よく使われる構成管理ツール
初回のデプロイには便利だけど，その後の継続利用とかにはちょっと，何があるんじゃないかというお気持ち．

# よくつかうオプション
特定のホストにだけPlaybookを適応は `l` オプション
```
$ ansible-playbook playbook.yml -l TARGET_HOST
```

ステップ実行は `--step` (1つのtaskごとにy/nで実行するかどうかを確認出来る)
```
$ ansible-playbook playbook.yml --step
```

特定のtask移行を実行は `--start-at=` オプション
```
$ ansible-playbook playbook.yml --start-at="Task Name"
```


# Ansible Custom Moduleの作りかた
Ansibleを書いてて，宣言的にPlaybookとかRoleを作れないと分かったら，諦めて，Custom Moduleを書いた方がてっとり早いと思う．
Custom ModuleはPlaybookのymlファイルを配置するディレクトリに `library` というディレクトリを掘ってその中で配置する．
プログラムのファイル名がそのまま，AnsibleのCustom Module名になる．
```
$ tree .
├── README.md
├── ansible.cfg
├── inventories
├── library
│   └── hogehoge.py
├── requirements.txt
├── roles
└── playbook.yml
```


libraryの下でAnsibleModuleクラスを用いて，プログラムを作成する．
```
def main():
    module = AnsibleModule(
        argument_spec=dict(
            dns=dict(required=True),
            zone=dict(required=True),
            hogehoge=dict(required=False, type='bool', default=True),
        ),
        supports_check_mode=True
    )

    dns = module.params['dns']
    zone_name = module.params['zone']
    hogehoge = module.params['hogehoge']

    if module.check_mode:
        module.exit_json(changed=False)

    if hogehoge != True:
        module.fail_json(msg=f"Hogehoge is not true")
    module.exit_json(changed=True)

from ansible.module_utils.basic import AnsibleModule
if __name__ == "__main__":
    main()
```
これは，とくに何もないCustom Moduleだが，だいたいの使いかたはこれで分かると思う．
これを呼び出すば場合は以下のようにPlaybookで書く．
```yaml
- name: hogehoge
  hogehoge:
    dns: 8.8.8.8
    zone: exmaple.com.
- name: hogehoge?
  hogehoge:
    dns: 8.8.8.8
    zone: exmaple.com.
    hogehoge: False
```
また，このモジュールではAnsibleのModuleの `import` を `main` 関数の直前で行なっている．
```
from ansible.module_utils.basic import AnsibleModule
if __name__ == "__main__":
    main()
```
これは，AnsbileのCustoom Moduleはこの `import` 含めてサーバに持っていく時は，1つのファイルに埋め込まれて実行されるらしく，実際に実行する部分よりも上にあると，エラーなどの行番号がずれて，デバッグなどが行いにくくなるためらしい．


また，Custom Moduleでssh先のファイル操作などを行いたい場合もこの中で，普通にファイルの操作を行えばよい．
```
import json

def main():
    module = AnsibleModule(
        argument_spec=dict(
            dns=dict(required=True),
            zone=dict(required=True, type='dict'),
            config_path=dict(required=True, type='str')
        ),
        supports_check_mode=True
    )

    dns = module.params['dns']
    zone_config = module.params['zone']
    config_path = module.params['config_path']

    with open(config_path, 'w') as f:
        f.write(json.dumps(zone_config))
    module.exit_json(changed=True)

from ansible.module_utils.basic import AnsibleModule
if __name__ == "__main__":
    main()
```
Custom Moduleは基本的にターケットとなった環境で実行されるのでライブラリの確認とかは十全にやらないといけない．


# 先に実行されたタスクの実行結果がchangedの時にのみ実行する
Ansibleを書いてて， `shell` とかを使う時に実行するスクリプトファイルとかを `template` で生成した場合に，変更があった時だけ実行したいといった事が考えられる．
そのような場合には， `register` と `when` を使って実行結果を確認する．
```yaml
- name: Set hoge commands
  template:
    src: hoge.sh.j2
    dest: /tmp/hoge.sh
    mode: 0755
  register: hoge_scrpit

- name: Run hoge command
  shell: /tmp/hoge.sh
  when: hoge_script.changed
```
日本語で調べても地味にこれだけっていう情報が見付からなかった．
registerに入ってる値は以下のページで確認出来る．
- [Return Values — Ansible Documentation](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common)


# Custom Factsについて
Ansibleはホスト毎にユーザが保存した情報などを `Custom Facts` として，サーバマシンなどに保存し，次回の，Playbookの実行時にその値を読みだす機能がある．
`/etc/ansible/facts.d` に `json` 形式か `ini` 形式かを選択出来る．
構造化して使用したい場合には `json` しか選択肢がない．
`template` で `json` 生成するの辛い．
以下のようにPlaybookでディレクトリの作成と配置をする．
```yaml
- name: Create custom fact directory
  file:
    path: /etc/ansible/facts.d
    state: directory

- name: Set hoge fact
  template:
    src: hoge_data.fact.j2
    dest: "/etc/ansible/facts.d/hoge_data.fact"
```
多分しないとは思うけど(自分はしたんだけど)このfactファイルのパーミッションを下手にいじるとフォーマットエラーと言ってgathering facts中に落ちるので厳しい．
もっと，適当に答えて欲しい．

次回の実行からCustom Factsの中身は， `ansible_local` という変数から呼び出す事が出来るようになる．
今回の場合は `ansible_local.hoge_data` 以下に `json` の `Key-Value` で入ってるのでよしなに使えばよい．


# when と with_dict を同時に使う

条件分岐をしつつ，ループを実行出来る．
具体的には， `with_dict` が先に実行されて， `with_dict` のループの中で `when` が動くような感じ．
```
- debug:
    msg: "{{ item.key }}"
  with_dict:
  when: item.key == "hoge"
```

# 特権モードでの実行について
Ansibleでは特権モードでの実行には `become` を使用する．
[Understanding privilege escalation: become — Ansible Documentation](https://docs.ansible.com/ansible/latest/user_guide/become.html)

使用する方法としては，Playbookに直接書くか，task毎に書いていくかのどちらかになる．

Playbookでは以下のように書く
```yml
- hosts: test
  become: yes
  roles:
    - nsd
```

Taskでは以下のように書く
```yml
- name: Restart nsd service
  service:
    name: nsd
    state: restarted
  become: yes
```

基本的にはtask単位で書いた方が良いらしい．
特に，roleの再利用性を上げるには良い．

Roleの中で設定しておけば，Playbook側の書き方に依存せずに実行出来る可能性が上がる．

また， `become` と同時に `become_user` を設定する事で，実行するユーザも指定する事が出来る．
```yml
- name: Restart nsd service
  command: nsd-control restart
  become: yes
  become_user: nsd
```
こちらは基本的なパーミッション設定さえそれぞれのtaskでしていればあまり使用する機会はないが，上記のように特定のユーザでのみ実行出来るようなコマンドがある場合に使用する．

# 名前解決した結果のIPアドレスを挿入
Ansibleで名前解決した結果を元にtemplateなどを使用したい場合がある．
例えば，PromethuesのExpoterを配置したい時に，そのホストがPublic IPとPrivate IPアドレスを持っていて，Private IPアドレスだけでホストしたい場合などに使用する．

{% raw %}
```
{{ lookup('dig', ansible_host) }}
```
{% endraw %}

この `ansible_host` の部分は文字列でかまわない．
自分の場合はアクセスする時のホスト名に対応したIPアドレスを入れたかったから，こんな感じに書いた．

逆にPublic IPアドレスを書きたい場合などに，Publicなドメイン名から設定を入れてもよい．
ただ，この機能を使用するには `dnspython` をインストールする必要がある．



# ハンドラーをPlaybookの途中でエラーが発生しても実行する．

インストールスクリプトなどだと初回の実行順序的に必ずエラーが発生してしまい，notifyした，handlerが実行されない事があります．
その時に，Playbookの途中でエラーが発生した場合にも，notify先のhandlerを強制的に実行するオプションがあります．

Playbookのhostの中に `force_handlers: True` と記述すれば何がなんでもhandlerを動かしてくれる．

```
- hosts: test
  force_handlers: True
  become: yes
  roles:
    - nsd
```


# PlaybookからPlaybookを呼び出す
複数のホストなどがある場合に，後から特定のホストに対してタスクを実行させたい場合などを考えると便利．
全部のPlaybookを実行する `site.yml` などの中で `import_playbook` を使用して他のPlaybookを読みだし，，それぞれのPlaybookでホストやグループ，まとまり事にタスクを作っていく．
後から，特定のグループを追加する時や，使用しなくなった，playbookを削除していくのにも，分かりやすくて便利．

```yml:site.yml
- import_playbook: nsd.yml
- import_playbook: unbound.yml
- import_playbook: node_exporter.yml
```


# Playbookを1台が成功したら残りに対して実行するように設定する
同時に実行するマシンの指定にはPlaybookに `serial` という値を追加して指定する．
この `serial` は値か配列を受けとることが出来る．
値を受けとった場合にはその値の台数ずつ実行する．
配列を受け取った場合には，配列の順の台数ずつ実行し，それで終了しない場合には，配列の一番最後の要素だけ実行していく．
また，途中でtaskが失敗した場合には，以降の実行は中断される．
よって，これを用いることで，最初の1台が成功した場合に残りも実行という処理を行う事が出来る．

以下のように設定すると，1台を実行し，それが成功した場合に残りのホストに対して，並列に実行するようになる．
```yaml
- hosts: hoge
  become: yes
  serial:
    - 1
    - 100%
  roles:
    - hogehoge
```
