---
title: "tmux 사용법 완전 정리: 세션 관리부터 생산성 꿀팁까지"
date: 2026-02-14T08:35:00+09:00
draft: true
description: "tmux의 기본 사용법(세션/윈도우/패널)부터 실무에서 바로 쓰는 고급 팁, 플러그인(TPM/Resurrect/Continuum), 클립보드 설정까지 한 번에 정리합니다."
categories: [System, Tooling, Productivity]
tags: [tmux, terminal, linux, productivity, devtools]
---

터미널 작업이 길어질수록 이런 상황이 자주 생깁니다.

- SSH 연결이 끊겨서 실행 중이던 작업이 날아감
- 프로젝트마다 터미널 창을 여러 개 열어두다가 관리가 안 됨
- 같은 명령을 여러 서버에 반복 입력해야 함

이때 가장 확실한 해결책이 `tmux`입니다. 이 글에서는 **처음 쓰는 분도 바로 따라할 수 있게** 기본 개념부터 실무 팁까지 정리했습니다.

<!--more-->

## 1. tmux가 정확히 뭐가 좋은가?

`tmux`는 터미널 멀티플렉서입니다. 하나의 터미널 안에서 세션/윈도우/패널을 만들고, 분리(detach)했다가 다시 붙을(attach) 수 있습니다.

핵심 구조는 3가지만 기억하면 됩니다.

- **Session**: 작업 공간(프로젝트 단위)
- **Window**: 탭
- **Pane**: 탭 안 분할 화면

즉, 프로젝트마다 Session 하나씩 두고, 빌드/서버/로그를 Pane으로 분리하면 작업 흐름이 안정됩니다.

## 2. 가장 먼저 익혀야 할 기본 명령

### 2.1 세션 생성/접속/목록

```bash
# 새 세션 생성
tmux new -s myproj

# 세션 목록
tmux ls

# 세션 다시 붙기
tmux attach -t myproj

# 접속 중이던 클라이언트 강제 분리 후 붙기
tmux attach -d -t myproj
```

아래 한 줄은 실무에서 정말 많이 씁니다.

```bash
# 있으면 붙고, 없으면 생성
tmux new -As myproj
```

### 2.2 분리(detach)

tmux 내부에서:

```text
Ctrl+b, d
```

서버 작업 중 SSH가 끊겨도 세션은 살아있어서 다시 `attach`하면 이어서 작업할 수 있습니다.

## 3. 기본 단축키 치트시트

tmux 기본 prefix는 `Ctrl+b`입니다.

### 3.1 빠른 시작 (자주 쓰는 핵심)

| 키 | 기능 | 설명 |
| --- | --- | --- |
| `Ctrl+b c` | 새 윈도우 | 현재 세션에 새 window 생성 |
| `Ctrl+b n` / `Ctrl+b p` | 윈도우 이동 | 다음/이전 window로 전환 |
| `Ctrl+b %` | 좌우 분할 | pane을 수평으로 분할 |
| `Ctrl+b "` | 상하 분할 | pane을 수직으로 분할 |
| `Ctrl+b` + 방향키 | 패널 이동 | 인접 pane으로 포커스 이동 |
| `Ctrl+b x` | 패널 종료 | 현재 pane 닫기 |
| `Ctrl+b z` | 패널 줌 | 현재 pane 확대/복원 |
| `Ctrl+b [` | 복사 모드 | copy mode 진입 |
| `Ctrl+b ]` | 붙여넣기 | 최근 버퍼 붙여넣기 |
| `Ctrl+b ?` | 도움말 | 전체 키바인딩 목록 표시 |

### 3.2 윈도우 관리 치트시트

