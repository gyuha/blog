---
title: "윈도우용 패키지 매니저 Chocolatey 사용법"
date: 2020-01-10T03:03:39+09:00
draft: true
categories: [utillity]
tags: [windows,package,manager, choco]
---

Chocolatey는 윈도우용 패키지 매니저로, 설치하려는 윈도우용 소프트웨어를 일일이 웹사이트에서 찾아서 설치할 필요 없이 간단하게 커맨드 만으로 윈도우용 소프트웨어를 설치 할 수 있게 해 줍니다.
<!--more-->

## Chocolatey 설치

chocolate를 설치 하려면 관리자 권한 cmd나 PowerShell을 실행해서 설치를 해 줘야 합니다.

## cmd 사용시

```bash
@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin
```



## powershell 사용시

```bash
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```



## 패키지  찾기

아래 웹페이지에 접속해서 검색하시면 됩니다.

>  https://chocolatey.org/packages

또는 cmd에서 `search` 나  `list` 명령어로 검색을 할 수 있습니다. 

```bash
> choco search googlechrome
Chocolatey v0.10.15
GoogleChrome 79.0.3945.117 [Approved] Downloads cached for licensed users
vivaldi.install 2.10.1745.23
... 생략
10 packages found.
```

예로 구글크롬 웹브라우저를 검색해 보면  10개의 패키지가 나옵니다. 그냥 chrome을 검색하면 백여개가 넘는 패키지가 목록이 나오게 됩니다.

여기서 정확하게 필요한 패키지만을 보기 위해서는 `-e` 또는 `--exact` 옵션을 넣어 줘야 합니다.

```bash
> choco search googlechrome -e
Chocolatey v0.10.15
GoogleChrome 79.0.3945.117 [Approved] Downloads cached for licensed users
1 packages found.
```

그리고, 간혹 특정 버전의 패키지를 설치 해야 할 경우가 있습니다. 그럴 경우 버전을 확인하기 위해서는 `-a`, `--all`  옵션을 넣어 주면 버전 정보를 확인 할 수 있습니다.



## 패키지 상세 정보 보기

`info` 명령어을 사요하거나 search에서 `-v`옵션을 추가해 주면 됩니다. 

그런데 `info` 명령어 search에서 -e 옵션이 붙은 것처럼 동작을 하게 됩니다.

```bash
> choco info googlechrome
Chocolatey v0.10.15
GoogleChrome 79.0.3945.117 [Approved] Downloads cached for licensed users
 Title: Google Chrome | Published: 2020-01-07
 Package approved as a trusted package on 1 08 2020 01:22:22.
... 생략
```

또는

```bash
> choco search googlechrome -ev
Chocolatey v0.10.15
GoogleChrome 79.0.3945.117 [Approved] Downloads cached for licensed users
 Title: Google Chrome | Published: 2020-01-07
 Package approved as a trusted package on 1 08 2020 01:22:22.
... 생략
```

여기서 `-ev` 로 옵션을 줬는데, 이건 `-e -v`를 하나로 요약한 형식입니다.



## 패키지 설치 하기

`install` 명령을 이용해서 설치하고 싶은 패키지를 아래와 같이 설치 합니다.

```bash
> choco install bandizip
Chocolatey v0.10.15
Installing the following packages:
bandizip
... 생략
Note: If you don't run this script, the installation will fail.
Note: To confirm automatically next time, use '-y' or consider:
choco feature enable -n allowGlobalConfirmation
Do you want to run the script?([Y]es/[A]ll - yes to all/[N]o/[P]rint):
```

명령어 프롬프트가 나오면 y를 눌러주면 간단하게 설치가 완료 됩니다.

설치 시 자동으로 y를 누르고 싶다면 `-y` 옵션을 넣어 주면 됩니다. 그리고 강제로 설치하고 싶다면 `-f`를 넣어 주면 됩니다.

```bash
> choco install -yf bandizip
```



혹시 특정 버전을 설치하고 싶다면 `--version` 옵션을 이용해서 해당 버전을 설치 할 수 있습니다.

```bash
choco install bandizip --version=6.24
```



## 패키지 삭제 하기

chocolatey는 설치된 패키지도 `uninstall` 명령어를 이용해서 편하게 삭제가 가능 합니다.

```bash
> choco uninstall bandizip
Chocolatey v0.10.15
Uninstalling the following packages:
bandizip
... 생략
Do you want to run the script?([Y]es/[A]ll - yes to all/[N]o/[P]rint): 
```

명령어 프롬프트가 나오면 y를 눌러주면 삭제가 됩니다.

`y`키를 누르기 귀찮다면 설치 할 때와 같이 `-yf`를 누르시면 바로 삭제가 가능 합니다.

