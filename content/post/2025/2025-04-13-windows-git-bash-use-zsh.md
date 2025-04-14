---
title: "윈도우 git-bash에서 zsh 사용하기"
date: 2025-04-13T13:49:04+09:00
draft: false
categories: [System]
tags: [windows, git-bash, zsh, terminal]
---

윈도우 환경에서 개발을 하다보면 터미널의 기능이 제한적이라는 것을 느끼게 됩니다. 이럴 때 git-bash와 zsh를 함께 사용하면 더 강력한 터미널 환경을 구축할 수 있습니다. 이 글에서는 윈도우 git-bash에서 zsh를 설치하고 설정하는 방법을 알아보겠습니다.
<!--more-->

## 1. Git Bash 설치

먼저 Git Bash를 설치해야 합니다. [Git for Windows](https://git-scm.com/download/win)에서 최신 버전을 다운로드하여 설치합니다.

## 2. ZSH 설치

### 2.1 Nerd Font 설치

ZSH를 사용하기 전에 먼저 Nerd Font를 설치해야 합니다. [Nerd Fonts](https://www.nerdfonts.com/font-downloads)에서 원하는 폰트를 다운로드하여 설치합니다. 이 글에서는 `D2CodingLigature Nerd Font`를 사용합니다.

- [D2CodingLigature Nerd Font Download](https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/CommitMono.zip)

### 2.2 ZSH 패키지 다운로드

[MSYS2 패키지 저장소](https://packages.msys2.org/package/zsh?repo=msys&variant=x86_64)에서 최신 zsh 패키지를 다운로드합니다. 패키지는 `.zst` 형식으로 압축되어 있으므로, [PeaZip](https://peazip.github.io/zst-compressed-file-format.html)과 같은 압축 해제 프로그램이 필요합니다.

### 2.3 ZSH 설치

다운로드한 패키지의 내용을 Git Bash 설치 디렉토리(기본값: `C:\Program Files\Git`)에 압축 해제합니다.

### 2.4 ZSH 테스트 및 초기 설정

Git Bash를 열고 다음 명령어를 실행합니다:

```bash
zsh
```

이 단계에서 zsh는 몇 가지 초기 설정을 물어봅니다. 탭 완성, 히스토리 등의 설정을 원하는 대로 구성하면 됩니다.

### 2.5 터미널 설정

`~/.minttyrc` 파일을 생성하고 다음 내용을 추가합니다:


```bash
BoldAsFont=no
Font=D2CodingLigature Nerd Font
FontHeight=14
Columns=180
Rows=46
ScrollbackLines=2000
BackgroundColour=13,13,13
MiddleClickAction=void
RightClickAction=paste
Language=
BellType=0
BellFlash=no
Printer=Microsoft Print to PDF
Transparency=off
CursorBlinks=yes
ThemeFile=nord
ForegroundColour=178,178,178
CursorColour=225,225,225
FontSmoothing=full
Locale=en_US
Charset=UTF-8
Term=xterm-256color
BoldAsColour=no
CursorType=block
```
이렇게 설정 하면 git-bash의 터미널 창이 이뻐 집니다.

## 3. ZSH 설정

### 3.1 ZSH를 기본 셸로 설정

`/etc/zsh/zshenv` 파일을 편집하여 다음 줄을 파일 시작 부분에 추가합니다:

```bash
PATH=/mingw64/bin/usr/bin:/usr/bin:/bin:$PATH
```

### 3.2 Git Bash에서 ZSH 자동 실행 설정

`~/.bashrc` 파일을 생성하고 다음 내용을 추가합니다:

```bash
# Launch Zsh
if [ -t 1 ]; then
exec zsh
fi
```

이제 git-bash를 실행 합니다.

## 4. ZSH 유틸 설치
oh-my-zsh를 설치 하면 편하긴 한데. oh-my-zsh가 기본적으로 너무 많은 기능을 가지고 있어서 많이 무겁다는 단점있습니다.
이 포스트에서는 필요한 유틸만 별도로 설치 합니다. 

### 4.1 설치 경로 만들기
```
mkdir -p ~/.zsh/plugins
mkdir -p ~/.zsh/theme
```

### 4.2 zsh-autosuggestions 설치

zsh-autosuggestions는 명령어를 입력할 때 이전에 사용한 명령어를 기반으로 자동 완성을 제안해주는 플러그인입니다. 터미널에서 작업할 때 반복적인 명령어 입력을 크게 줄여주고, 긴 경로나 복잡한 명령어를 쉽게 재사용할 수 있게 해줍니다. 제안된 명령어는 회색으로 표시되며, 오른쪽 화살표 키를 눌러 빠르게 수락할 수 있습니다.

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/plugins/zsh-autosuggestions
```

`~/.zshrc` 파일에 아래의 내용을 추가 해 줍니다. 마지막에 추가 해 줍니다.
```bash
if [[ -r "~/.zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh" ]]; then
	source "~/.zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh"
fi 
```

### 4.3 zsh-syntax-highlighting 설치

zsh-syntax-highlighting은 명령줄에서 입력하는 명령어와 인자에 구문 강조 색상을 적용해주는 ZSH 플러그인입니다. 이 플러그인은 명령어가 올바르게 입력되었는지 실시간으로 시각적 피드백을 제공하며, 명령어를 실행하기 전에 오타나 구문 오류를 식별하는 데 도움을 줍니다. 유효한 명령어는 녹색으로, 존재하지 않는 명령어는 빨간색으로 표시되어 명령어 입력의 정확성을 즉시 확인할 수 있습니다.

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.zsh/plugins/zsh-syntax-highlighting
```

`~/.zshrc` 파일에 아래의 내용을 추가해 줍니다. 이 플러그인은 항상 zshrc 파일의 마지막에 로드되어야 한다는 점을 기억하세요.
`~/.zshrc` 파일에 아래의 내용을 추가 해 줍니다. 마지막에 추가 해 줍니다.

```bash
if [[ -r "~/.zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]]; then
	source "~/.zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi 
```

### 4.4 zsh-completions 설치

zsh-completions은 ZSH의 기본 명령어 완성 기능을 대폭 확장해주는 플러그인입니다. 이 플러그인은 수백 개의 추가 명령어, 도구 및 유틸리티에 대한 완성 스크립트를 제공하여 명령어 입력의 효율성과 정확성을 높여줍니다. Git, Docker, npm, pip, kubectl 등과 같은 다양한 개발 도구에 대한 고급 탭 완성 기능을 제공하므로 복잡한 명령어나 옵션을 기억하지 않아도 쉽게 입력할 수 있습니다.

```bash
git clone https://github.com/zsh-users/zsh-completions.git ~/.zsh/plugins/zsh-completions
```

`~/.zshrc` 파일에 아래의 내용을 추가해 줍니다.

```bash
if [[ -d ~/.zsh/plugins/zsh-completions/src ]]; then
  fpath=(~/.zsh/plugins/zsh-completions/src $fpath)
  autoload -U compinit && compinit
fi
```

이 설정은 zsh-completions의 완성 스크립트를 ZSH의 함수 경로(fpath)에 추가하고, 완성 시스템(compinit)을 초기화합니다.

## 6. Powerlevel10k 테마 설치

### 6.1 Powerlevel10k 설치

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/.zsh/theme/powerlevel10k
echo 'source ~/.zsh/theme/powerlevel10k/powerlevel10k.zsh-theme' >> ~/.zshrc
```
git-bash를 다시 시작 하면 Powerlevel10k의 설정이 시작 됩니다.


## 7. VS Code에서 ZSH 사용하기

VS Code의 `settings.json` 파일에 다음 설정을 추가합니다:

```json
"terminal.integrated.defaultProfile.windows": "Git Bash",
"terminal.integrated.fontFamily": "'D2CodingLigature Nerd Font'"
```

## 8. Windows Terminal에서 ZSH 사용하기

Windows 10/11에서는 Windows Terminal을 통해 더 강력하고 사용자 친화적인 터미널 환경을 구성할 수 있습니다. Windows Terminal에 Git Bash(ZSH)를 추가하여 사용하는 방법은 두 가지가 있습니다.

### 8.1 Git 설치 시 Windows Terminal 연동 옵션 선택

가장 간단한 방법은 Git for Windows를 설치할 때 Windows Terminal 프로필에 Git Bash를 추가하는 옵션을 선택하는 것입니다.

1. Git for Windows 설치 프로그램을 실행합니다.
2. 설치 과정 중 "Windows Terminal에 Git Bash 프로필 추가" 옵션을 체크합니다.
3. 설치가 완료되면 Windows Terminal에서 Git Bash를 바로 사용할 수 있습니다.

### 8.2 수동으로 Windows Terminal에 Git Bash 추가하기

이미 Git이 설치되어 있다면, Windows Terminal 설정 파일을 직접 수정하여 Git Bash를 추가할 수 있습니다.

1. Windows Terminal을 실행한 후, 상단의 드롭다운 메뉴 → 설정을 클릭합니다.
2. 좌측 하단의 "설정 파일 열기" 버튼을 클릭하여 JSON 설정 파일을 엽니다.
3. `profiles` → `list` 배열에 다음 코드를 추가합니다:

```json
{
    "guid": "{수정필요-GUID}",
    "hidden": false,
    "name": "Git Bash (ZSH)",
    "commandline": "C:\\Program Files\\Git\\bin\\bash.exe -li",
    "icon": "C:\\Program Files\\Git\\mingw64\\share\\git\\git-for-windows.ico",
    "startingDirectory": "%USERPROFILE%"
}
```

4. `guid` 값은 고유해야 합니다. [온라인 GUID 생성기](https://www.guidgenerator.com/online-guid-generator.aspx)를 사용하여 새 GUID를 생성하세요.
5. Git 설치 경로가 기본값과 다르다면 `commandline`과 `icon` 경로를 적절히 수정하세요.
6. 설정 파일을 저장하고 Windows Terminal을 재시작합니다.

기본 Profile을 bash로 하고 싶다면, 설정 파일에서

위에 입력 했던, profile의 id를 `defaultProfile`에 넣어 주면 된다.

```json
"defaultProfile": "{수정필요-GUID}",
```


이제 Windows Terminal의 드롭다운 메뉴에서 "Git Bash (ZSH)"를 선택하면 Git Bash가 실행되고, 우리가 설정한 ZSH 환경이 자동으로 로드됩니다.

이제 윈도우에서도 강력한 ZSH 환경을 사용할 수 있습니다. Git Bash와 ZSH의 결합은 개발 생산성을 크게 향상시킬 수 있습니다.

