---
title: "Claude Code 플러그인 완전 가이드: 개발부터 활용까지"
date: 2026-02-12T10:00:00+09:00
draft: true
description: "Claude Code의 플러그인 시스템을 통해 프로젝트와 팀 전체에서 공유할 수 있는 사용자 정의 기능으로 확장하는 방법을 소개합니다."
tags: ["Claude Code", "Plugin", "AI Coding", "Automation"]
---

Claude Code의 **플러그인 시스템**을 사용하면 프로젝트와 팀 전체에서 공유할 수 있는 사용자 정의 기능으로 Claude Code를 확장할 수 있습니다.

마켓플레이스에서 미리 빌드된 플러그인을 설치하거나, 워크플로우 자동화를 위해 자신만의 플러그인을 만들 수 있습니다.

<!--more-->

## 플러그인이란?

플러그인은 다음 구성 요소를 포함할 수 있는 **확장 가능한 단위**입니다:

- **명령(Commands)**: 슬래시 명령어로 실행되는 사용자 정의 기능
- **에이전트(Agents)**: 특정 작업에 특화된 전문화된 AI 어시스턴트
- **스킬(Skills)**: 모델의 기능을 확장하는 재사용 가능한 지식 베이스
- **훅(Hooks)**: 이벤트 핸들러를 통한 워크플로우 자동화
- **MCP 서버**: 외부 도구와 서비스에 연결

## 플러그인 구조

기본 플러그인 구조는 다음과 같습니다:

```
my-plugin/
├── .claude-plugin/           # 필수: 플러그인 메타데이터
│   └── plugin.json          # 플러그인 매니페스트
├── commands/                 # 선택: 슬래시 명령어
│   └── my-command.md
├── agents/                   # 선택: 사용자 정의 에이전트
│   └── specialist.md
├── skills/                   # 선택: 에이전트 스킬
│   └── my-skill/
│       └── SKILL.md
│       ├── README.md        # 추가 문서 (선택)
│       └── examples/        # 예제 파일 (선택)
├── hooks/                    # 선택: 이벤트 핸들러
│   └── hooks.json
│   └── pre-commit.py        # 핸 스크립트
├── .mcp.json                # 선택: MCP 서버 설정
└── README.md                # 플러그인 문서
```

### plugin.json 구조

플러그인 매니페스트 파일은 플러그인의 메타데이터를 정의합니다:

```json
{
  "name": "my-plugin",
  "description": "플러그인에 대한 간단한 설명",
  "version": "1.0.0",
  "author": {
    "name": "작성자 이름",
    "email": "email@example.com"
  },
  "license": "MIT",
  "claude": {
    "minVersion": "1.0.0"
  }
}
```

### Commands (명령어)

사용자가 슬래시(`/`)로 실행하는 기능입니다.

**Frontmatter 옵션:**
```yaml
---
description: "명령어에 대한 간단한 설명"
argument-hint: "<required-arg> [optional-arg]"
allowed-tools: [Read, Glob, Grep, Bash]
model: "opus"
---

# 명령어 제목

명령어가 실행될 때 수행할 작업을 설명합니다...

## Arguments

사용자가 제공한 인수: $ARGUMENTS
```

**주요 Frontmatter 필드:**
- `description`: `/help`에 표시될 설명
- `argument-hint`: 인수 힌트 표시
- `allowed-tools`: 미리 승인된 도구 목록
- `model`: 사용할 모델 (haiku, sonnet, opus)

### Agents (에이전트)

특정 작업에 특화된 전문 AI 어시스턴트입니다.

**에이전트 구조:**
```yaml
---
name: specialist
description: "에이전트를 사용할 시기 설명"
model: inherit
color: yellow
tools: ["Read", "Grep", "Bash"]
---

당신은 전문 분야 전문가입니다...

**작업:**
1. 첫 번째 단계
2. 두 번째 단계
...
```

**주요 Frontmatter 필드:**
- `name`: 에이전트 식별자
- `description`: 에이전트를 언제 사용할지 설명 (매우 중요!)
- `model`: 사용할 모델 (inherit, haiku, sonnet, opus)
- `color`: UI 표시 색상
- `tools`: 에이전트가 사용할 수 있는 도구

### Skills (스킬)

Claude가 자동으로 사용하는 재사용 가능한 지식 베이스입니다.

**스킬 구조:**
```
skills/
└── my-skill/
    └── SKILL.md          # 필수
    ├── README.md         # 선택
    ├── references/       # 참고 자료
    └── examples/         # 예제 파일
```

