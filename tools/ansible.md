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
from ansible.module_utils.basic import AnsibleModule

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
