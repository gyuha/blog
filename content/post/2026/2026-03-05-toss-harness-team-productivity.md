---
title: "Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기"
date: 2026-03-05
draft: false
categories:
  - AI
tags:
  - LLM
  - Claude Code
  - Context Engineering
  - Harness
  - Marketplace
  - 조직 생산성
description: "토스페이먼츠의 'Harness' 개념을 통해 LLM 팀의 생산성 저점을 높이는 방법을 살펴봅니다. 컨텍스트 엔지니어링의 중요성과 실행 가능한 SSOT, 그리고 세 가지 지식 계층 아키텍처를 소개합니다."
---

당신의 팀은 같은 LLM을 쓰고 있나요?

"현재 많은 개발팀이 LLM을 도입하고 있지만, 냉정하게 들여다보면 그것은 '각자도생'에 가깝습니다."
<!--more-->

같은 모델, 같은 IDE를 쓰는데도 결과물의 차이는 극심합니다. 어떤 엔지니어는 **컨텍스트 엔지니어링**에 대한 높은 이해도로 LLM에게 정확한 역할을 부여해 10분 만에 복잡한 리팩토링을 끝냅니다. 반면, 어떤 엔지니어는 단순한 질문과 답변을 반복하며 할루시네이션과 씨름하느라 1시간을 허비하죠.

```mermaid
flowchart LR
    subgraph A["엔지니어 A - 10분 완성"]
        A1[컨텍스트 세팅]
        A2[레포 코딩 가이드라인]
        A3[Lint 규칙]
        A4[기존 코드 패턴]
        A1 --> A2
        A1 --> A3
        A1 --> A4
        A2 --> A5[팀 컨벤션에 맞는 결과]
        A3 --> A5
        A4 --> A5
    end

    subgraph B["엔지니어 B - 1시간 소요"]
        B1[단순 질문]
        B2[일반적 스타일 코드]
        B3[수정 루프 반복]
        B1 --> B2
        B2 --> B3
        B3 --> B4[결과물 수정 및 반복]
    end

    style A fill:#e3f2fd
    style B fill:#ffebee
```

A 엔지니어는 작업 전에 컨텍스트를 먼저 세팅합니다. 레포의 코딩 가이드라인, lint 규칙, 기존 코드 패턴을 LLM에게 주입한 뒤 작업을 시킵니다. 결과물은 처음부터 팀 컨벤션에 맞고, 10분이면 머지 가능한 상태가 됩니다.

B 엔지니어는 "이 함수 리팩토링해줘"로 시작합니다. AI는 일반적인 스타일로 코드를 뱉고, 이후 1시간 동안 "우리 팀은 이렇게 안 해"를 반복하며 수정 루프에 갇힙니다.

<!--more-->

## The Frictionless Harness: 맥락이 끊기지 않는 경험

Open Interpreter, OpenCode 등 훌륭한 시도들은 많았습니다. 하지만 개발자에게 '새로운 도구를 쓴다'는 감각은 여전히 미세한 마찰(Friction)을 일으킵니다. 브라우저로 나가서 챗봇에게 코드를 붙여넣는 순간, 문맥 교환(Context Switching) 비용이 발생하기 때문이죠.

Claude Code가 제공하는 TUI(Terminal User Interface) 환경의 가치는 바로 이 지점에 있다고 생각합니다. 호불호를 떠나, 개발자가 가장 많은 시간을 보내는 터미널 안에서 자연어와 코드가 끊김 없이 섞이는 경험(Seamless Integration)을 제공한다는 점입니다.

```mermaid
flowchart LR
    subgraph Traditional["전통적인 방식"]
        T1[IDE에서 코드 작성]
        T2[브라우저로 이동]
        T3[코드 복사 및 붙여넣기]
        T4[챗봇 대화]
        T5[결과를 다시 IDE에 붙여넣기]
        T1 --> T2
        T2 --> T3
        T3 --> T4
        T4 --> T5
        T5 --> T2
    end

    subgraph Frictionless["Frictionless Harness"]
        F1[터미널 내 개발 환경]
        F2[자연어와 코드의<br/>Seamless Integration]
        F3[문맥 전환 없는 경험]
        F1 --> F2
        F2 --> F3
    end

    style Traditional fill:#fff3e0
    style Frictionless fill:#e8f5e9
```

## Executable SSOT: 문서는 죽고, 코드는 산다

"우리는 항상 SSOT(Single Source of Truth)를 갈구하지만, 위키(Wiki)나 노션 문서는 작성되는 순간부터 낡은 정보가 됩니다. 사람이 읽기 위한 문서이기 때문입니다."

