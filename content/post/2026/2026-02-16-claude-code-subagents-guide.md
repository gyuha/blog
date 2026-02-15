---
title: "Claude Code Subagent 만들기: 실무에서 바로 쓰는 설계/구현 가이드"
date: 2026-02-16T01:40:00+09:00
draft: true
description: "Claude Code Subagent를 직접 만들고 운영하는 방법을 공식 문서 기준으로 정리하고, 블로그 자동화 사례를 통해 Agent/Skill 분리, 권한 설계, 병렬 실행 패턴까지 설명합니다."
categories: [AI, Development, Productivity]
tags: [claude, claude-code, subagent, multi-agent, automation, agent-sdk]
---

"에이전트는 많이 만들었는데, 왜 자꾸 컨텍스트가 오염되지?"

"읽기 전용 조사 작업인데 왜 메인 세션에서 토큰을 이렇게 많이 먹지?"

Claude Code를 오래 쓰다 보면 결국 **Subagent 설계**가 생산성을 결정합니다.

이 글은 Claude 공식 문서의 `sub-agents`를 중심으로, 실제로 바로 적용 가능한 방식으로 정리했습니다. 추가로 Agent SDK 관점과 멀티 에이전트 운영 사례를 함께 묶어서, "어디서부터 어떻게 시작하면 되는지"를 한 번에 이해할 수 있게 구성했습니다.

<!--more-->

## 1) Subagent가 정확히 뭔가?

Subagent는 특정 작업을 위임받아 처리하는 **전문화된 AI 워커**입니다.

핵심은 4가지입니다.

1. **독립 컨텍스트**에서 실행됨
2. 자체 **시스템 프롬프트**를 가짐
3. 사용할 **도구 권한(tools/disallowedTools)**을 분리 가능
4. 필요하면 모델(`haiku`, `sonnet`, `opus`, `inherit`)도 분리 가능

즉, "탐색/검토/수정"을 메인 세션에 다 몰아 넣지 않고, 역할별로 컨텍스트를 분리해서 운영할 수 있습니다.

## 2) Subagent vs Agent Teams, 뭐가 다른가?

둘 다 멀티 에이전트처럼 보이지만 목적이 다릅니다.

- **Subagent**: 단일 세션 안에서 특정 작업을 위임받아 처리한 뒤 결과를 반환
- **Agent Teams**: 여러 에이전트가 병렬로 돌아가며 서로 통신하고 조율하는 협업 구조

간단히 말하면:

- "코드베이스 조사만 빨리 해줘" -> Subagent
- "보안/성능/테스트 리뷰어를 팀으로 동시에 돌려줘" -> Agent Teams

## 3) 가장 빠른 시작 방법 (`/agents`)

가장 쉬운 방법은 Claude Code에서 `/agents`를 쓰는 것입니다.

```text
/agents
```

추천 흐름:

1. `Create new agent` 선택
2. `User-level` 또는 `Project-level` 선택
3. `Generate with Claude`로 초안 생성
4. 도구 권한(읽기 전용/전체)과 모델 선택
5. 저장 후 바로 호출

`User-level`은 여러 프로젝트에서 재사용할 때 좋고,
`Project-level(.claude/agents/)`은 팀과 함께 버전 관리할 때 좋습니다.

## 4) 수동으로 만들 때: Subagent 파일 템플릿

Subagent는 Markdown + YAML frontmatter 파일입니다.

예: `.claude/agents/code-reviewer.md`

```markdown
---
name: code-reviewer
description: 코드 변경 직후 품질/보안/유지보수성을 검토한다. 필요할 때 적극적으로 사용한다.
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: default
---

당신은 시니어 코드 리뷰어다.
변경 파일 중심으로 검토하고, 우선순위(critical/warning/suggestion)로 결과를 정리하라.
```

### 자주 쓰는 frontmatter 필드

- `name` (필수): 에이전트 식별자
- `description` (필수): Claude가 언제 이 에이전트를 호출할지 판단 기준
- `tools`: 허용 도구 목록
- `disallowedTools`: 금지 도구 목록
- `model`: `haiku` / `sonnet` / `opus` / `inherit`
- `permissionMode`: `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`
- `skills`: 시작 시 주입할 스킬 목록
- `hooks`: PreToolUse/PostToolUse/Stop 등 라이프사이클 훅
- `memory`: `user`, `project`, `local` 범위 메모리

