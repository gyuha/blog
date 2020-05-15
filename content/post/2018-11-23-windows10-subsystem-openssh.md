---
title: "Windows 10 subsystem Ubuntu에서 ssh 설치 하기"
date: 2018-11-23T10:19:45+09:00
draft: true
categories: [os]
tags: [windows]
---

먼저 기존에 설치된 openssh를 삭제하고 다시 설치해야 합니다.
<!--more-->

그리고, sshd_config에서 port를 22번 말고 다른 포트로 변경해 줘야 합니다.

기본으로는 `Port 22`는 주석처리 되어 있습니다. 주석처리를 지우고 변경합니다.

이유는,  윈도우에서 이미 22번 포트를 사용하고 있기 때문입니다. 만약에 꼭 22번을 쓰고 윈도우에서 사용하는 22번 포트를 disable하고 써야 합니다.

정리하면 아래와 같습니다.

```bash
sudo apt-get remove --purge openssh-server
sudo apt-get install openssh-server
sudo vi /etc/ssh/sshd_config # Change Port from 22 to 222 
sudo service ssh --full-restart
```

