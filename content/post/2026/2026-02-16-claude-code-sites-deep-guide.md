---
title: "Claude Code 사용자라면 꼭 알아둘 사이트 5선: 스킬/에이전트 생태계 실전 가이드"
date: 2026-02-16T01:58:00+09:00
draft: true
description: "Claude Code 관련 추천 링크 5개, 각 사이트의 역할, 강점, 추천 사용 시나리오, 주의점, 시작 방법까지 실무 관점으로 정리했습니다."
categories: [AI, Development, Productivity]
tags: [claude, claude-code, skills, agents, mcp, workflow, automation]
---

Claude Code 사용자라면, **무엇을 해결해주는지**, **어떤 상황에서 쓰면 좋은지**, **시작할 때 주의할 점은 무엇인지**까지 실무 기준으로 정리해봤습니다.

<!--more-->

## 먼저 한눈에: 어떤 사이트를 언제 쓰면 좋을까?

- **빠르게 실전 템플릿을 붙여서 시작**하고 싶다 -> [aitmpl.com/skills](https://www.aitmpl.com/skills)
- **스킬을 대량 탐색**하고 싶다 -> [skillsmp.com](https://skillsmp.com)
- **멀티 에이전트 오케스트레이션을 본격 도입**하고 싶다 -> [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)
- **생태계 전체 레퍼런스를 한곳에서 훑고 싶다** -> [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- **명령/페르소나/모드 중심 프레임워크**가 필요하다 -> [SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)

---

## 1) AITMPL Skills 
[https://www.aitmpl.com/skills](https://www.aitmpl.com/skills)

### 이 사이트는 무엇인가?

`Claude Code Templates`를 중심으로, 스킬/에이전트/커맨드/설정/훅/MCP/템플릿을 탐색하고 조합하는 허브입니다.

핵심은 "컴포넌트 조합형"입니다. 즉, 한두 개 기능만 설치하는 게 아니라 개발 스택을 묶어서 가져가는 방식이 강합니다.

### 강점

- 탐색 카테고리가 명확합니다: `skills`, `agents`, `commands`, `settings`, `hooks`, `mcps`, `templates`
- 스택 빌더처럼 **선택한 구성을 커맨드로 바로 생성**하는 흐름이 빠릅니다
- 기업/플랫폼별 묶음(OpenAI, Anthropic, GitHub 등)처럼 큐레이션이 있어 처음 진입이 쉽습니다

### 이런 경우에 추천

- 팀 온보딩할 때 "기본 개발 환경"을 빠르게 맞춰야 할 때
- 빈 프로젝트에서 Claude Code 운영 구성을 한 번에 세팅할 때
- 개별 스킬보다 "조합 가능한 스택"이 필요한 경우

### 주의할 점

- 템플릿 중심 사이트라서, 각 구성요소의 품질은 **원본 저장소별로 편차**가 있습니다
- 설치 전에 실제로 어떤 파일/권한/훅이 들어오는지 반드시 확인해야 합니다

### 시작 팁

1. 먼저 `skills`와 `agents`만 최소 구성으로 선택합니다
2. 로컬 테스트 후 `hooks`, `mcps`를 단계적으로 추가합니다
3. 팀 저장소 반영 전에는 개인 환경에서 충돌을 먼저 확인합니다

---

## 2) SkillsMP 
[https://skillsmp.com](https://skillsmp.com)

### 이 사이트는 무엇인가?

공개 GitHub 기반의 Agent Skill을 모아 검색/분류해주는 마켓플레이스입니다.

`SKILL.md` 생태계를 중심으로, Claude Code뿐 아니라 Codex/ChatGPT 계열과의 호환성을 강조합니다.

### 강점

- 스킬 규모가 매우 커서 "비슷한 문제를 이미 푼 스킬"을 찾기 좋습니다
- 키워드 + 의미 기반 검색(AI search)로 탐색 효율이 좋습니다
- 카테고리/인기도/최근 업데이트 관점으로 후보를 빠르게 줄일 수 있습니다

### 이런 경우에 추천

- "내가 지금 필요한 스킬이 이미 존재하는지"부터 확인하고 싶을 때
- 도메인별(테스트, DevOps, 데이터, 문서화)로 실전 예시를 수집할 때
- 팀 내부 커스텀 스킬 설계 전에 벤치마크가 필요할 때

### 주의할 점

- 커뮤니티 수집형이므로 **공식 품질 보증 저장소가 아닙니다**
- 설치 전 `SKILL.md`와 포함 스크립트의 동작/권한을 직접 검토해야 합니다
- 인기 순위만 보고 도입하면 내 워크플로우와 맞지 않을 수 있습니다

### 시작 팁

1. 문제를 먼저 문장으로 정의합니다 (예: "PR 리뷰 자동화")
2. 상위 후보 3개만 골라 `SKILL.md`와 허용 도구를 비교합니다
3. 프로젝트 루트(`.claude/skills`)에 넣기 전에 개인 영역에서 먼저 검증합니다

---

## 3) Oh My ClaudeCode 
[https://github.com/Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)

### 이 저장소는 무엇인가?

Claude Code를 팀 단위로 운용할 때 필요한 **멀티 에이전트 오케스트레이션 프레임워크**입니다.

핵심 메시지는 "Zero learning curve, Team-first orchestration"에 가깝고, 팀 모드/자동 위임/검증 루프를 강하게 밀고 있습니다.

### 강점

- 팀 파이프라인(계획 -> 실행 -> 검증 -> 보정)처럼 **단계형 워크플로우**가 명확합니다
- 여러 오케스트레이션 모드(autopilot, ultrawork, ralph 등)로 상황별 선택이 가능합니다
- 운영 편의 기능(상태 추적, 비용 최적화, 자동 재개 유틸리티)이 잘 정리되어 있습니다

### 이런 경우에 추천

- 단일 프롬프트보다 "역할 분리 + 검증 루프"가 중요한 팀
- 장기 리팩터링/마이그레이션처럼 대형 작업을 구조적으로 돌리고 싶은 경우
- 개인 실험 단계를 넘어 팀 표준 워크플로우를 만들고 싶은 경우

### 주의할 점

- 기능이 많은 만큼 초기 학습 없이 바로 전면 도입하면 오히려 복잡해질 수 있습니다
- 기존 팀 규칙(CLAUDE.md, 훅, 커맨드 체계)과 충돌하는지 먼저 봐야 합니다
- 프로젝트 브랜딩명과 패키지명 차이 같은 설치 포인트를 확인해야 합니다

### 시작 팁

1. 처음부터 모든 모드를 켜지 말고 `team` 또는 `autopilot` 하나만 선택합니다
2. "작은 리포 하나"에서 1주일 정도 운영해보고 룰을 고정합니다
3. 통과 기준(테스트/타입체크/리뷰 기준)을 먼저 정의한 뒤 확장합니다

---

## 4) Awesome Claude Code 
[https://github.com/hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

### 이 저장소는 무엇인가?

Claude Code 생태계 리소스를 폭넓게 모은 큐레이션 리스트입니다.

스킬, 훅, 슬래시 커맨드, 툴링, 워크플로우, CLAUDE.md 예시까지 "지도"처럼 탐색할 수 있는 레퍼런스 허브에 가깝습니다.

### 강점

- 카테고리 분류가 좋아서 "무엇을 찾아야 하는지 모를 때" 출발점이 됩니다
- 최신 추가 항목을 통해 생태계 변화 속도를 빠르게 파악할 수 있습니다
- 특정 프레임워크에 락인되지 않고 비교 탐색이 가능합니다

### 이런 경우에 추천

- 지금 당장 도구를 설치하기보다, 먼저 지형도를 그리고 싶을 때
- 팀 표준을 만들기 전에 대안들을 비교하고 싶을 때
- Claude Code 학습 로드맵/참고 자료를 한 번에 모으고 싶을 때

### 주의할 점

- 큐레이션 저장소 특성상 항목 수가 많아 "선택 피로"가 생길 수 있습니다
- 모든 링크가 내 프로젝트 성숙도와 맞는 것은 아닙니다

### 시작 팁

1. 카테고리 1개만 정해(예: Hooks) 30분 타임박스로 탐색합니다
2. "이번 주에 적용할 후보 2개"만 선정합니다
3. 적용 후 효과를 기록하고 다음 카테고리로 넘어갑니다

---

## 5) SuperClaude Framework 
[https://github.com/SuperClaude-Org/SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)

### 이 저장소는 무엇인가?

Claude Code를 명령 체계/전문화 에이전트/행동 모드로 확장하는 구성 프레임워크입니다.

핵심은 "구조화된 개발 플랫폼"처럼 쓰게 만드는 것이고, 커맨드 중심 운영과 MCP 연동 전략이 잘 정리되어 있습니다.

### 강점

- 슬래시 커맨드 기반 운영 문서가 잘 되어 있어 재현성이 좋습니다
- 전용 에이전트와 모드 개념이 분리되어 역할 설계가 쉽습니다
- 연구/구현/테스트/운영 흐름을 하나의 프레임에서 다루기 좋습니다

### 이런 경우에 추천

- 커맨드 기반 개발 습관을 팀에 강하게 정착시키고 싶은 경우
- "문서화된 규칙 + 반복 가능한 실행"이 중요한 조직
- MCP를 붙여 자동화 범위를 넓히고 싶은 경우

### 주의할 점

- 버전별 설치 경로와 기능 상태(예: 향후 플러그인 계획)가 바뀔 수 있습니다
- 기능 확장 전에 현재 안정 버전의 설치/운영 가이드를 먼저 확인해야 합니다

### 시작 팁

1. 공식 설치 가이드의 "현재 안정 버전" 절차만 먼저 따릅니다
2. 핵심 커맨드 3개만 선정해 팀 공통 루틴으로 고정합니다
3. 운영 로그를 보며 모드/서버를 점진적으로 늘립니다

---

## 상황별 추천 조합

### A. 입문자/개인 개발자

- `Awesome Claude Code`로 지형 파악
- `AITMPL`에서 최소 템플릿 도입
- `SkillsMP`로 필요한 스킬 1~2개만 추가

### B. 팀 단위 자동화 초입

- `Oh My ClaudeCode` 또는 `SuperClaude` 중 하나를 핵심 프레임으로 선택
- 나머지는 보조 레퍼런스/스킬 공급원으로 사용

### C. 도구 실험을 빠르게 반복해야 하는 팀

- `SkillsMP` + `Awesome Claude Code`로 후보 발굴
- `Oh My ClaudeCode`/`SuperClaude`로 운영 체계화

---

## 마무리

핵심은 "많이 깔기"가 아니라 "문제-도구 매칭"입니다.

사이트 5개를 다 써야 하는 게 아니라, 지금 내 병목을 가장 빨리 푸는 순서로 들어가면 됩니다.

추천 시작 순서 하나만 남기면:

1. `awesome-claude-code`로 선택지 파악
2. `skillsmp`로 구체 스킬 후보 압축
3. `aitmpl`로 초기 스택 구성
4. 팀 단계에서 `oh-my-claudecode` 또는 `superclaude` 중 하나를 채택

---

### 참고 링크

- [AITMPL Skills](https://www.aitmpl.com/skills)
- [SkillsMP](https://skillsmp.com)
- [Oh My ClaudeCode](https://github.com/Yeachan-Heo/oh-my-claudecode)
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code)
- [SuperClaude Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)
