---
title: "우분투 18.04에서 kimchi 설치 하기"
date: 2019-01-04T17:04:32+09:00
draft: true
categories: [system]
tags: [kvm,kimchi,ubuntu,setting]
---

## Bridge Network 설치하기

전 kvm을 개발로 쓰면서 bridge network 형태로 자주 사용해서 먼저 bridge network를 설정 해 줍니다.
<!--more-->

kimchi를 설치 이후에 설정으로 추가해 주면... 문제가 발생하면서 네트워크가 불능이 되어 버립니다.

그래서 미리 설정을 해 줍니다.

먼저 bridge-utils를 설치 해 줍니다.

```bash
sudo apt install bridge-utils
```



그리고, `/etc/netplan/50-cloud-init.yaml`을 수정해 줍니다.

```bash
sudo vi /etc/netplan/50-cloud-init.yaml
```

아래와 같이 입력 합니다.

```yaml
network:
    ethernets:
        enp3s0:
            dhcp4: false
    bridges:
        br0:
            interfaces:
                - enp3s0
            dhcp4: false
            addresses:
            - 192.168.1.200/24
            gateway4: 192.168.1.200
            nameservers:
                addresses:
                - 1.1.1.1
                - 8.8.8.8
            parameters:
                forward-delay: 0
                stp: false
            optional: true
    version: 2
```

입력한 내용을 적용 합니다.

```bash
sudo netplan apply
```

이제 네트워크에 잘 적용이 되었는지 확인 합니다.

```bash
$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
5: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 4e:6a:7f:1e:e0:0e brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.200/24 brd 192.168.1.255 scope global br0
       valid_lft forever preferred_lft forever
    inet6 fe80::4c6a:7fff:fe1e:e00e/64 scope link
       valid_lft forever preferred_lft forever
6: wlp3s0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 6c:71:d9:9a:4b:3b brd ff:ff:ff:ff:ff:ff
7: enp4s0f2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel master br0 state UP group default qlen 1000
    link/ether 00:90:f5:e7:6e:10 brd ff:ff:ff:ff:ff:ff

```



## Kimchi 설치하기

먼저 업데이트 할꺼와 업그레이드 할 꺼를 해 줍니다.

```bash
sudo apt update && sudo apt upgrade -y
```



그리고 KVM을 설치하고 Kimchi와 Wok이 필요로 하는 패키지들을 설치해 줍니다. 

```bash
sudo apt install qemu qemu-kvm libvirt-bin \
python-paramiko python-pil novnc python-libvirt \
python-ethtool python-ipaddr python-guestfs \
libguestfs-tools spice-html5 spice-html5 \
python-magic keyutils libnfsidmap2 \
libtirpc1 nfs-common rpcbind python-configobj \
python-parted -y
```



혹시 패키지를 찾지 못한다면 Universe 저장소를 활성화 해 줘야 합니다.

```bash
sudo add-apt-repository universe
```



KVM 설치를 확인 합니다.

```bash
$ kvm-ok
INFO: /dev/kvm exists
KVM acceleration can be used
```

정상적으로 설치가 되었다면 위와 같은 메시지가 나옵니다.

nginx를 설치 합니다.

```bash
sudo apt install nginx -y
```



Kimchi의 최신 설치파일을 받아 옵니다.

```bash
$ wget https://github.com/kimchi-project/kimchi/releases/download/2.5.0/wok-2.5.0-0.noarch.deb
$ wget https://github.com/kimchi-project/kimchi/releases/download/2.5.0/kimchi-2.5.0-0.noarch.deb
```



먼저 wok을 설치를 합니다.

```bash
$ sudo dpkg -i wok-2.5.0-0.noarch.deb
$ sudo apt install -f -y
```

그리고, Kimchi를 설치 합니다. 그런데 그냥 설치 하면 `python-imaging`에서 문제가 발생 합니다. 그래서 python-imaging을 depends에서 제외하고 설치를 해 줍니다.

```bash
$ sudo dpkg --ignore-depends=python-imaging -i kimchi-2.5.0-0.noarch.deb
```



만약에 UFW를 사용 한다면, 8001번 포트를 열어 줍니다.

```bash
$ sudo ufw allow 8001/tcp
```

설치가 되었다면 재부팅해 줍니다.

```bash
$ sudo reboot
```



### Kimchi 패키지 종속 문제 해결하기

우선 kimchi에서 python-imaging을 제거 해 줘야 합니다. 여기서는 python-imaging을 python-pil을 대체해 줍니다.

먼저 아래와 같이 편집기를 띄워 줍니다.

```
$ sudo vi /var/lib/dpkg/status
```

`/var/lib/dpkg/status` 파일에서 `package: kimchi`를 검색해 보면...