하지만 Claude Code의 플러그인 형태로 정의된 지식은 성격이 다릅니다. 이들은 '실행 가능한 SSOT(Executable SSOT)'가 될 수 있는 잠재력을 가지고 있습니다.

*   **사람이 읽으면:** 업무 가이드라인이자 매뉴얼이 되고,
*   **LLM이 읽으면:** 정확한 지시사항이 담긴 시스템 프롬프트가 됩니다.

```mermaid
flowchart TD
    subgraph SSOT["SSOT (Single Source of Truth)"]
        K[조직의 지식]
    end

    K --> H1[사람이 읽을 때]
    K --> H2[LLM이 읽을 때]

    H1 --> G[업무 가이드라인 & 매뉴얼]
    H2 --> P[시스템 프롬프트 & 지시사항]

    style K fill:#e1f5fe
    style G fill:#fff3e0
    style P fill:#e8f5e9
```

## Raising the Floor: 범용 도구를 넘어, 도메인 최적화 하네스로

"팀 내에는 코딩 실력과 무관하게 'LLM 활용 노하우'의 편차가 존재합니다. 우리는 이 문제를 해결하기 위해 '팀 생산성의 저점(Floor)'을 높여야 합니다."

```mermaid
graph TD
    subgraph Before["Before: 생산성 편차"]
        B1[고성능자]
        B2[저성능자]
        B3[LLM 노하우 편차]
        B1 --> B3
        B2 --> B3
    end

    subgraph After["After: Raising the Floor"]
        A1[공통 워크플로우]
        A2[하네스 설치]
        A3[최적화된 컨텍스트]
        A4[생산성 저점 향상]
        A1 --> A2
        A2 --> A3
        A3 --> A4
    end

    style Before fill:#ffebee
    style After fill:#e8f5e9
```

## Software 1.0의 시선: 익숙한 성공 방정식의 재현

"우리는 이미 Software 1.0 시대에 '플랫폼 엔지니어링'을 통해 팀의 생산성을 높여왔습니다."

인증(Auth), 로깅(Logging), 결제 연동 등 반복되는 기능을 사내 공통 라이브러리나 모듈로 만들었고, 이를 통해 팀원들이 '바퀴를 다시 발명하는(Reinvent the wheel)' 시간을 없앴습니다. 덕분에 우리는 비즈니스 로직에만 집중하며 빠르게 제품을 출시할 수 있었습니다.

```mermaid
flowchart LR
    subgraph Platform["플랫폼 엔지니어링"]
        P1[인증]
        P2[로깅]
        P3[결제 연동]
        P1 --> P4[공통 라이브러리]
        P2 --> P4
        P3 --> P4
    end

    P4 --> T[팀원들]
    T --> B[비즈니스 로직 집중]
    B --> R[빠른 제품 출시]

    style Platform fill:#e1f5fe
    style B fill:#fff3e0
```

## Why Marketplace? (Beyond RAG & Server)

"혹자는 '그냥 위키 문서를 RAG(Retrieval-Augmented Generation)로 구축해서 연동하면 되지 않나?'라고 반문할 수 있습니다."

### 1) 예측 가능성(Predictability)
RAG 시스템을 구축해 본 분들은 공감하실 겁니다. 가시성이 떨어집니다. 하이브리드 서치, 리랭커 점수 등 내부 로직에 의해 어떤 컨텍스트가 주입될지 예측하기 어렵습니다.

### 2) 빠른 실험과 Dev-Prod Parity (환경 일치)
서버에 배포하지 않고도 워크플로우를 검증할 수 있습니다. 로컬 TUI 환경에서 플러그인을 수정하고, 즉시 Claude와 대화하며 피드백 루프를 돌릴 수 있습니다.

```mermaid
flowchart TD
    subgraph RAG["RAG 접근법"]
        R1[위키 문서]
        R2[하이브리드 서치]
        R3[리랭커 점수]
        R4[컨텍스트 주입 불확실성]
        R1 --> R2
        R2 --> R3
        R3 --> R4
    end

    subgraph Marketplace["Marketplace 접근법"]
        M1[플러그인 코드]
        M2[명확한 정의]
        M3[로컬 TUI 테스트]
        M4[즉시 피드백 루프]
        M1 --> M2
        M2 --> M3
        M3 --> M4
    end

    style RAG fill:#ffebee
    style Marketplace fill:#e8f5e9
```

## Marketplace 1.0: 워크플로우 배포 플랫폼

