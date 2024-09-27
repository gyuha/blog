---
title: "우분투 노트북 서버 사용시 커버를 덮어도 잠들지 않도록 하기"
date: 2019-01-04T10:23:04+09:00
draft: true
categories: [system]
tags: [ubuntu,laptop,server]
---

먼저 터미널에서 아래와 같은 파일을 열어 줍니다.
<!--more-->

```bash
sudo vi /etc/systemd/logind.conf
```



파일에서 `#HandleLidSwitch=suspend`로 되어 있는 곳의 샵(#) 주석을 제거 하고 `HandleLidSwitch=ignore` 이렇게 변경해 줍니다.

```ini
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.
#
# Entries in this file show the compile time defaults.
# You can change settings by editing this file.
# Defaults can be restored by simply deleting this file.
#
# See logind.conf(5) for details.

[Login]
#NAutoVTs=6
#ReserveVT=6
#KillUserProcesses=no
#KillOnlyUsers=
#KillExcludeUsers=root
#InhibitDelayMaxSec=5
#HandlePowerKey=poweroff
#HandleSuspendKey=suspend
#HandleHibernateKey=hibernate
HandleLidSwitch=ignore
#HandleLidSwitchDocked=ignore
#PowerKeyIgnoreInhibited=no
#SuspendKeyIgnoreInhibited=no
#HibernateKeyIgnoreInhibited=no
#LidSwitchIgnoreInhibited=yes
#HoldoffTimeoutSec=30s
#IdleAction=ignore
#IdleActionSec=30min
#RuntimeDirectorySize=10%
#RemoveIPC=yes
#InhibitorsMax=8192
#SessionsMax=8192
#UserTasksMax=33%
```



그리고 서비스를 재실행 해 줍니다.

```bash
systemctl restart systemd-logind.service
```

