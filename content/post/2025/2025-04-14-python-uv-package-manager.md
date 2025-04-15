---
title: "Python의 uv 패키지 매니저"
date: 2025-04-14T21:35:29+09:00
draft: true
categories: [python]
tags: [python]
---

UV는 현대적이고 고성능 파이썬 패키지 관리자이며 Rust로 작성된 설치 프로그램입니다. `PIP`과 같은 전통적인 Python 패키지 관리 도구의 드롭 인 교체 역할을하며 속도, 신뢰성 및 종속성 해상도가 크게 향상됩니다.
<!--more-->



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
❯ powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2.2. macOS/Linux

macOS 또는 Linux에서는 다음 명령어를 사용하여 설치할 수 있습니다:

```bash
❯ curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2.3. pip를 사용한 설치

Python의 `pip`를 사용하여 설치할 수도 있습니다:

```bash
❯ pip install uv
```

설치 후 `uv` 명령어가 제대로 작동하는지 확인하려면 다음 명령어를 실행하세요:

```bash
❯ uv --version
```

개인적으로는 python을 설치 하고 pip로 uv를 설치하는 것을 추천 합니다.
vscode에서 Jupter Notebook 같이 자동으로 pip를 통해서 설치하는 경우가 있는데. python의 pip를 통하면 편하게 설치가 됩니다.


## 3. 셀 통합 설정

`uv`는 다양한 셸 환경에서 자동 완성 및 편리한 명령어 사용을 지원합니다. 아래는 OS별 셸 통합 설정 방법입니다.

#### 3.1. Windows (PowerShell)

PowerShell에서 `uv` 자동 완성을 설정하려면 다음 명령어를 실행하세요:

```powershell
❯ mkdir -Force $PROFILE.CurrentUserAllHosts
❯ uv generate-completion powershell > $PROFILE.CurrentUserAllHosts\uv.ps1
```

PowerShell을 다시 시작하면 자동 완성이 활성화됩니다.

#### 3.2. macOS/Linux (Zsh)

Zsh에서 `uv` 자동 완성을 설정하려면 다음 명령어를 실행하세요:

```bash
❯ mkdir -p ~/.zsh/completions
❯ uv generate-completion zsh > ~/.zsh/completions/_uv
```

그런 다음 `~/.zshrc` 파일에 다음 줄을 추가합니다:

```bash
fpath=(~/.zsh/completions $fpath)
autoload -U compinit && compinit
```

Zsh를 다시 시작하거나 `source ~/.zshrc`를 실행하여 설정을 적용합니다.

#### 3.3. macOS/Linux (Bash)

Bash에서 `uv` 자동 완성을 설정하려면 다음 명령어를 실행하세요:

```bash
❯ mkdir -p ~/.bash_completion.d
❯ uv --generate-completion bash > ~/.bash_completion.d/uv
```

그런 다음 `~/.bashrc` 파일에 다음 줄을 추가합니다:

```bash
if [ -f ~/.bash_completion.d/uv ]; then
  . ~/.bash_completion.d/uv
fi
```

Bash를 다시 시작하거나 `source ~/.bashrc`를 실행하여 설정을 적용합니다.

---
## 4. 패키지 관리 하기
### 4.1. 파이썬 버전 설치하기
특정 Python 버전을 설치하거나 변경하려면 다음을 실행하세요:

```bash
❯ uv python install 3.12.10
```
설치된 Python 버전을 확인하려면:

```bash
❯ uv python list
```

현재 폴더에 가상환경 폴더를 설치 하려면 아래와 같이 합니다.

```bash
❯ uv venv --python 3.12.10
Using CPython 3.12.10
Creating virtual environment at: .venv
Activate with: source .venv/Scripts/activate
```

이렇게 하면 현재 폴더에 `.venv`폴더가 생성 되고 python 가상 환경 설정이 들어 갑니다.




### 4.2. 프로젝트 생성하기

가상 환경을 설정 하려면 아래와 같이 init 명령를 통해서 프로젝트 초기 설정을 할 수 있습니다.

```bash
❯ uv init uv-project
❯ cd uv-project
❯ uv venv 
❯ source .venv/Scripts/activate
```
uv-project 폴더가 생성되고, 내부 구조는 대략 다음과 같습니다:

```bash
❯ tree -a
.
├── .python-version
├── .gitignore
├── .venv
├── pyproject.toml
├── hello.py
└── README.md
```

 * .python-version을 통해 **파이썬 버전**이 고정됩니다
 * pyproject.toml 은 **의존성 및 프로젝트 메타데이터**를 정의하는 핵심 파일입니다.
 * .venv 폴더는 아직 보이지 않을 수 있는데, 의존성을 추가하면 자동으로 생성됩니다.

혹시 현재 폴더에 아래와 같이 설정 하시면 됩니다.
 ```bash
