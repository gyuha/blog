---
title: "Windows Terminal Git Bash 한글 깨짐 해결하기"
date: 2026-02-05T08:30:00+09:00
draft: false
description: "Windows Terminal에서 Git Bash 사용 시 한글이 깨지는 문제를 Git 설정과 .bashrc, .inputrc 수정을 통해 해결하는 방법을 소개합니다."
tags: ["Windows Terminal", "Git Bash", "UTF-8"]
---

Windows Terminal(wt) 내 Git Bash에서 한글이 깨지는 문제는 주로 **Git 설정의 유니코드(UTF-8) 처리 미흡 때문**입니다. `git status`, `git log` 명령어에서 한글 파일명이나 커밋 메시지가 깨져서 표시되는 경험이 있으실 겁니다.

이 문제는 Git 설정, `.bashrc`, `.inputrc` 파일 수정을 통해 해결할 수 있습니다. 가장 효과적인 방법은 `git config` 명령어를 사용하여 `core.quotepath`를 `false`로 설정하고, 쉘 환경에서 `LANG` 환경 변수를 UTF-8로 설정하는 것입니다.

<!--more-->

## 문제 현상

Windows Terminal의 Git Bash에서 다음과 같은 한글 깨짐 현상이 발생합니다:

- `git status` 명령어에서 한글 파일명이 이스케이프 문자로 표시됨
- `git log` 명령어에서 한글 커밋 메시지가 깨져서 보임
- `ls` 명령어로 한글 파일명 확인 시 깨짐
- 터미널 입력 시 한글이 정상적으로 표시되지 않음

## 해결 방법

### 1. Git 파일명/메시지 한글 깨짐 해결

`git status`, `git log`에서 한글이 정상적으로 표시되도록 Git의 `core.quotepath` 설정을 변경합니다. 이 설정은 0x80 이상의 문자(한글 등)를 이스케이프할지 여부를 결정합니다.

```bash
git config --global core.quotepath false
```

### 2. ls 명령어 한글 파일명 깨짐 해결

`~/.bashrc` 파일에 환경 변수 설정을 추가하여 로케일을 UTF-8로 설정합니다. Git Bash에서 다음 명령어를 실행하세요:

```bash
echo 'export LANG="ko_KR.UTF-8"' >> ~/.bashrc
echo 'export LC_ALL="ko_KR.UTF-8"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 입력 시 한글 깨짐 해결 (Inputrc 설정)

`~/.inputrc` 파일을 생성하거나 수정하여 8비트 문자 입력을 허용하도록 설정합니다:

```bash
echo "set output-meta on" >> ~/.inputrc
echo "set convert-meta off" >> ~/.inputrc
```

- `set output-meta on`: 8비트 문자(Meta 키 + 문자 조합 등)를 직접 출력
- `set convert-meta off`: 8비트 문자를 이스케이프 시퀀스로 변환하지 않음

## 적용 확인

모든 설정을 완료한 후 Git Bash를 재시작하면 다음과 같이 한글이 정상적으로 표시됩니다:

```bash
$ git status
현재 브랜치 main
브랜치가 'origin/main'과 일치합니다

커밋하도록 정리하지 않은 변경 사항들:
  (git add/rm을 사용하여 커밋할 것을 표시하십시오)
  (git restore를 사용하여 작업 디렉토리 변경 사항을 폐기하십시오)

    수정됨:   한글파일명.md
```

## 함께 보기

- [Git 공식 문서 - git-config](https://git-scm.com/docs/git-config)
- [Windows Terminal 공식 문서](https://docs.microsoft.com/en-us/windows/terminal/)