| 키 | 기능 | 설명 |
| --- | --- | --- |
| `Ctrl+b c` | 새 윈도우 | window 생성 |
| `Ctrl+b 0~9` | 번호 이동 | 해당 번호 window로 즉시 전환 |
| `Ctrl+b '` | 번호 입력 이동 | window 번호를 입력해 전환 |
| `Ctrl+b n` / `Ctrl+b p` | 다음/이전 | window 순서 이동 |
| `Ctrl+b l` | 마지막 윈도우 | 직전에 보던 window로 복귀 |
| `Ctrl+b ,` | 이름 변경 | 현재 window 이름 변경 |
| `Ctrl+b &` | 윈도우 종료 | 현재 window 닫기(확인 프롬프트) |
| `Ctrl+b w` | 트리 선택 | session/window/pane 트리에서 선택 |
| `Ctrl+b .` | 인덱스 이동 | 현재 window 번호 재배치 |

### 3.3 세션 관리 치트시트

| 키 | 기능 | 설명 |
| --- | --- | --- |
| `Ctrl+b s` | 세션 목록 | session 트리 열기 |
| `Ctrl+b $` | 세션 이름 변경 | 현재 session 이름 변경 |
| `Ctrl+b d` | detach | session은 유지하고 빠져나오기 |
| `Ctrl+b D` | 클라이언트 관리 | 붙어있는 client 목록/분리 |
| `Ctrl+b (` | 이전 세션 | 이전 session으로 전환 |
| `Ctrl+b )` | 다음 세션 | 다음 session으로 전환 |

### 3.4 패널/레이아웃 관리 치트시트

| 키 | 기능 | 설명 |
| --- | --- | --- |
| `Ctrl+b %` / `Ctrl+b "` | 분할 | 좌우/상하 분할 |
| `Ctrl+b o` | 다음 패널 | pane 순환 이동 |
| `Ctrl+b q` | 패널 번호 표시 | 번호 보고 숫자로 즉시 이동 |
| `Ctrl+b ;` | 마지막 패널 | 직전에 활성화한 pane으로 복귀 |
| `Ctrl+b {` / `Ctrl+b }` | 패널 위치 교환 | 이전/다음 pane과 스왑 |
| `Ctrl+b z` | 확대/복원 | 현재 pane zoom 토글 |
| `Ctrl+b Space` | 레이아웃 순환 | pane layout 변경 |
| `Ctrl+b !` | 패널 분리 | 현재 pane을 새 window로 분리 |

### 3.5 셸 명령 치트시트 (세션/윈도우)

| 명령 | 기능 | 설명 |
| --- | --- | --- |
| `tmux ls` | 세션 목록 | 현재 살아있는 session 확인 |
| `tmux new -s myproj` | 세션 생성 | 이름 지정해 새 session 생성 |
| `tmux new -As myproj` | attach-or-create | 있으면 붙고 없으면 생성 |
| `tmux attach -t myproj` | 세션 접속 | 특정 session에 붙기 |
| `tmux attach -d -t myproj` | 강제 접속 | 다른 client를 분리하고 붙기 |
| `tmux kill-session -t myproj` | 세션 종료 | 특정 session 종료 |
| `tmux kill-server` | 전체 종료 | tmux server 및 모든 session 종료 |

## 4. 실무에서 바로 체감되는 꿀팁

### 4.1 여러 서버에 같은 명령 동시에 실행

패널 동기화:

```bash
# tmux 명령 프롬프트(Ctrl+b :)에서 실행
setw synchronize-panes on
```

끄기:

```bash
setw synchronize-panes off
```

배포, 로그 확인, 동일 명령 반복 작업에서 매우 유용합니다.

### 4.2 패널 번호 보면서 즉시 이동

```text
Ctrl+b q
```

패널 번호가 잠깐 뜨고 숫자 키로 바로 이동할 수 있습니다.

### 4.3 자주 쓰는 윈도우 레이아웃 회전

```text
Ctrl+b Space
```

분할 레이아웃을 순환하면서 보기 편한 형태로 빠르게 전환할 수 있습니다.

### 4.4 복잡한 패널에서 일시적으로 집중

```text
Ctrl+b z
```

현재 패널을 전체 화면처럼 써서 디버깅/로그 추적에 좋습니다.

### 4.5 tmux 설정 즉시 반영

`.tmux.conf` 수정 후 재실행 없이 반영:

```bash
tmux source-file ~/.tmux.conf
```

## 5. 추천 `.tmux.conf` 시작 템플릿