❯ uv init
❯ uv venv 
❯ source .venv/Scripts/activate
 ```


## 5. 패키지 관리

### 5.1. 패키지 설치 하기
uv add로 패키지를 설치 할 수 있습니다. 한번에 여러개의 패키지를 설치 하려면 뒤에 붙여서 패키지명을 적어 주면 됩니다.

```bash
❯ uv add scipy six
Resolved 4 packages in 152ms
Prepared 3 packages in 1.50s
░░░░░░░░░░░░░░░░░░░░ [0/3] Installing 
Installed 3 packages in 527ms
 + numpy==2.2.4
 + scipy==1.15.2
 + six==1.17.0
```

설치가 완료 되면 `pyproject.toml`파일을 확인 해 보면 설치된 패키지가 기록 된 것을 확인 할 수 있습니다.

```bash
❯ cat pyproject.toml
[project]
name = "uv"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "scipy>=1.15.2",
    "six>=1.17.0",
]
```

### 5.2. 기존 requirements.txt 파일에서 설치 하기

기존 python 프로젝트 라면 requirements.txt 파일이 있을 겁니다.
그 파일을 기준으로 패키지를 설치 하려면 아래와 같이 사용 하시면 됩니다.

```bash
❯ uv add -r requirements.txt
```

혹시, 다른 uv 사용자가 아닌 분을 배려 해서 requirements.txt 파일을 만들고 싶다면 uv pip 명령어를 통해서 파일을 만들 수도 있습니다
```bash
❯ uv pip freeze > requirements.txt
```

### 5.3. 패키지 삭제 하기
환경과 `pyproject.toml` 파일에서 의존성을 제거하려면 `uv remove` 명령어를 사용할 수 있습니다. 이 명령어는 해당 패키지와 그 하위 의존성들을 모두 제거합니다:

```bash
❯ uv remove scikit-learn
```

## 6. 스크립트 실행하기
필요한 의존성을 설치한 후에는 평소처럼 Python 스크립트 작업을 시작할 수 있습니다. UV는 Python 코드를 실행하는 몇 가지 다른 방법을 제공합니다:

Python 스크립트를 직접 실행하려면 일반적인 `python script.py` 구문 대신 `uv run` 명령 다음에 스크립트 이름을 사용하면 됩니다:

```bash
❯ uv run hello.py
```

`run` 명령은 스크립트가 프로젝트를 위해 UV가 생성한 가상 환경 내에서 실행되도록 보장합니다.


## 7. UV에서 잠금 파일이란 무엇입니까?
잠금 파일(uv.lock)은 UV의 종속성 관리에서 필수적인 부분입니다. 종속성을 설치하기 위해 uv add 명령을 실행하면 UV가 uv.lock 파일을 생성하고 업데이트합니다. 이 잠금 파일은 다음과 같은 몇 가지 중요한 용도로 사용됩니다.

설치된 모든 종속성과 하위 종속성의 정확한 버전을 기록합니다.
서로 다른 환경에서 종속성 버전을 "잠금"하여 재현 가능한 빌드를 보장합니다.
일관된 패키지 버전을 유지 관리하여 "종속성 지옥"을 방지하는 데 도움이 됩니다.
UV가 종속성을 다시 해결하는 대신 잠긴 버전을 사용할 수 있으므로 설치 속도가 빨라집니다.
UV는 잠금 파일을 자동으로 관리하므로 수동으로 편집할 필요가 없습니다. 잠금 파일은 모든 개발자가 동일한 종속성 버전을 사용할 수 있도록 버전 제어에 커밋되어야 합니다.

### 잠금 파일과 requirements.txt의 차이점
잠금 파일과 requirements.txt은 모두 종속성을 추적하는 역할을 하지만 고유한 목적과 사용 사례가 있습니다. 잠금 파일에는 정확한 패키지 버전과 전체 종속성 트리에 대한 자세한 정보가 포함되어 있어 개발 전반에 걸쳐 일관된 환경을 보장합니다. Requirements.txt 파일은 더 간단하고, 일반적으로 직접 종속성만 나열하며, Python 도구에서 널리 지원됩니다.

잠금 파일은 재현 가능한 빌드를 유지 관리하고 종속성 충돌을 방지하기 위해 개발에 필수적입니다. Requirements.txt 파일은 배포 시나리오 또는 UV를 사용하지 않을 수 있는 사용자와 코드를 공유할 때 더 적합합니다. 또한 UV의 잠금 파일 형식을 지원하지 않는 도구 및 서비스와의 호환성을 위해 필요합니다.

배포를 위한 requirements.txt 생성하는 동안 개발용 UV의 잠금 파일을 사용하여 두 파일을 모두 유지 관리할 수 있습니다. UV 잠금 파일에서 requirements.txt 생성하려면 다음 명령을 사용합니다.

```bash
❯ uv export -o requirements.txt
```

이렇게 하면 잠금 파일을 기반으로 고정된 버전이 있는 텍스트 파일이 생성되므로 프로젝트의 종속성을 표준 형식으로 쉽게 공유하면서 개발 중에 UV의 고급 종속성 관리의 이점을 계속 활용할 수 있습니다.






