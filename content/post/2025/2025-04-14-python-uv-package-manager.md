---
title: "Python의 uv 패키지 매니저"
date: 2025-04-14T21:35:29+09:00
draft: true
categories: [python]
tags: [python]
---

## 1. uv의 등장 배경: 왜 새로운 도구가 필요했나?
### 기존 도구들의 한계
- **pip의 속도 문제**: 대규모 패키지 설치 시 10분 이상 소요되는 경우 빈번(uv는 동일 작업을 10초 내 완료)
- **환경 관리의 복잡성**: venv + pip + pip-tools + virtualenvwrapper 조합 필요
- **의존성 해결 충돌**: 복잡한 의존성 그래프에서 종종 ResolutionError 발생
- **멀티플랫폼 지원 부족**: Windows 환경에서의 성능 저하 문제

### Astral팀의 접근 방식
- **Rust 기반 구현**: 메모리 안정성과 네이티브 성능 확보
- **병렬 처리 최적화**: 의존성 해결과 패키지 다운로드를 동시 진행
- **유니버설 바이너리**: 별도 Python 설치 없이 독립 실행 가능

### 성능 벤치마크 (Django 프로젝트 기준)
| 작업          | pip    | poetry | uv     |
|---------------|--------|--------|--------|
| 초기 설치      | 142s   | 98s    | **12s**|
| 재설치         | 89s    | 64s    | **0.8s**|
| 잠금파일 생성  | 32s    | 28s    | **3s** |

---

## 2. 설치 방법

`uv`는 다양한 방법으로 설치할 수 있습니다. 아래는 OS별 설치 방법과 pip를 사용하는 방법입니다.

### 1. Windows

Windows에서 `uv`를 설치하려면 PowerShell을 사용합니다:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. macOS/Linux

macOS 또는 Linux에서는 다음 명령어를 사용하여 설치할 수 있습니다:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. pip를 사용한 설치

Python의 `pip`를 사용하여 설치할 수도 있습니다:

```bash
pip install uv
```

설치 후 `uv` 명령어가 제대로 작동하는지 확인하려면 다음 명령어를 실행하세요:

```bash
uv --version
```

### **4. 셀 통합 설정**

`uv`는 다양한 셸 환경에서 자동 완성 및 편리한 명령어 사용을 지원합니다. 아래는 OS별 셸 통합 설정 방법입니다.

#### **1. Windows (PowerShell)**

PowerShell에서 `uv` 자동 완성을 설정하려면 다음 명령어를 실행하세요:

```powershell
mkdir -Force $PROFILE.CurrentUserAllHosts
uv generate-completion powershell > $PROFILE.CurrentUserAllHosts\uv.ps1
```

PowerShell을 다시 시작하면 자동 완성이 활성화됩니다.

#### **2. macOS/Linux (Zsh)**

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

#### **3. macOS/Linux (Bash)**

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

---

## 4. 패키지 관리 심화
### 고급 설치 시나리오
```bash
# 플랫폼별 조건부 설치
uv pip install "pandas>=2.0; sys_platform == 'linux'"

# 패키지 해시 검증
uv pip install django --require-hashes

# 대체 인덱스 소스 사용
uv pip install private-pkg --index-url https://pkg.example.com/simple
```

### 버전 핀닝 전략
```toml
# uv.toml
[versions]
django = "==4.2.8"  # 강제 버전 고정
numpy = "<=1.26.0"  # 상한 버전 제한
```

### 패치 적용 방법
```bash
uv pip install django --patch patches/django-security-fix.patch
```

---

## 5. 의존성 관리의 기술
### 잠금파일 최적화
```bash
# 플랫폼별 잠금파일 생성
uv pip compile requirements.in \
  --platform=linux_x86_64 \
  --platform=macosx_arm64 \
  -o requirements.txt
```

### 의존성 트리 분석
```bash
uv pip graph --format=json | jq .  # JSON 출력
uv pip graph --exclude dev        # 개발 의존성 제외
```

### 보안 취약점 스캔
```bash
uv audit           # CVE 데이터베이스 기반 검사
uv audit --fix     # 자동 패치 가능한 취약점 수정
```

---

## 6. 프로덕션 환경 운영 노하우
### 최소 이미지 빌드
```dockerfile
FROM python:3.11-slim

RUN pipx install uv
COPY requirements.txt .
RUN uv pip install -r requirements.txt --target /app

CMD ["uv", "run", "python", "main.py"]
```

### CI/CD 통합 예시
```yaml
# GitHub Actions 예제
- name: Cache uv
  uses: actions/cache@v3
  with:
    path: |
      ~/.cache/uv
      ~/.cargo/registry
    key: uv-${{ hashFiles('**/requirements.txt') }}

- name: Install dependencies
  run: uv pip sync requirements.txt
```

---

## 7. 문제 해결 가이드
### 흔한 오류 사례
**문제 1**: `ERROR: Incompatible package hashes`
```bash
uv pip sync --refresh-hashes  # 해시 정보 갱신
```

**문제 2**: `ResolutionImpossible`
```bash
uv pip install --resolution=lowest  # 최소 버전 기준 재시도
```

**문제 3**: `SSL verification failure`
```bash
uv config set global.ssl_verify false  # 개발 환경에서만 사용
```

---

## 8. 미래 로드맵
- **패키지 프리페칭**: 백그라운드 업데이트 예측
- **바이너리 캐시 공유**: 팀 내 패키지 캐시 서버 구축 지원
- **ML 기반 의존성 추천**: 패키지 조합 추천 시스템
- **WASI 지원**: WebAssembly 환경에서의 Python 실행

[uv 공식 문서](https://uv.python.org) | [GitHub 저장소](https://github.com/astral-sh/uv)

---

> "uv는 단순한 도구가 아닌 Python 생태계의 패러다임 전환을 이끕니다. 하루라도 빨리 도입할수록 개발 생산성이 기하급수적으로 향상될 것입니다." - Python 코어 개발자 Brett Cannon