이 글에서 가장 하고 싶은 이야기는 여기에 있습니다. 저는 현재의 플러그인과 마켓플레이스가 단순한 기능 확장이 아니라고 봅니다. 이것은 "조직의 일하는 방식(Workflow)을 배포하는 플랫폼의 1.0 버전"이 될 수 있습니다.

### Scenario 1: 브랜치 가드
1. claude가 git commit을 시도합니다.
2. 플러그인에 등록된 Hook이 감지하고 개입합니다.
3. "잠시만요, 현재 main 브랜치입니다. 우리 팀 컨벤션에 따라 feature/ 브랜치를 생성하고 작성하겠습니다."

```mermaid
sequenceDiagram
    participant D as 개발자
    participant C as Claude
    participant H as Hook Plugin
    participant G as Git

    rect rgb(225, 245, 254)
        note right of H: Hook Plugin
    end

    D->>C: 커밋 요청
    C->>G: git commit 시도
    H->>H: 현재 브랜치 감지
    H->>C: main 브랜치임을 알림
    C->>D: feature/ 브랜치 생성 제안
    D->>C: 승인
    C->>G: feature/ 브랜치 생성 및 커밋
```

### Scenario 2: 피처 개발 자동화
1. `/new-feature` 입력 → Claude가 대화를 통해 구현할 기능의 맥락을 수집
2. Jira 이슈 발급, 브랜치 생성, 구현 계획 작성 → 엔지니어가 계획을 검토/승인
3. 구현 진행 → PR 생성 및 리뷰 요청

```mermaid
flowchart LR
    I[/new-feature 입력/]
    C1[맥락 수집]
    P1[Jira 이슈 발급]
    P2[브랜치 생성]
    P3[구현 계획 작성]
    R[엔지니어 검토 및 승인]
    I1[구현 진행]
    PR[PR 생성 및 리뷰 요청]

    I --> C1
    C1 --> P1
    C1 --> P2
    C1 --> P3
    P1 --> R
    P2 --> R
    P3 --> R
    R --> I1
    I1 --> PR

    style I fill:#e1f5fe
    style R fill:#fff3e0
    style PR fill:#e8f5e9
```

## Layered Architecture: 관심사별 컨텍스트 계층화

신입사원에게 회사 전체 문서를 한꺼번에 던져주지 않듯, LLM에게도 현재 작업에 필요한 지식만 명확하게 주입해야 합니다. 저는 지식을 세 가지 계층으로 분리하여 관리하는 것이 효과적일 거라 생각합니다.

*   **Global Layer:** 전사 공통 규정 (보안 정책, 기본 코딩 스타일)
*   **Domain Layer:** 팀/비즈니스별 지식 (결제, 정산, 회원 등 특정 도메인 로직)
*   **Local Layer:** 특정 레포지토리의 구현 디테일 및 프로젝트 특화 규칙

```mermaid
flowchart TD
    subgraph Global["Global Layer"]
        G1[보안 정책]
        G2[기본 코딩 스타일]
        G3[전사 공통 규정]
    end

    subgraph Domain["Domain Layer"]
        D1[결제 도메인]
        D2[정산 도메인]
        D3[회원 도메인]
    end

    subgraph Local["Local Layer"]
        L1[레포지토리 구현 디테일]
        L2[프로젝트 특화 규칙]
    end

    Global --> C[LLM Context]
    Domain --> C
    Local --> C

    style Global fill:#e3f2fd
    style Domain fill:#fff3e0
    style Local fill:#e8f5e9
```

## Outlook: The Data Flywheel Hypothesis

"이 시스템이 정착된 이후, 우리는 조금 더 먼 미래를 그려볼 수 있습니다. 이것은 아직 가설(Hypothesis)의 영역이지만, AI 엔지니어링이 나아가야 할 필연적인 방향이기도 합니다."

## Conclusion: 우리만의 최적화된 하네스 구축을 향해

"결국 이 모든 흐름이 향하는 곳은 '우리 조직에 최적화된 하네스(Harness)의 구축'이라고 생각합니다."

도구는 준비되었습니다. 이제 여러분의 팀은 무엇을 '설치'하시겠습니까?

```mermaid
flowchart LR
    T[팀] --> W[워크플로우 설치]
    H[하네스 구축]
    P[생산성 저점 향상]
    W --> H
    H --> P

    style T fill:#e1f5fe
    style H fill:#fff3e0
    style P fill:#e8f5e9
```

---

*원문: [Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기](https://toss.tech/article/harness-for-team-productivity)*
