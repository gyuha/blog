---
title: "Python의 uv 패키지 매니저"
date: 2025-04-14T21:35:29+09:00
draft: true
categories: [python]
tags: [python]
---

## 1. uv의 등장 배경: 왜 새로운 도구가 필요했나?
### 1.1. 기존 도구들의 한계
- **pip의 속도 문제**: 대규모 패키지 설치 시 10분 이상 소요되는 경우 빈번(uv는 동일 작업을 10초 내 완료)
- **환경 관리의 복잡성**: venv + pip + pip-tools + virtualenvwrapper 조합 필요
- **의존성 해결 충돌**: 복잡한 의존성 그래프에서 종종 ResolutionError 발생
- **멀티플랫폼 지원 부족**: Windows 환경에서의 성능 저하 문제

### 1.2. Astral팀의 접근 방식
- **Rust 기반 구현**: 메모리 안정성과 네이티브 성능 확보
- **병렬 처리 최적화**: 의존성 해결과 패키지 다운로드를 동시 진행
- **유니버설 바이너리**: 별도 Python 설치 없이 독립 실행 가능

### 1.3. 성능 벤치마크 (Django 프로젝트 기준)
| 작업          | pip    | poetry | uv     |
|---------------|--------|--------|--------|
| 초기 설치      | 142s   | 98s    | **12s**|
| 재설치         | 89s    | 64s    | **0.8s**|
| 잠금파일 생성  | 32s    | 28s    | **3s** |

---

## 2. 설치 방법

`uv`는 다양한 방법으로 설치할 수 있습니다. 아래는 OS별 설치 방법과 pip를 사용하는 방법입니다.

### 2.1. Windows

Windows에서 `uv`를 설치하려면 PowerShell을 사용합니다:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2.2. macOS/Linux

macOS 또는 Linux에서는 다음 명령어를 사용하여 설치할 수 있습니다:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2.3. pip를 사용한 설치

Python의 `pip`를 사용하여 설치할 수도 있습니다:

```bash
pip install uv
```

설치 후 `uv` 명령어가 제대로 작동하는지 확인하려면 다음 명령어를 실행하세요:

```bash
uv --version
```

### 4. 셀 통합 설정

`uv`는 다양한 셸 환경에서 자동 완성 및 편리한 명령어 사용을 지원합니다. 아래는 OS별 셸 통합 설정 방법입니다.

#### 4.1. Windows (PowerShell)

PowerShell에서 `uv` 자동 완성을 설정하려면 다음 명령어를 실행하세요:

```powershell
mkdir -Force $PROFILE.CurrentUserAllHosts
uv generate-completion powershell > $PROFILE.CurrentUserAllHosts\uv.ps1
```

PowerShell을 다시 시작하면 자동 완성이 활성화됩니다.

#### 4.2. macOS/Linux (Zsh)

Zsh에서 `uv` 자동 완성을 설정하려면 다음 명령어를 실행하세요:

```bash
mkdir -p ~/.zsh/completions
uv generate-completion zsh > ~/.zsh/completions/_uv
```

그런 다음 `~/.zshrc` 파일에 다음 줄을 추가합니다:

```bash
fpath=(~/.zsh/completions $fpath)
autoload -U compinit && compinit
```

Zsh를 다시 시작하거나 `source ~/.zshrc`를 실행하여 설정을 적용합니다.

#### 4.3. macOS/Linux (Bash)

Bash에서 `uv` 자동 완성을 설정하려면 다음 명령어를 실행하세요:

```bash
mkdir -p ~/.bash_completion.d
uv --generate-completion bash > ~/.bash_completion.d/uv
```

그런 다음 `~/.bashrc` 파일에 다음 줄을 추가합니다:

```bash
if [ -f ~/.bash_completion.d/uv ]; then
  . ~/.bash_completion.d/uv
fi
```

Bash를 다시 시작하거나 `source ~/.bashrc`를 실행하여 설정을 적용합니다.

---

## 3. 가상환경 관리하기

uv는 Python 가상환경을 간편하게 생성하고 관리할 수 있는 강력한 도구를 제공합니다. 아래는 가상환경 관리 방법입니다:

### 3.1. 가상환경 생성


---

## 4. 패키지 관리


### 4.2 pip로 package 설치 하기
```
uv pip install -r requirements.txt
```
pip를 통해서 패키지를 설치 한다. 하지만 `pyproject.toml`에는 기록하지 않습니다.

### 4.1 기존 requirements.txt 파일에서 설치 하기

```
uv add -r requirements.txt
```
실행을 하면 패키지를 설치 하고 `pyproject.toml`파일에 패키지를 넣어 줍니다.