```ini
Package: kimchi
Status: install ok installed
Priority: optional
Section: base
Maintainer: Aline Manera <alinefm@br.ibm.com>
Architecture: all
Version: 2.5.0
Depends: wok (>= 2.1.0), python-imaging, python-configobj, novnc, python-jsonschema (>= 1.3.0), python-libvirt, gettext, libvirt-bin, nfs-common, qemu-kvm, python-parted, python-psutil (>= 0.6.0), python-ethtool, sosreport, python-ipaddr, python-lxml, open-iscsi, python-guestfs, libguestfs-tools, spice-html5, python-magic, python-paramiko
Description: Kimchi web application
Build-Depends: xsltproc,
               gettext,
               python-lxml

```

Depends에 보시면, `python-imaging`이라고 되어 있습니다. 이걸 `python-pil`로 변경해 줍니다.

웹 브라우저에서 

> https://[서버 IP]:8001

로 접속을 해 접속 해 봅니다. 꼭 `https`로 해야 접속이 됩니다. `http`를 하면 400번 에러만 보게 됩니다.

웹 브라우저에서 보안상 어쩌구 해서 무시하고 처음 접속을 하면 되면 8010포트로 이동을 하게 됩니다.

이때는 그냥.. 살며시 무시하고 url의 포트를 8001로 변경 해 주세요.

그리고 나면 Wok을 로그인 하면이 나옵니다.

여기서 사용자의 이름은 패스워드는 우분투의 계정을 넣어 주시면 됩니다.



여기까지 하면 한 고비를 남겨서 잘 동작하는 화면을 볼 수 있습니다.



## Ubuntu 18.04 서버 설치 하기

먼저 ubuntu 18.04의 이미지를 받아 줍니다.

```bash
$ cd /var/lib/kimchi/isos
$ sudo wget http://releases.ubuntu.com/18.04.1/ubuntu-18.04.1-live-server-amd64.iso
```

이미지가 다 받아 지면 `Vitualization` > `Templates` 에서 `+ Add Template` 버튼을 누르면 제일 처음에 Ubuntu 18.04가 보입니다.

하지만, 아직 이미지를 쓰진 못 합니다. ㅜ.ㅜ

> KCHTMPL0020E: Unable to create template due error: KCHIMG0001E: Error 
> probing image OS information: part_list: parted print: /dev/sda: 
> Warning: The driver descriptor says the physical block size is 2048 
> bytes, but Linux says it is 512 bytes.



#### Ubuntu 18.04 이미지 오류 수정하기

이미지를 템플릿으로 추가 하려면 위와 같이 메시지가 나옵니다.

여기서 다시 편집이 들어가야 합니다.

```bash
$ sudo vi /usr/lib/python2.7/dist-packages/wok/plugins/kimchi/model/templates.py
```



먼저 아래와 같은 라인을 찾습니다. 제가 쓰는 버전에서는 42라인입니다.

```python
ISO_TYPE = "ISO 9660 CD-ROM"
```

이걸 아래와 같이 변경해 줍니다.

```python
ISO_TYPE = ["DOS/MBR", "ISO 9660 CD-ROM"]
```



그리고  다시 아래와 같은 줄을 찾아 줍니다.

```python
        if ISO_TYPE in ftype:
```

위 라인을 아래와 같이 바꿔 줍니다.

```python
        iscdrom = [t for t in ISO_TYPE if t in ftype]
        if iscdrom:
```

여기서 수정 할 때 주의 해야 할 점은 python이라서 공백에 민감합니다. 꼭 공백을 맞춰서 넣어 주세요.

python을 약간만 보셨다면 어렵지 않게 하실 수 있을 겁니다.



그리고 재부팅을 해 줍니다.

```bash
$ sudo reboot
```



## 포트를 443으로 변경해 주기

인증서는 없지만, 그래도 443으로 변경해 주면 포트를 안 써줘도 되니.. 변경 해 줍니다.



#### Nginx 설정 변경하기

```bash
$ sudo vi /etc/nginx/conf.d/wok.conf
```

아래과 같은 2라인을  찾습니다.

```ini
....
listen 0.0.0.0:8001 ssl;
....
proxy_redirect http://127.0.0.1:8010/ https://$host:8001/;
....
```

내용을 아래와 같이 변경 합니다.

```ini
....
listen 0.0.0.0:443 ssl;
....
proxy_redirect http://127.0.0.1:8010/ https://$host:443/;
....
```



#### Wok 설정 변경하기

```bash
$ sudo vi /etc/wok/wok.conf
```

아래과 같은 라인을 찾습니다.

```ini
....
#proxy_port = 8001
....
```

아래과 같이 변경 해 줍니다.

```ini
....
proxy_port = 443
....
```



## 참고

* [Ubuntu server 18.04 as a Hypervisor using KVM and Kimchi for VM Management](http://www.ubuntuboss.com/ubuntu-server-18-04-as-a-hypervisor-using-kvm-and-kimchi-for-vm-management/)
* [Ubuntu 18.04 Server + LXDでブリッジ接続する](https://qiita.com/330k/items/9ef10da53fa9dfb1e1a9)