### Hooks (훅)

특정 이벤트 발생 시 자동으로 실행되는 핸들러입니다.

**hooks.json 구조:**
```json
{
  "description": "훅 플러그인 설명",
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/pretooluse.py",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [...],
    "UserPromptSubmit": [...],
    "Stop": [...]
  }
}
```

**지원되는 훅 이벤트:**
- `PreToolUse`: 도구 사용 전
- `PostToolUse`: 도구 사용 후
- `UserPromptSubmit`: 사용자 프롬프트 제출 시
- `Stop`: 세션 중지 시

**환경 변수:**
- `${CLAUDE_PLUGIN_ROOT}`: 플러그인 루트 경로

### MCP 서버

외부 도구와 서비스에 연결합니다.

**.mcp.json 구조:**
```json
{
  "my-server": {
    "type": "http",
    "url": "https://api.example.com/mcp"
  },
  "local-server": {
    "type": "command",
    "command": "node",
    "args": ["server.js"]
  }
}
```

## 플러그인 설치 및 관리

### 마켓플레이스 추가

플러그인을 발견하고 설치하기 위해 마켓플레이스를 추가합니다:

```bash
/plugin marketplace add your-org/claude-plugins
```

### 플러그인 설치

```bash
# 특정 플러그인 설치
/plugin install formatter@your-org

# 플러그인 활성화
/plugin enable plugin-name@marketplace-name

# 플러그인 비활성화 (제거하지 않음)
/plugin disable plugin-name@marketplace-name

# 플러그인 완전 제거
/plugin uninstall plugin-name@marketplace-name
```

## 첫 번째 플러그인 만들기

간단한 인사말 명령을 추가하는 플러그인을 만들어 봅시다.

### 1. 플러그인 폴더 생성

```bash
mkdir -p hello-plugin/.claude-plugin
cd hello-plugin
```

### 2. plugin.json 작성

```json
{
  "name": "hello-plugin",
  "version": "1.0.0",
  "description": "간단한 인사말 명령을 제공합니다",
  "author": "your-name"
}
```

### 3. 명령 추가

`commands/hello.md` 파일을 생성합니다:

```markdown
---
description: "친결한 인사말을 출력합니다"
---

안녕하세요! Claude Code 플러그인 개발에 온 것을 환영합니다!
```

### 4. 로컬에서 테스트

```bash
/plugin marketplace add ./
/plugin install hello-plugin
/hello
```

## 스킬 추가하기

플러그인에 에이전트 스킬을 추가하여 Claude의 기능을 확장할 수 있습니다.

### 스킬 구조

```
skills/
└── code-review/
    └── SKILL.md
```

### SKILL.md 예제

```markdown
---
description: "코드를 리뷰하고 개선 사항을 제안합니다"
parameters:
  - name: code
    description: "리뷰할 코드"
    required: true
---

# 코드 리뷰

제공된 코드를 분석하고 다음 측면에서 리뷰합니다:

1. **버그 및 잠니ial 오류**
2. **성능 최적화 기회**
3. **코드 스타일 일치성**
4. **보안 문제**

...
```

## 팀 플러그인 설정

저장소 수준에서 플러그인을 구성하면 팀 전체에서 일관된 도구를 사용할 수 있습니다.

### .claude/settings.json 구성

```json
{
  "marketplaces": [
    "your-org/shared-plugins"
  ],
  "plugins": {
    "shared-formatter": {
      "source": "marketplace",
      "marketplace": "your-org/shared-plugins",
      "enabled": true
    }
  }
}
```

## 활용 예제

### 예제 1: 코드 포멧팅 플러그인

프로젝트의 코딩 스타일을 자동으로 적용하는 플러그인:

```json
{
  "name": "project-formatter",
  "hooks": {
    "pre-commit": "format-code"
  }
}
```

### 예제 2: API 문서 생성 스킬

API 엔드포인트에서 자동으로 문서를 생성하는 스킬:

```markdown
---
description: "API 엔드포인트에서 문서를 생성합니다"
---

엔드포인트를 분석하고 OpenAPI 스펵명을 생성합니다...
```

### 예제 3: 배포 자동화

CI/CD 파이프라인과 연동하여 자동으로 배포하는 훅:

```json
{
  "hooks": {
    "after-success": "deploy-to-production"
  }
}
```

## MCP 개발 베스트 프랙티스

MCP 도구 개발 시 다음 원칙을 따르면 더 효과적인 플러그인을 만들 수 있습니다:

### 1. 더 적은, 더 초점화된 도구

하나의 API 엔드포인트마다 별도의 도구를 만들지 마세요. 대신 다단계 오퍼레이션을 하나의 도구로 통합하세요.

**나쁜 예제:**
```json
// 나쁜: 엔드포인트마다 분리된 도구
{
  "name": "list_users",
  "description": "사용자 목록을 가져옵니다"
}
{
  "name": "create_event",
  "description": "이벤트를 생성합니다"
}
```

**좋은 예제:**
```json
// 좋은: 하나의 도구로 다단계 오퍼레이션 처리
{
  "name": "schedule_event",
  "description": "사용자를 탐색하고 이벤트를 예약합니다",
  "parameters": {
    "user_query": "사용자 탐색 쿼리",
    "event_details": "이벤트 세부 정보"
  }
}
```

### 2. 서비스/리소스별 네임스페이스

도구 이름을 서비스나 리소스별로 네임스페이스하세요:

```json
{
  "asana_search": { "description": "Asana에서 탐색" },
  "asana_create": { "description": "Asana에 생성" },
  "jira_search": { "description": "Jira에서 탐색" },
  "jira_create": { "description": "Jira에 생성" }
}
```

### 3. 의미 있는 컨텍스트 반환

기술적 세부사항보다 시그널을 우선시하세요. `uuid` 대신 `name`을 사용하세요:

```json
// 나쁜
{
  "result": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "status": "active"
  }
}

// 좋은
{
  "result": {
    "name": "프로젝트 알파",
    "status": "진행 중",
    "assignee": "김개발"
  }
}
```

### 4. 응답 포멷 지원

에이전트가 "간결한" 또는 "상세한" 응답을 선택할 수 있도록 하세요:

```json
{
  "name": "get_repository_info",
  "parameters": {
    "format": {
      "type": "string",
      "enum": ["concise", "detailed"],
      "description": "응답 형식"
    }
  }
}
```

### 5. 토큰 효율 최적화

Claude Code는 최대 25,000 토큰 제한이 있습니다:

- 페이지네이션 구현
- 필터링 옵션 제공
- 결과 길이 자르기
- 관련 정보만 반환

## 시큐리티 베스트 프랙티스

플러그인 개발 시 다음 시큐리티 원칙을 따르세요:

### 1. 훅 기본 비활성화

모든 훅을 기본적으로 비활성화 상태로 시작하세요:

```json
{
  "hooks": {
    "pre-commit": {
      "enabled": false,
      "command": "security-scan"
    }
  }
}
```

### 2. MCP 서버 명시적 승인

알 수 없는 MCP 서버를 자동으로 연결하지 마세요:

```json
{
  "mcpServers": {
    "database": {
      "enabled": false,
      "requireApproval": true,
      "description": "프로덕션 데이터베이스 접속"
    }
  }
}
```

### 3. 에러 메시지 검토

에러 메시지에 민간한 정보를 포함하지 않도록 주의하세요. 에러 로그를 검토하여 시큐리티 문제를 확인하세요.

## 일반적인 실수 피하기

다음과 같은 실수를 피하세요:

- ❌ 하나의 API 엔드포인트마다 도구 생성
- ❌ 너무 많은 저수준 기술적 세부사항 반환
- ❌ 모호하거나 불확실한 도구 이름 사용
- ❌ 도구 설명 품질 간과
- ❌ 실제 에이전트 워크플로우 테스트 없음

## 베스트 프랙티스

1. **버전 관리**: `plugin.json`에서 의미 있는 버전 관리를 사용하세요
2. **문서화**: README.md에 설치 및 사용 지침을 포함하세요
3. **테스트**: 로컬 마켓플레이스에서 변경 사항을 반복적으로 테스트하세요
4. **커뮤니티 기여**: 플러그인 컬렉션에 기여하는 것을 고려하세요

## 참고자료

- [Claude Code 플러그인 공식 문서](https://code.claude.com/docs/ko/plugins)
- [Claude Code 플러그인 구조 완전 정복 - Vitalholic](https://vitalholic.tistory.com/426)
- [roboco-io/plugins: Claude Code 플러그인 모음 - GitHub](https://github.com/roboco-io/plugins)
- [Claude Code Survival Guide 2026 - LinkedIn](https://www.linkedin.com/pulse/claude-code-survival-guide-2026-skills-agents-mcp-servers-rob-foster-lq9we)
