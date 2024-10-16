---
title: "VSCode에서 Ruff로 Python 코드 품질 관리하기"
date: 2024-10-01T01:10:56+09:00
draft: true
categories: [python]
tags: [python, vscode, ruff]
---


Python 개발자라면 코드 품질 관리의 중요성을 잘 알고 계실 겁니다. 오늘은 VSCode에서 Ruff를 사용하여 Python 코드의 품질을 효과적으로 관리하는 방법을 소개해 드리겠습니다.
<!--more-->

## Ruff란?

Ruff는 Python 코드를 위한 빠르고 강력한 linter입니다. 기존의 여러 도구(Flake8, Black, isort 등)의 기능을 통합하여 제공하며, 주요 특징과 기능은 다음과 같습니다.

- **성능**: Ruff는 Rust로 작성되었으며, Flake8이나 Black과 같은 전통적인 린터나 포맷터보다 **10-100배 더 빠른** 것으로 알려져 있습니다. 이러한 속도는 개발 중 실시간 피드백을 가능하게 하여 코딩 경험을 크게 향상시킵니다.

- **설치**: pip를 통해 쉽게 설치할 수 있습니다:
  ```bash
  pip install ruff
  ```

- **설정**: Ruff는 `pyproject.toml`, `ruff.toml`, 또는 `.ruff.toml`과 같은 파일을 통해 설정을 지원하여 사용자가 줄 길이나 무시할 규칙 등을 커스터마이즈할 수 있습니다.

## 특징

- **린팅과 포맷팅**: Ruff는 `ruff check` 명령으로 린팅을, `ruff format` 명령으로 포맷팅을 수행할 수 있어 코드 품질 유지를 위한 다목적 도구입니다.

- **광범위한 규칙 세트**: Flake8, isort 등 인기 있는 도구들에서 영감을 받은 **800개 이상의 내장 규칙**을 포함합니다. 이 광범위한 규칙 세트는 스타일 위반부터 잠재적 버그까지 다양한 코딩 문제를 식별하는 데 도움을 줍니다.

- **자동 수정**: Ruff는 사용되지 않는 import 제거와 같은 특정 오류를 자동으로 수정할 수 있는 기능을 제공하여 개발자의 생산성을 향상시킵니다.

- **통합**: 다양한 편집기(예: VS Code)와 잘 통합되며 CI/CD 파이프라인에서 사용할 수 있어 로컬 개발과 팀 환경 모두에 적합합니다.

## 사용 사례

Ruff는 특히 다음과 같은 경우에 유용합니다:

- **코드 리뷰 프로세스**: 일관된 품질을 보장하여 코드 리뷰를 간소화합니다.
- **지속적 통합**: CI/CD 워크플로우에서 품질 검사를 자동화합니다.
- **대규모 코드베이스**: 전통적인 도구들이 현저히 느려질 수 있는 대규모 프로젝트에 이상적입니다.



## VSCode에서 Ruff 설정하기

### 1. Ruff 확장 설치

먼저 VSCode 마켓플레이스에서 "Ruff" 확장을 검색하여 설치합니다.

### 2. ruff.toml 설정

프로젝트 루트 디렉토리에 `ruff.toml` 파일을 생성하고 다음과 같이 설정합니다:

```toml
# Black과 동일합니다.
line-length = 88
indent-width = 4

# 밑줄로 시작하는 미사용 변수를 허용합니다.
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

# Python 3.12을 가정합니다.
target-version = "py312"

# 일반적으로 무시되는 다양한 디렉토리를 제외합니다.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
]

[lint]
# https://docs.astral.sh/ruff/rules/ 참고
# E: pycodestyle 오류 (PEP 8 스타일 가이드)
# F: Pyflakes (논리적 오류 및 잠재적 버그)
# I: isort (import 정렬)
# N: pep8-naming (이름 지정 규칙)
# S: flake8-bandit (보안 이슈)
# B: flake8-bugbear (추가적인 버그 및 디자인 문제 검출)
# A: flake8-builtins (내장 함수 이름 오용 검사)
select = ["E", "F", "I", "N", "B"]  
ignore = []
fixable = ["ALL"]
unfixable = []

[mccabe]
max-complexity = 10

[flake8-quotes]
docstring-quotes = "double"

[flake8-tidy-imports]
ban-relative-imports = "all"

[pycodestyle]
max-doc-length = 88

[pydocstyle]
convention = "google"

[pylint]
max-args = 8
max-branches = 12
max-returns = 6
max-statements = 50

[pyupgrade]
keep-runtime-typing = true

[format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
docstring-code-format = false
docstring-code-line-length = "dynamic"
```

이 설정은 Black 스타일을 따르면서도 Ruff의 다양한 기능을 활용합니다.

### 3. VSCode settings.json 설정

VSCode의 설정 또는 프로젝트의 `.vscode/settings.json` 파일에 다음 설정을 추가합니다:

```json
{
    "ruff.enable": true,
    "python.languageServer": "Pylance",
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    "python.analysis.diagnosticMode": "workspace",
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    }
}
```

## 설정 설명

1. **Ruff 활성화**: `"ruff.enable": true`로 Ruff를 활성화합니다.

2. **언어 서버**: Pylance를 사용하여 더 나은 Python 지원을 받습니다.

3. **타입 체크**: `"basic"` 모드로 설정하여 기본적인 타입 체크를 수행합니다.

4. **자동 import**: 자동 import 제안 기능을 활성화합니다.

5. **진단 모드**: 전체 작업 공간에 대해 진단을 수행합니다.

6. **Python 파일 설정**:
   - 저장 시 자동 포맷팅을 활성화합니다.
   - Ruff를 기본 포맷터로 설정합니다.
   - 저장 시 자동으로 import를 정리합니다.

## 결론

이렇게 설정하면 VSCode에서 Python 개발 시 Ruff를 통해 자동으로 코드 품질을 관리할 수 있습니다. 저장할 때마다 코드가 자동으로 포맷팅되고, import가 정리되며, 다양한 lint 규칙이 적용됩니다. 이를 통해 일관된 코드 스타일을 유지하고, 잠재적인 버그를 사전에 방지할 수 있습니다.

Ruff의 빠른 성능 덕분에 대규모 프로젝트에서도 원활하게 사용할 수 있으며, 하나의 도구로 여러 가지 코드 품질 관리 작업을 수행할 수 있어 매우 효율적입니다.

이제 여러분도 VSCode와 Ruff를 활용하여 더 나은 Python 코드를 작성해보세요!
