---
title: "윈도우 git-bash에서 zsh 사용하기"
date: 2025-04-13T13:49:04+09:00
draft: false
categories: [System]
tags: [windows, git-bash, zsh, terminal]
---

윈도우 환경에서 개발을 하다보면 터미널의 기능이 제한적이라는 것을 느끼게 됩니다. 이럴 때 git-bash와 zsh를 함께 사용하면 더 강력한 터미널 환경을 구축할 수 있습니다. 이 글에서는 윈도우 git-bash에서 zsh를 설치하고 설정하는 방법을 알아보겠습니다.

## 1. Git Bash 설치

먼저 Git Bash를 설치해야 합니다. [Git for Windows](https://git-scm.com/download/win)에서 최신 버전을 다운로드하여 설치합니다.

## 2. ZSH 설치

### 2.1 Nerd Font 설치

ZSH를 사용하기 전에 먼저 Nerd Font를 설치해야 합니다. [Nerd Fonts](https://www.nerdfonts.com/font-downloads)에서 원하는 폰트를 다운로드하여 설치합니다. 이 글에서는 `EnvyCodeR Nerd Font Mono`를 사용합니다.

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
Font=EnvyCodeR Nerd Font Mono
FontHeight=14
Columns=180
Rows=46
ScrollbackLines=2000
BackgroundColour=13,13,13
MiddleClickAction=void
RightClickAction=paste
Language=
BellType=0
BellFlash=yes
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

## 3. ZSH 설정

### 3.1 ZSH를 기본 셸로 설정

`/etc/zsh/zshenv` 파일을 편집하여 다음 줄을 파일 시작 부분에 추가합니다:

```bash
PATH=/mingw64/bin/usr/bin:/usr/bin:/bin:$PATH
```

### 3.2 Git Bash에서 ZSH 자동 실행 설정

`C:\Program Files\Git\etc\bash.bashrc` 파일 끝에 다음 내용을 추가합니다:

```bash
# Get user bash configuration ~/.bashrc
source ~/.bashrc;
```

그리고 `~/.bashrc` 파일을 생성하고 다음 내용을 추가합니다:

```bash
# Launch Zsh
if [ -t 1 ]; then
exec zsh
fi
```

## 4. ZSH 플러그인 설치

### 4.1 zsh-autosuggestions 설치

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH/plugins/zsh-autosuggestions
source $ZSH/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
```

### 4.2 zsh-syntax-highlighting 설치

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH/plugins/zsh-syntax-highlighting
source $ZSH/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
```

## 5. Oh My Zsh 설치

다음 명령어를 실행하여 Oh My Zsh를 설치합니다:

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

## 6. Powerlevel10k 테마 설치

### 6.1 Powerlevel10k 설치

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

### 6.2 설정 마법사 실행

ZSH를 재시작한 후 다음 명령어를 실행하여 Powerlevel10k 설정 마법사를 시작합니다:

```bash
p10k configure
```

## 7. VS Code에서 ZSH 사용하기

VS Code의 `settings.json` 파일에 다음 설정을 추가합니다:

```json
"terminal.integrated.profiles.windows": {
  "Git Zsh": {
    "path": "C:\\Program Files\\Git\\bin\\bash.exe",
    "args": []
  }
},
"terminal.integrated.defaultProfile.windows": "Git Zsh",
"terminal.integrated.fontFamily": "'EnvyCodeR Nerd Font Mono'"
```

이제 윈도우에서도 강력한 ZSH 환경을 사용할 수 있습니다. Git Bash와 ZSH의 결합은 개발 생산성을 크게 향상시킬 수 있습니다.