아래는 입문자에게 무난한 시작점입니다.

```tmux
# prefix를 Ctrl+a로 변경 (선택)
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# 마우스 사용
set -g mouse on

# 인덱스를 1부터
set -g base-index 1
setw -g pane-base-index 1

# copy mode를 vi 스타일로
setw -g mode-keys vi

# 설정 리로드 단축키
bind r source-file ~/.tmux.conf \; display-message "tmux.conf reloaded"
```

prefix 변경은 취향입니다. 기본 `Ctrl+b`가 익숙하면 그대로 써도 됩니다.

## 6. 플러그인: 이것만 알아도 생산성 급상승

### 6.1 TPM (Tmux Plugin Manager)

설치:

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

`.tmux.conf` 하단:

```tmux
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'

run '~/.tmux/plugins/tpm/tpm'
```

플러그인 설치/업데이트:

- `prefix + I`: 설치
- `prefix + U`: 업데이트

### 6.2 tmux-resurrect: 세션 저장/복원

```tmux
set -g @plugin 'tmux-plugins/tmux-resurrect'
```

- `prefix + Ctrl-s`: 저장
- `prefix + Ctrl-r`: 복원

재부팅 후 세션/윈도우/패널 레이아웃을 되살릴 때 유용합니다.

### 6.3 tmux-continuum: 자동 저장/자동 복원

```tmux
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @continuum-restore 'on'
```

주의할 점:

- continuum은 상태줄(`status`)이 켜져 있어야 주기 저장이 동작
- 일부 테마/플러그인이 `status-right`를 덮어쓰면 자동 저장이 멈출 수 있음

## 7. 복사/클립보드에서 자주 막히는 포인트

tmux 복사 모드와 시스템 클립보드 연동은 터미널 종류/버전에 따라 다르게 동작합니다.

기본적으로 확인할 것:

```bash
tmux show -s set-clipboard
tmux info | grep Ms
```

일반적인 권장값:

```tmux
set -s set-clipboard external
```

왜 `external`을 권장하나?

- `on`은 tmux 내부 앱이 클립보드 설정에 영향을 줄 수 있어 보안상 주의 필요
- `external`은 그 범위를 제한해서 상대적으로 안전함

Linux에서 외부 도구를 쓰는 경우(예: `xsel`, `xclip`)는 `DISPLAY`나 툴 동작 이슈가 있을 수 있습니다. 환경에 따라 `pbcopy`(macOS) 등 OS별 방식으로 맞추는 것이 안전합니다.

## 8. 실전 운영 패턴 (권장)

프로젝트마다 세션 하나를 고정해서 쓰면 좋습니다.

```bash
tmux new -As backend
tmux new -As frontend
tmux new -As ops
```

각 세션에서 권장 패널 구성 예시:

- pane 1: 앱 서버 실행
- pane 2: 테스트/빌드
- pane 3: 로그 tail
- pane 4: git 작업

이 패턴만 지켜도 터미널 창 난립이 거의 사라집니다.

## 9. 마무리

tmux는 처음 1~2일만 어색하고, 그 이후에는 “없으면 불편한” 도구가 됩니다.

시작은 간단히:

1. `tmux new -As myproj` 습관화
2. `Ctrl+b d`로 분리/복귀 익히기
3. 자주 쓰는 키 8~10개만 먼저 외우기
4. 필요하면 TPM + resurrect/continuum 추가

이 순서로 가면 무리 없이 실전에 정착할 수 있습니다.

## 참고 링크

- tmux 공식 매뉴얼: https://man7.org/linux/man-pages/man1/tmux.1.html
- tmux 공식 위키(Home): https://github.com/tmux/tmux/wiki
- tmux Getting Started: https://github.com/tmux/tmux/wiki/Getting-Started
- tmux Clipboard 문서: https://github.com/tmux/tmux/wiki/Clipboard
- TPM: https://github.com/tmux-plugins/tpm
- tmux-resurrect: https://github.com/tmux-plugins/tmux-resurrect
- tmux-continuum: https://github.com/tmux-plugins/tmux-continuum
