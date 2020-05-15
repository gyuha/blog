---
title: "Ubuntu 18.04에서 netplan을 사용한 static ip 설정"
date: 2019-01-04T10:30:30+09:00
draft: true
categories: [system]
tags: [ubuntu,setting]
---

17.10부터 네트워크 인터페이스 설정이 `netplan`이라는 새로운 네트워크 설정이 생겼다. 기존에 인터페이스 설정(/etc/network/interfaces)보다는 간결해 보입니다. 
<!--more-->



변경 할 파일은 아래와 같습니다.

```bash
sudo vi /etc/netplan/50-cloud-init.yaml
```



기본적으로 dhcp로 설치 했을 경우 아래와 같이 나옵니다.

```yml
network:
    ethernets:
        enp4s0f2:
        	addresses: []
            dhcp4: true
   version: 2
```



그 내용을 아래와 같이 ip와 정보를 넣고 설정 해 주면 됩니다.

```yml
network:
    ethernets:
        enp4s0f2:
            dhcp4: no
            addresses: [192.168.1.200/24]
            gateway4: 192.168.1.1
            nameservers:
                    addresses: [1.1.1.1,8.8.8.8,8.8.4.4]
    version: 2

```

그리고 변경 된 내용을 아래와 같이 적용 합니다.

```bash
sudo netplan apply
```



변경된 내용을 `ifconfig`로 확인 하면 됩니다.

```bash
$ ifconfig
enp4s0f2: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.200  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::290:f5ff:fee7:6e10  prefixlen 64  scopeid 0x20<link>
        ether 00:90:f5:e7:6e:10  txqueuelen 1000  (Ethernet)
        RX packets 89208  bytes 132983451 (132.9 MB)
        RX errors 0  dropped 9  overruns 0  frame 0
        TX packets 55318  bytes 4234704 (4.2 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 252  bytes 19812 (19.8 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 252  bytes 19812 (19.8 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```



그런데.. dhcp4가 `true`이다가.. 끌때는 `no`로 변경 되어서.. 오타인가 찾아 봤는데..

모두 그렇게 사용하고 있네요.. 흠.....

이상하지만 잘 동작 합니다. -_-;;;