```bash
> choco uninstall -yf bandizip
```



## choco로 설치된 패키지 목록 확인하기

`search` 또는 `list`명령로 확인 가능 합니다. 뒤에 `-l` 옵션을 주면 로컬에 설치된 패키지의 목록을 출력 해 줍니다.

```bash
> choco search -l
bandizip 6.25
... 생략
zeal 0.6.1
zeal.install 0.6.1
62 packages installed.
```

또는 `clist` 명령어를 사용해서도 조회가 가능 합니다.

```bash
> clist -l
```

`clist` 명령은 `choco search`를 와 같은 역할을 합니다.



## 패키지 업데이트 하기

`upgrade` 명령어를 통해서 패키지를  최신 버전으로 업데이트가 가능 합니다.

```bash
> choco upgrade bandizip
```

혹시, choco를 통해서 설치한 프로그램을 모두 업데이트 하고 싶다면 패키지 이름 대신 `all`을 넣어 주면 됩니다.

```bash
> choco upgrade all
```



## chocolatey 설치부터 패키지 설치까지 한방 스크립트

`choco_install.bat`라는 파일을 만들고 아래의 내용을 복사해서 넣어 주세요.

그리고, 뒷 부분에 설치하고 싶은 패키지를  넣어 주시면 됩니다.

```bash
@echo off
CLS
ECHO **************************************
ECHO * Start Chocolatey Batch
ECHO **************************************

:::::::::::::::::::::::::::::::::::::::::
:: 체크 및 관리자 권한 가져 오기
NET FILE 1>NUL 2>NUL
if '%errorlevel%' == '0' ( goto gotPrivileges ) else ( goto getPrivileges )

:getPrivileges
:::::::::::::::::::::::::::::::::::::::::
:: UAC를 사용해서 관리자 권한으로 전환
if '%1'=='ELEV' (shift & goto gotPrivileges)  
ECHO.
ECHO **************************************
ECHO * Use UAC, switch to admin
ECHO **************************************

setlocal DisableDelayedExpansion
set "batchPath=%~0"
setlocal EnableDelayedExpansion
ECHO Set UAC = CreateObject^("Shell.Application"^) > "%temp%\OEgetPrivileges.vbs"
ECHO UAC.ShellExecute "!batchPath!", "ELEV", "", "runas", 1 >> "%temp%\OEgetPrivileges.vbs"
"%temp%\OEgetPrivileges.vbs"
exit /B


:gotPrivileges
:::::::::::::::::::::::::::::::::::::::::
:: 시작 하기
setlocal & pushd .

WHERE choco 1>NUL 2>NUL
if '%errorlevel%' == '0' ( goto chocoInstalled ) else ( goto chocoMissing )

:chocoMissing
::::::::::::::::::::::::::::
:: Chocolatey가 없을 경우 설치
::::::::::::::::::::::::::::
ECHO.
choice /M "Chocolatey not found. Install now?"
IF '%errorlevel%' == '2' exit /B
ECHO.
ECHO **************************************
ECHO * Chocolatey install
ECHO **************************************

@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin

:chocoInstalled
ECHO.
ECHO **************************************
ECHO * Packages install
ECHO **************************************

@echo on

:: 항상 자동으로 yes를 선택하도록 설정
choco feature enable --name=allowGlobalConfirmation

:: 먼저 기존 패키지 업데이트
choco upgrade all -y

:: 사용할 어플리케이션 설치
set choco_install=choco install -fy
%choco_install% bandizip 
%choco_install% firefox
%choco_install% googlechrome
%choco_install% vcredist140
%choco_install% vcredist2012
%choco_install% directx
%choco_install% dotnetfx
%choco_install% javaruntime
%choco_install% everything
%choco_install% wox
%choco_install% qbittorrent
%choco_install% f.lux
%choco_install% typora
%choco_install% freefilesync
%choco_install% calibre
%choco_install% notion
%choco_install% vlc
%choco_install% krita
%choco_install% paint.net
%choco_install% jbs
%choco_install% ditto
%choco_install% ccleaner.portable
%choco_install% git.install --params "/GitAndUnixToolsOnPath /NoShellIntegration /NoGuiHereIntegration /WindowsTerminal"

:: 항상 자동으로 yes를 선택하는 옵션 끄기
choco feature disable --name=allowGlobalConfirmation

:: 업데이트 된 설정 다시 읽기
RefreshEnv.cmd

pause
```

`choco_install.bat` 파일을 실행했을때 관리자 권한이 아니면 관리자 권한을 부여해서 실행하게 됩니다.

컴퓨터 설치를 자주 하시게 되는 분들은 위와 같이 파일을 하나 설정해 둔다면 유용하게 사용 할 수 있을 것이라고 생각 됩니다.

