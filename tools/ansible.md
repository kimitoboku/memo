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