## 5) 실무 설계 원칙 (이거 먼저 지키면 실패 확률이 줄어듦)

### 원칙 A: 설명(description)을 가장 공들여 써라

Claude는 설명을 보고 라우팅합니다. 설명이 모호하면 호출 타이밍이 흔들립니다.

- 나쁜 예: "코드 잘 보는 에이전트"
- 좋은 예: "코드 변경 직후 보안/성능/테스트 누락을 점검하는 리뷰 에이전트"

### 원칙 B: 최소 권한으로 시작하라

처음부터 `Write/Edit/Bash`를 다 열지 말고, 읽기 전용으로 검증한 뒤 필요한 권한만 확장하세요.

### 원칙 C: 단일 책임으로 쪼개라

하나의 Subagent가 기획+구현+리뷰+배포까지 다 하게 만들면 다시 범용 에이전트가 됩니다.

- `explorer` (읽기 전용 탐색)
- `implementer` (수정)
- `reviewer` (검증)

이렇게 분리하면 훨씬 안정적입니다.

### 원칙 D: 토큰 폭탄 작업은 Subagent로 격리하라

대규모 로그 분석, 테스트 전체 실행, 문서 수집 같은 작업은 Subagent에 위임해서 메인 컨텍스트를 보호하세요.

## 6) 블로그 자동화 관점에서의 Subagent 설계 예시

질문이 자주 나옵니다.

"블로그 자동화를 할 때도 Subagent를 써야 하나요?"

답은 **Yes**입니다. 특히 다음처럼 나누면 좋습니다.

1. `keyword-researcher` (읽기 전용)
2. `content-planner` (읽기 + 정리)
3. `post-writer` (쓰기 허용)
4. `seo-reviewer` (읽기 전용 검수)

여기서 핵심은, 작성(`post-writer`) 권한을 다른 에이전트와 분리하는 것입니다. 그래야 잘못된 수정/덮어쓰기 리스크를 줄일 수 있습니다.

## 7) Hook으로 안전장치 걸기 (고급)

권한만으로 부족할 때는 `PreToolUse` 훅으로 명령을 필터링할 수 있습니다.

예를 들어 Bash는 허용하지만 위험 명령은 차단하도록 만들 수 있습니다.

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
```

검증 스크립트에서 금지 패턴을 감지하면 종료 코드 `2`로 차단합니다.

## 8) Agent SDK는 언제 필요한가?

Subagent를 CLI 안에서 운영하는 단계 다음으로,
백엔드 서비스/워크플로우에 내장하려면 Agent SDK를 고려할 수 있습니다.

- 장점: 앱/서버 코드에서 에이전트 실행 흐름을 직접 제어 가능
- 용도: 장기 세션 운영, 외부 시스템 연동, 커스텀 툴 체인 구성

다만, 처음에는 SDK부터 시작하기보다 **Claude Code 내 Subagent로 설계 검증**을 먼저 하는 편이 빠릅니다. 구조가 검증된 후 SDK로 올리는 것이 실패 비용이 낮습니다.

## 9) 바로 써먹는 체크리스트

새 Subagent를 만들 때 아래 7가지만 확인하세요.

1. `description`이 구체적인가?
2. 기본 도구 권한이 최소 권한인가?
3. 모델 선택 이유가 명확한가? (속도/비용/품질)
4. 단일 책임이 지켜졌는가?
5. 결과 출력 형식(예: 우선순위/파일경로)이 정해졌는가?
6. 실패 시 재시도 규칙이 있는가?
7. 팀 공유가 필요하면 `.claude/agents/`에 버전 관리되는가?

## 마무리

Subagent를 잘 만들면 "AI가 잘 답한다"를 넘어
**"AI 워크플로우가 재현 가능하게 굴러간다"** 단계로 올라갑니다.

처음에는 복잡하게 시작하지 말고,

- 읽기 전용 `explorer` 하나
- 수정 전용 `implementer` 하나
- 검수 전용 `reviewer` 하나

이 3개만 먼저 만들어 보세요.

그 다음에 hooks, memory, skills를 붙이면 됩니다.

## 참고 자료

- Claude Code 공식 문서 (Subagents): https://code.claude.com/docs/ko/sub-agents
- Bind AI 블로그 (Claude Agent SDK 개요): https://blog.getbind.co/how-to-create-agents-with-claude-agents-sdk/
- zoeylog (클로드 코드 자동화 사례): https://zoey.day/blog?post=1q3vdn2px1w382xy49pr
