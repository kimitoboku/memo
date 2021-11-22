---
layout: post
title: KVMまわりの使い方
---


# KVMの準備
```
sudo yum install libvirt libvirt-client qemu-kvm-ev virt-manager virt-top virt-viewer virt-install bridge-utils libguestfs-tools-c
sudo systemctl start libvirtd
```


# default ネットワークの削除
普通にVMを作成して動作させるだけならば、default networkを使っても良いが、dnsmasqが動いたりしてちょっと面倒なので、削除しておく。
```
sudo virsh net-destroy --network default
```


# VMの起動/削除
VMの起動は多くの場合は、define xmlを書いて行う。
```
: 起動
sudo virsh define /path/to/define.xml

: 削除
sudo virsh destroy /path/to/define.xml
```

## define xml
基本的には以下のような感じで書いておけば良い。
Nameは分かりやすいように。UUIDは被らないように設定する。
MemoryとCPUに関しては使いたいだけ使う。
```
<domain type='kvm'>
  <name>instance-name</name>
  <uuid>03035244-4b6b-11ec-81d3-0242ac130003</uuid>
  <memory unit='KiB'>1000000000</memory>
  <currentMemory unit='KiB'>1000000000</currentMemory>
  <vcpu placement='static'>4</vcpu>
  <os>
    <type arch='x86_64' machine='pc-i440fx-rhel7.0.0'>hvm</type>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
  </features>
  <cpu mode="host-passthrough" match="exact">
  </cpu>
  <clock offset='utc'>
    <timer name='rtc' tickpolicy='catchup'/>
    <timer name='pit' tickpolicy='delay'/>
    <timer name='hpet' present='no'/>
  </clock>
  <devices>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='{{ vm_image_path }}/{{ vm_image_name }}'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <controller type='virtio-serial' index='0'></controller>
    <console type='pty'>
      <target type='serial' port='0'/>
    </console>
    <channel type='unix'>
      <target type='virtio' name='org.qemu.guest_agent.0'/>
      <address type='virtio-serial' controller='0' bus='0' port='1'/>
    </channel>
    <video>
      <model type="cirrus"/>
    </video>
  </devices>
</domain>
```

### ネットワークデバイス
libvirtdが管理しているnetworkを利用したい場合には `device` に type が `network` の `interface` を追加する。
```
  <devices>
    <interface type='network'>
      <source network='default'/>
      <model type='virtio'/>
    </interface>
  </devices>
```
また、さらに細かく設定したい場合には、以下ようにIPアドレスや、MACアドレスなど、ネットワークの設定に応じて設定する事も出来る。
IPアドレスだけだとかMACアドレスだけといった設定も出来る。
```
  <devices>
    <interface type='network'>
      <source network='default'/>
      <model type='virtio'/>
      <mac address='00:00:5e:00:53:01'/>
      <ip address='192.168.122.1' netmask='255.255.255.0'>
    </interface>
  </devices>
```


また、networkではなく、type ethernetを利用する事でより柔軟にコントロールも出来る。
以下のように `type` が `ethernet` となったインターフェースも追加する事が出来る。
```
  <devices>
    <interface type="ethernet">
      <model type="virtio"/>
      <driver name="vhost">
      </driver>
      <script path=""/>
      <target dev='tap-name'/>
      <mac address='00:00:5e:00:53:03'/>
    </interface>
  </devices>
```
このインターフェースを追加すると、VMのインターフェースに1対1対応する、 target devに指定されたtapがHV上に作成されて通信が可能になる。
ただ、 `ethernet` ではIPアドレスの指定などが出来ないため、そのハンドリングを行う必要がある。
具体的には、dnsmasqを用いてDHCPでVMにIPアドレスを採番するか、ConsoleでログインしてIPアドレスを手動で割り当てる必要がある。
より柔軟にコントロール出来るため、OpenStackなどでは基本的に `ethernet` が用いられる。

# VMへのConsole経由の接続
ネットワークから接続出来る場合には必要ないが、まぁ、往々にして、ネットワークの設定は失敗するので、Consoleからのアクセスも必要
```
sudo virsh console --domain instance-name
```
