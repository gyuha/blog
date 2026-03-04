---
title: "oh-my-claudecode: Claude Code를 위한 멀티 에이전트 오케스트레이션 플러그인"
date: 2026-03-04T15:00:00+09:00
draft: false
categories:
  - AI
  - Development
tags:
  - claude-code
  - multi-agent
  - orchestration
  - vibe-coding
  - automation
description: "한국인 개발자가 만든 Claude Code용 올인원 플러그인 oh-my-claudecode를 소개한다. 32개 전문 에이전트가 역할별로 나누어 설계, 구현, 검증을 자동화하고 병렬 실행으로 생산성을 극대화하는 방법을 살펴본다."
---

바이브 코딩(Vibe Coding) 시대에 혼자서 설계, 코딩, 리뷰, 테스트를 모두 처리하는 것은 비효율적이다. 한국인 개발자 **@bellman.pub** 가 개발한 **oh-my-claudecode** 는 Claude Code를 위한 oh-my-zsh 같은 올인원 플러그인으로, 32개 전문 에이전트가 역할별로 나누어 작업을 처리한다.

<!--more-->

## Sources

- [Threads - @vibe.tip 소개 포스트](https://www.threads.com/@vibe.tip/post/DVcxahkkzBh)
- [GitHub - Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)

## oh-my-claudecode란?

oh-my-claudecode는 Claude Code CLI를 위한 **Teams-first Multi-agent orchestration** 플러그인이다. 핵심 철학은 "Claude Code를 배우지 말고 그냥 OMC를 쓰라"는 것으로, 제로 설정으로 동작하며 자연어로 작업을 지시하면 전문 에이전트들이 알아서 처리한다.

```mermaid
flowchart TB
    classDef input fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef plan fill:#fff3e0,stroke:#ef6c00,color:#e65100
    classDef exec fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef verify fill:#fce4ec,stroke:#c2185b,color:#880e4f
    classDef agent fill:#f3e5f5,stroke:#7b1fa2,color:#4a148c
    classDef output fill:#e0f7fa,stroke:#00838f,color:#006064

    subgraph Input["사용자 입력"]
        U[자연어 요청]:::input
    end

    subgraph OMC["oh-my-claudecode 오케스트레이션"]
        TP[Team Planner]:::plan
        PRD[PRD 생성]:::plan
        EX[Executor 실행]:::exec
        VF[Verifier 검증]:::verify
        FX[Fixer 수정]:::exec
    end

    subgraph Agents["32개 전문 에이전트"]
        A1[Architect]:::agent
        A2[Executor]:::agent
        A3[Verifier]:::agent
        A4[Researcher]:::agent
        A5[Designer]:::agent
        A6[Test Engineer]:::agent
        A7[Code Reviewer]:::agent
        A8[...]:::agent
    end

    subgraph Output["결과"]
        R[완성된 코드]:::output
    end

    U --> TP
    TP --> PRD --> EX --> VF
    VF -->|실패| FX
    FX --> EX
    VF -->|성공| R

    TP -.-> A1
    EX -.-> A2
    VF -.-> A3
    A1 -.-> A4
    A2 -.-> A5
    A3 -.-> A6
    A4 -.-> A7
```

### 핵심 특징

| 특징 | 설명 |
|------|------|
| **제로 설정** | 지능형 기본값으로 별도 설정 없이 바로 사용 가능 |
| **Team-first 오케스트레이션** | Team 모드가 정식 오케스트레이션 표면 |
| **자연어 인터페이스** | 명령어를 외울 필요 없이 원하는 것을 설명하면 됨 |
| **자동 병렬화** | 복잡한 작업이 전문 에이전트에 분산됨 |
| **지속적 실행** | 작업이 완전히 검증될 때까지 포기하지 않음 |
| **비용 최적화** | 스마트 모델 라우팅으로 토큰 30-50% 절약 |
| **경험 학습** | 문제 해결 패턴을 자동으로 추출하여 재사용 |
| **실시간 가시성** | HUD statusline에서 내부 동작을 실시간 확인 |

## 오케스트레이션 모드

oh-my-claudecode는 다양한 사용 사례에 맞춰 여러 오케스트레이션 전략을 제공한다. v4.1.7부터 **Team** 모드가 정식 오케스트레이션 표면이며, 기존 swarm/ultrapilot은 Team으로 라우팅된다.

```mermaid
flowchart LR
    classDef mode fill:#e8eaf6,stroke:#3949ab,color:#1a237e
    classDef usecase fill:#fff8e1,stroke:#ffa000,color:#ff6f00
    classDef recommend fill:#c8e6c9,stroke:#43a047,color:#2e7d32

    subgraph Modes["오케스트레이션 모드"]
        T[Team<br/>권장]:::recommend
        OT[omc-teams<br/>tmux CLI]:::mode
        CCG[ccg<br/>Tri-model]:::mode
        AP[Autopilot<br/>단일 리드]:::mode
        UW[Ultrawork<br/>최대 병렬]:::mode
        RP[Ralph<br/>지속 모드]:::mode
        PL[Pipeline<br/>순차 처리]:::mode
    end

    subgraph UseCases["사용 사례"]
        UC1[협업 작업]:::usecase
        UC2[Codex/Gemini CLI]:::usecase
        UC3[혼합 백엔드+UI]:::usecase
        UC4[간단한 기능]:::usecase
        UC5[대량 리팩토링]:::usecase
        UC6[완료 보장]:::usecase
        UC7[엄격 순서]:::usecase
    end

    T --> UC1
    OT --> UC2
    CCG --> UC3
    AP --> UC4
    UW --> UC5
    RP --> UC6
    PL --> UC7
```

### Team 모드 (권장)

Team 모드는 스테이지드 파이프라인으로 동작한다:

```
team-plan → team-prd → team-exec → team-verify → team-fix (loop)
```

사용 예시:

```bash
/team 3:executor "fix all TypeScript errors"
```

Team 모드를 활성화하려면 `~/.claude/settings.json`에 다음을 추가한다:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### omc-teams: tmux CLI 워커

v4.4.0부터 Codex/Gemini MCP 서버 대신 **실제 CLI 프로세스**를 tmux 분할 창에서 실행할 수 있다:

```bash
/omc-teams 2:codex   "review auth module for security issues"
/omc-teams 2:gemini  "redesign UI components for accessibility"
/omc-teams 1:claude  "implement the payment flow"
```

| 스킬 | 워커 | 용도 |
|------|------|------|
| `/omc-teams N:codex` | N개 Codex CLI 창 | 코드 리뷰, 보안 분석, 아키텍처 |
| `/omc-teams N:gemini` | N개 Gemini CLI 창 | UI/UX 디자인, 문서, 대형 컨텍스트 |
| `/omc-teams N:claude` | N개 Claude CLI 창 | tmux 내 Claude CLI 일반 작업 |
| `/ccg` | Codex 1 + Gemini 1 | 병렬 tri-model 오케스트레이션 |

워커는 필요시 생성되고 작업 완료 시 종료되어 유휴 리소스를 소비하지 않는다.

### 매직 키워드

파워 유저를 위한 선택적 단축어들이다. 자연어로도 충분히 동작한다:

| 키워드 | 효과 | 예시 |
|--------|------|------|
| `team` | 정식 Team 오케스트레이션 | `/team 3:executor "fix TypeScript errors"` |
| `omc-teams` | tmux CLI 워커 | `/omc-teams 2:codex "security review"` |
| `ccg` | Tri-model Codex+Gemini | `/ccg review this PR` |
| `autopilot` | 완전 자율 실행 | `autopilot: build a todo app` |
| `ralph` | 지속성 모드 | `ralph: refactor auth` |
| `ulw` | 최대 병렬성 | `ulw fix all errors` |
| `plan` | 계획 인터뷰 | `plan the API` |
| `ralplan` | 반복 합의 계획 | `ralplan this feature` |
| `deep-interview` | 소크라테스식 요구사항 명확화 | `deep-interview "vague idea"` |

## 워크플로우: 막연한 아이디어에서 완성된 코드까지

oh-my-claudecode의 대표적인 워크플로우는 세 단계로 구성된다:

```mermaid
flowchart TD
    classDef step1 fill:#e3f2fd,stroke:#1976d2,color:#0d47a1
    classDef step2 fill:#fff3e0,stroke:#f57c00,color:#e65100
    classDef step3 fill:#e8f5e9,stroke:#388e3c,color:#1b5e20
    classDef success fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
    classDef fail fill:#ffebee,stroke:#d32f2f,color:#b71c1c

    subgraph Step1["1단계: deep-interview"]
        I[막연한 아이디어]:::step1 --> Q[소크라테스식 질문]:::step1
        Q --> C[명확화된 요구사항]:::step1
    end

    subgraph Step2["2단계: ralplan"]
        C --> P[Planner]:::step2
        P --> A[Architect]:::step2
        A --> CR[Critic]:::step2
        CR -->|피드백| P
        CR -->|합의| D[확정 설계]:::success
    end

    subgraph Step3["3단계: autopilot"]
        D --> E[구현]:::step3
        E --> T[테스트]:::step3
        T --> V[검증]:::step3
        V -->|실패| E
        V -->|성공| O[완성된 코드]:::success
    end

    Step1 --> Step2 --> Step3
```

### 1단계: deep-interview

요구사항이 불명확하거나 아이디어가 막연할 때 사용한다. 소크라테스식 질문을 통해 숨겨진 가정을 드러내고 가중치가 적용된 차원에서 명확성을 측정한다.

```bash
/deep-interview "I want to build a task management app"
```

### 2단계: ralplan

Planner, Architect, Critic 세 에이전트가 합의할 때까지 설계를 반복한다. 코드를 작성하기 전에 설계부터 확실히 잡는다.

```bash
/ralplan this feature
```

### 3단계: autopilot

구현부터 테스트까지 한 번에 끝낸다. 자주 쓰는 모드 중 하나로, 말하면 알아서 처리한다.

```bash
autopilot: build a REST API for managing tasks
```

## 32개 전문 에이전트

oh-my-claudecode는 아키텍처, 연구, 디자인, 테스트, 데이터 과학 등 다양한 영역의 **32개 전문 에이전트**를 제공한다:

```mermaid
flowchart LR
    classDef planning fill:#e8eaf6,stroke:#5c6bc0,color:#283593
    classDef execution fill:#e8f5e9,stroke:#66bb6a,color:#2e7d32
    classDef quality fill:#fce4ec,stroke:#ec407a,color:#ad1457
    classDef research fill:#fff3e0,stroke:#ffa726,color:#e65100
    classDef design fill:#e0f7fa,stroke:#26c6da,color:#00838f

    subgraph Agents["32개 전문 에이전트"]
        subgraph Planning["계획 & 설계"]
            PL[Planner]:::planning
            AR[Architect]:::planning
            AN[Analyst]:::planning
        end

        subgraph Execution["실행"]
            EX[Executor]:::execution
            DE[Deep Executor]:::execution
            CS[Code Simplifier]:::execution
        end

        subgraph Quality["품질 보증"]
            CR[Code Reviewer]:::quality
            TE[Test Engineer]:::quality
            VF[Verifier]:::quality
            QU[Quality Reviewer]:::quality
            SR[Security Reviewer]:::quality
        end

        subgraph Research["연구 & 분석"]
            RS[Researcher]:::research
            SC[Scientist]:::research
            EX2[Explore]:::research
            DB[Debugger]:::research
        end

        subgraph Design["디자인"]
            DS[Designer]:::design
            DC[Document Specialist]:::design
        end
    end
```

주요 에이전트 역할:

| 에이전트 | 역할 |
|----------|------|
| **Architect** | 설계 및 구조 결정 |
| **Executor** | 구현 및 코드 작성 |
| **Verifier** | 검증 및 품질 확인 |
| **Code Reviewer** | 코드 리뷰 (보안, 성능, 모범 사례) |
| **Test Engineer** | 테스트 전략 및 커버리지 |
| **Security Reviewer** | 보안 취약점 탐지 (OWASP Top 10) |
| **Researcher** | 코드베이스 탐색 및 조사 |
| **Debugger** | 근본 원인 분석 및 디버깅 |
| **Designer** | UI/UX 디자인 |
| **Scientist** | 데이터 분석 및 연구 실행 |

## 설치 및 설정

### 설치

세 줄이면 설치 완료다:

```bash
# 1. 마켓플레이스 추가
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode

# 2. 플러그인 설치
/plugin install oh-my-claudecode

# 3. 설정 실행
/omc-setup
```

### 업데이트

```bash
# 1. 마켓플레이스 업데이트
/plugin marketplace update omc

# 2. 설정 새로고침
/omc-setup
```

### 요구사항

- Claude Code CLI
- Claude Max/Pro 구독 또는 Anthropic API 키

### 선택적 Multi-AI 오케스트레이션

OMC는 선택적으로 외부 AI 제공자를 오케스트레이션할 수 있다:

| 제공자 | 설치 | 활성화 기능 |
|--------|------|-------------|
| Gemini CLI | `npm install -g @google/gemini-cli` | 디자인 리뷰, UI 일관성 (1M 토큰 컨텍스트) |
| Codex CLI | `npm install -g @openai/codex` | 아키텍처 검증, 코드 리뷰 교차 확인 |

비용 측면에서 Claude + Gemini + ChatGPT Pro 3개 플랜으로 월 ~$60에 모든 것을 커버할 수 있다.

## 유틸리티 기능

### Rate Limit Wait

속도 제한이 리셋될 때 Claude Code 세션을 자동으로 재개한다:

```bash
omc wait          # 상태 확인 및 안내
omc wait --start  # 자동 재개 데몬 활성화
omc wait --stop   # 데몬 비활성화
```

### 알림 태그 (Telegram/Discord/Slack)

세션 요약을 전송할 때 태그할 사용자를 설정할 수 있다:

```bash
# 태그 목록 설정
omc config-stop-callback telegram --enable --token <bot_token> --chat <chat_id> --tag-list "@alice,bob"
omc config-stop-callback discord --enable --webhook <url> --tag-list "@here,123456789012345678"
omc config-stop-callback slack --enable --webhook <url> --tag-list "<!here>,<@U1234567890>"
```

## 왜 oh-my-claudecode인가?

```mermaid
flowchart TD
    classDef old fill:#ffebee,stroke:#ef5350,color:#c62828
    classDef new fill:#e8f5e9,stroke:#66bb6a,color:#2e7d32
    classDef user fill:#e3f2fd,stroke:#42a5f5,color:#1565c0
    classDef result fill:#c8e6c9,stroke:#43a047,color:#1b5e20
    classDef outcome fill:#fff8e1,stroke:#ffb300,color:#ff6f00

    subgraph WithoutOMC["기존 방식"]
        W1[설계]:::old --> W2[코딩]:::old
        W2 --> W3[리뷰]:::old
        W3 --> W4[테스트]:::old
        W4 --> W5[혼자 다 함]:::old
    end

    subgraph WithOMC["oh-my-claudecode"]
        U[사용자]:::user --> O[자연어 요청]:::user
        O --> A1["Architect: 설계"]:::new
        O --> A2["Executor: 구현"]:::new
        O --> A3["Verifier: 검증"]:::new
        A1 --> R[결과]:::result
        A2 --> R
        A3 --> R
    end

    WithoutOMC -->|비효율| X[시간 낭비]:::outcome
    WithOMC -->|효율| Y[생산성 극대화]:::result
```

| 구분 | 기존 방식 | oh-my-claudecode |
|------|----------|------------------|
| 설계 | 직접 구조 잡고 계획 | Architect 에이전트가 담당 |
| 코딩 | 직접 코드 작성 | Executor 에이전트가 구현 |
| 리뷰 + 테스트 | 직접 품질 확인 | Verifier 에이전트가 검증 |
| 실행 방식 | 순차 처리 | 병렬 실행 가능 |
| 합의 기반 | 개인 판단 | 다중 에이전트 합의 |

## 핵심 요약

- **oh-my-claudecode** 는 Claude Code를 위한 멀티 에이전트 오케스트레이션 플러그인이다
- **32개 전문 에이전트** 가 역할별로 나누어 설계, 구현, 검증을 처리한다
- **Team 모드** 가 정식 오케스트레이션 표면으로 `team-plan → team-prd → team-exec → team-verify → team-fix` 파이프라인으로 동작한다
- **omc-teams** 로 실제 Codex/Gemini CLI 프로세스를 tmux에서 실행할 수 있다
- **deep-interview → ralplan → autopilot** 워크플로우로 막연한 아이디어를 완성된 코드로 변환한다
- **제로 설정** 으로 자연어만으로 작업 지시가 가능하다
- **비용 최적화** 로 토큰 30-50% 절약 효과가 있다

## 결론

oh-my-claudecode는 바이브 코딩의 효율성을 극대화하는 도구다. 혼자서 설계, 코딩, 리뷰, 테스트를 모두 처리하는 대신, 32개 전문 에이전트가 역할별로 나누어 병렬로 작업한다. 모드를 외울 필요 없이 자연어로 원하는 것을 말하면 된다. 설치는 세 줄이면 충분하다. Claude Code를 쓰고 있다면 oh-my-claudecode로 "딸깍" 을 더 잘하는 방법을 경험해 보자.

```bash
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode
/omc-setup
```

더 자세한 사용법은 `/omc-help` 를 입력하면 확인할 수 있다.
