---
title: "Claude Code 왜 나만 느릴까: 10단계 성장 로드맵 정리"
date: 2026-03-10T21:17:11+09:00
draft: false
categories:
  - AI
  - Development
tags:
  - Claude Code
  - Workflow
  - MCP
  - Context Engineering
  - Token Optimization
description: "Maker Evan 영상 내용을 바탕으로 Claude Code를 처음부터 빠르게 익히기 위한 10단계 성장 순서와 컨텍스트·토큰 관리 포인트를 정리합니다."
---

Claude Code를 처음 쓸 때 많은 사람이 비슷한 구간에서 막힙니다. 플러그인과 MCP를 잔뜩 붙였는데도 이상하게 느리고, 다른 사람 데모처럼 매끄럽게 굴러가지 않고, 결국 "내가 뭘 잘못하고 있지?"라는 감각만 남습니다. 이 영상의 핵심 주장은 단순합니다. **문제는 AI의 성능보다 학습 순서에 있고, 순서를 잘못 잡으면 도구를 많이 붙일수록 더 느려진다** 는 점입니다.
<!--more-->

발표자는 Claude Code를 "치매에 걸린 아인슈타인"에 비유합니다. 코딩 능력은 뛰어나지만 세션이 바뀌거나 컨텍스트가 압축되면 맥락을 잊기 때문에, 사용자는 단순히 기능을 배우는 것이 아니라 이 도구의 기억 구조와 비용 구조를 같이 배워야 합니다. 그래서 이 글은 영상의 10단계 로드맵을 그대로 따라가되, 왜 그 순서가 중요한지와 각 단계가 다음 단계의 전제가 되는 이유를 중심으로 정리합니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=20)

영상이 제시하는 10단계는 다음 순서입니다. 1) 플러그인 없이 기본 상태로 시작, 2) 튜토리얼만 보지 말고 작은 실전 프로젝트 만들기, 3) 반복 작업을 스킬로 만들기, 4) 필요한 MCP 연결하기, 5) MCP 대신 스킬/CLI를 쓰며 비용 최적화하기, 6) `CLAUDE.md` 중심의 컨텍스트 엔지니어링, 7) 파일 범위·모델 선택·컴팩션 회피를 포함한 토큰 절약, 8) 내 소비 패턴 파악, 9) Max 플랜이나 큰 작업으로 한계 체험, 10) 마지막에 하니스 도입입니다. 아래 본문은 이 10단계를 묶어서 설명하지만, 순서는 영상의 흐름을 그대로 유지합니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=872)


## Sources

- https://www.youtube.com/watch?v=d-iNXwtwdFU

## 1) 왜 처음부터 플러그인과 MCP를 붙이면 더 느려지는가

영상은 Claude Code 커뮤니티에서 가장 흔한 실패 패턴으로 "처음부터 플러그인, MCP, 프레임워크를 한꺼번에 얹고 시작하는 것"을 지적합니다. 표면적으로는 세팅이 화려해 보이지만, 실제로는 어떤 도구가 무슨 역할을 하는지 이해하지 못한 채 복잡성만 높아집니다. 그 결과 이상한 동작이 생겨도 원인을 추적하지 못하고, 사용자는 이를 AI 자체의 한계로 오해하게 됩니다. 발표자가 반복해서 강조하는 것은 도구 부족이 아니라 **이해 없이 도구를 쌓은 상태**가 문제라는 점입니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=33)

이 대목에서 중요한 건 Claude Code의 근본 전제입니다. 발표자는 이 도구가 복잡한 코딩과 디버깅은 잘하지만 기억을 못 한다고 설명합니다. 새 세션이 열리면 어제의 지시를 잊고, 긴 대화 중에도 컨텍스트가 흔들리기 시작합니다. 즉 사용자는 단순히 프롬프트를 잘 쓰는 사람이 아니라, 이 도구가 무엇을 기억하고 무엇을 잊는지 관리하는 운영자가 되어야 합니다. 그래서 첫 단계는 기능 추가가 아니라 **기본 상태의 동작 원리를 관찰하는 것**이 됩니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=98)

```mermaid
flowchart TD
    classDef bad fill:#ffc8c4,stroke:#c96f66,color:#333
    classDef core fill:#c5dcef,stroke:#5b8db8,color:#333
    classDef result fill:#fde8c0,stroke:#c89a3d,color:#333
    classDef good fill:#c0ecd3,stroke:#58a36f,color:#333

    A["처음부터 플러그인/MCP 대량 추가"]:::bad --> B["원인 모르는 이상 동작"]:::bad
    B --> C["AI가 원래 별론가? 라고 오해"]:::result

    D["기본 상태로 먼저 사용"]:::core --> E["파일 읽는 순서/오류 복구/한계 관찰"]:::core
    E --> F["어떤 도구가 왜 필요한지 이해"]:::good
```

## 2) 1단계부터 5단계까지: 실전 프로젝트, 스킬, MCP를 배우는 올바른 순서

로드맵의 앞 절반은 "학습 기반 만들기"에 가깝습니다. 1단계는 플러그인 없이 기본 상태로 시작하는 것이고, 2단계는 튜토리얼만 소비하지 말고 실제로 작은 프로젝트를 하나 만들어 보는 것입니다. 발표자는 Claude Code를 이론으로 익히는 도구가 아니라 몸으로 익히는 도구라고 설명합니다. 자전거를 책으로만 배울 수 없듯이, 50% 완성도의 작은 앱을 직접 만들면서 Claude와 부딪혀 보는 편이 훨씬 빨리 는다고 말합니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=186)

3단계는 반복 작업을 스킬로 추출하는 것입니다. 여기서 스킬은 단순한 편의 기능이 아니라, 반복되는 절차를 매번 긴 프롬프트로 설명하지 않게 해 주는 압축 장치입니다. 배포 절차, 코드 리뷰 기준, 커밋 메시지 형식처럼 두 번 이상 반복한 작업이 있다면 스킬로 만들어 두라는 조언이 나옵니다. 영상은 특히 스킬이 호출될 때만 로드되므로, 많이 설치해도 기본 비용이 거의 없다는 점을 장점으로 듭니다. 즉 학습의 세 번째 단계는 Claude에게 더 많은 권한을 주는 것이 아니라, **반복되는 인간 설명을 구조화된 재사용 자산으로 바꾸는 것**입니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=289)

4단계는 그 다음에야 MCP를 붙이는 것입니다. 발표자는 MCP를 Claude Code에 "팔다리를 붙여 주는 것"이라고 설명합니다. GitHub 작업, 브라우저 조작, 데이터베이스 질의처럼 도구 실행 능력을 넓히는 단계죠. 하지만 5단계가 바로 이어집니다. MCP는 강력하지만 세션 시작 시 기능 목록을 미리 로드하기 때문에 토큰 비용을 선불로 태웁니다. 그래서 자주 쓰지 않는 기능은 스킬이나 CLI로 대체하고, 안 쓰는 MCP는 꺼 두라는 것이 영상의 결론입니다. 커뮤니티 측정치로 MCP 서버 다섯 개를 켜면 전체 컨텍스트 용량의 41%가 사라질 수 있다는 언급도 나오는데, 이 수치는 발표자가 커뮤니티 수치로 소개한 것이므로 공식 스펙으로 받아들이기보다는 "초기 로드 비용이 크다"는 방향성으로 이해하는 편이 안전합니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=386)

```mermaid
flowchart TD
    classDef learn fill:#c5dcef,stroke:#5b8db8,color:#333
    classDef build fill:#c0ecd3,stroke:#58a36f,color:#333
    classDef tool fill:#fde8c0,stroke:#c89a3d,color:#333
    classDef warn fill:#ffc8c4,stroke:#c96f66,color:#333

    A["1. 기본 상태로 시작"]:::learn --> B["2. 작은 실전 프로젝트 제작"]:::build
    B --> C["3. 반복 작업을 스킬로 저장"]:::tool
    C --> D["4. 필요한 MCP 연결"]:::tool
    D --> E["5. 안 쓰는 MCP 제거<br>스킬/CLI로 대체"]:::warn
```

## 3) 6단계와 7단계: 컨텍스트 엔지니어링과 토큰 절약이 진짜 실력 차이를 만든다

영상에서 발표자가 가장 중요하다고 강조하는 부분은 6단계인 컨텍스트 엔지니어링입니다. 여기서 핵심은 `CLAUDE.md`를 장기 메모리처럼 다루는 것입니다. 프로젝트 구조, 코딩 규칙, 자주 쓰는 명령, 절대 하면 안 되는 것들을 이 파일에 짧고 핵심적으로 적어 두면 Claude가 세션 시작 시 자동으로 읽습니다. 다만 영상은 `/init`로 생성된 파일을 맹신하지 말고, 실제로 Claude가 잘 지키지 못하는 부분을 관찰해서 `CLAUDE.md`에 보강해야 효과가 좋다고 말합니다. 즉 이 파일은 초기 세팅 문서가 아니라 **실패를 관찰한 뒤 보정하는 운영 문서**에 더 가깝습니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=445)

바로 이어서 설명되는 개념이 컨텍스트 컴팩션입니다. 영상 흐름상 이 부분은 6단계의 연장선에서 설명되지만, 실제 운영 감각으로는 7단계 토큰 절약 전략을 이해하기 위한 핵심 전제이기도 합니다. 발표자는 Claude Code가 대화가 길어지면 지금까지의 대화를 강제로 요약해 버리고, 그 이후부터 지시 위반, 이미 고친 버그 재등장, 읽던 파일을 잊고 다시 읽기 같은 문제가 생긴다고 설명합니다. 이 때문에 컴팩션은 가능한 한 피하거나 최소화해야 합니다. 제안된 방법은 세 가지입니다. 첫째, `CLAUDE.md`를 짧고 핵심적으로 유지해 컴팩션 후에도 다시 읽혀 장기 메모리 역할을 하게 하는 것, 둘째, 관련 없는 작업을 시작할 때 `/clear`로 세션을 비우는 것, 셋째, 한 세션에 너무 많은 일을 몰지 않고 작업을 잘게 쪼개는 것입니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=520)

7단계는 이 컨텍스트 문제를 비용 절감까지 연결합니다. 필요 없는 파일은 읽히지 말고, 복잡한 설계에는 더 강한 모델을, 단순 수정에는 더 빠르고 저렴한 모델을 고르며, MCP 대신 CLI와 스킬을 우선 사용하라는 것입니다. 즉 토큰 절약은 단순히 비용 아끼기가 아니라, **컴팩션을 늦추고 기억 오염을 줄이는 컨텍스트 설계 문제**로 봐야 합니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=566)

```mermaid
flowchart TD
    classDef memory fill:#c5dcef,stroke:#5b8db8,color:#333
    classDef compact fill:#ffc8c4,stroke:#c96f66,color:#333
    classDef protect fill:#c0ecd3,stroke:#58a36f,color:#333
    classDef rule fill:#fde8c0,stroke:#c89a3d,color:#333

    A["세션 시작"]:::memory --> B["짧고 핵심적인 CLAUDE.md 자동 로드"]:::memory
    B --> C["대화가 길어짐"]:::rule
    C --> D["컨텍스트 컴팩션 발생"]:::compact
    D --> E["지시 위반/파일 재탐색/버그 재등장"]:::compact

    B --> F["/clear 사용"]:::protect
    B --> G["작업 단위 쪼개기"]:::protect
    B --> H["필요한 파일만 읽히기"]:::protect
    B --> I["모델/MCP 선택 최적화"]:::protect
```

## 4) 8단계부터 10단계까지: 소비 패턴 파악, Max 체험, Harness 도입

후반부 로드맵은 "도구를 더 붙이는 단계"가 아니라, 자신만의 운영 체계를 검증하는 단계입니다. 8단계에서는 복잡한 작업 하나를 실제로 처음부터 끝까지 수행해 보면서 자신의 토큰 소비 패턴을 파악하라고 말합니다. 얼마나 쓰는지 감이 없으면 요금제 선택도, 작업 분해 전략도 전부 감으로 하게 되기 때문입니다. 발표자는 이를 식비 예산에 비유합니다. 먼저 내가 얼마나 쓰는지 알아야 줄일 수 있다는 것이죠. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=632)

9단계는 Claude Code Max 플랜을 쓸 수 있다면 한 번은 끝까지 밀어붙여 보라는 것입니다. 이 단계의 취지는 단순한 과금 유도가 아니라, 안전한 범위에서만 도구를 써 보면 실제 한계와 강점을 모른다는 점에 있습니다. 복잡한 프로젝트를 처음부터 끝까지 돌려 봐야 "Claude Code로 잘 되는 일"과 "내가 직접 해야 하는 일"의 경계가 생깁니다. 즉 비싼 플랜 체험의 목적은 더 많이 쓰는 것이 아니라, **위임 가능한 업무의 경계를 배우는 것**입니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=678)

10단계는 Harness 찾기입니다. 발표자는 Harness를 Claude가 세션마다 제멋대로 행동하지 않도록 잡아주는 구조라고 설명합니다. 여기서 핵심은 하니스를 첫 단계에 두지 않는 이유입니다. 기초가 없는 상태에서 오마이클로드코드나 슈퍼파워즈 같은 레이어를 먼저 얹으면, 왜 필요한지 모른 채 또 다른 복잡성만 추가하게 됩니다. 그래서 하니스는 맨 마지막입니다. 먼저 Claude Code 자체의 동작 원리, 메모리 구조, 토큰 흐름, 모델 선택 감각을 몸으로 익힌 뒤에야 하니스가 진짜 생산성 도구가 됩니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=769)

```mermaid
flowchart TD
    classDef measure fill:#c5dcef,stroke:#5b8db8,color:#333
    classDef test fill:#fde8c0,stroke:#c89a3d,color:#333
    classDef guard fill:#c0ecd3,stroke:#58a36f,color:#333

    A["8. 실제 작업으로 소비 패턴 측정"]:::measure --> B["9. Max 플랜/큰 작업으로 한계 체험"]:::test
    B --> C["무엇을 Claude에게 맡길지 경계 파악"]:::guard
    C --> D["10. 내 스타일에 맞는 Harness 도입"]:::guard
```

## 5) 실전 적용 포인트: 10단계를 운영 체크리스트로 다시 묶기

이 영상이 주는 가장 큰 통찰은 "고급 기능을 빨리 붙이는 것"이 성장 순서가 아니라는 점입니다. 먼저 기본 상태를 관찰하고, 작은 프로젝트로 부딪히고, 반복 작업을 스킬로 만들고, 그 다음에 MCP를 붙이며, 이후에는 `CLAUDE.md`, `/clear`, 모델 선택, 파일 범위 제한으로 컨텍스트를 관리하고, 마지막에야 큰 플랜과 하니스를 검토해야 합니다. 즉 성장 순서는 기능 목록이 아니라 **복잡성을 감당할 수 있는 운영 능력을 한 단계씩 쌓는 순서**입니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=835)

실무적으로 바로 옮기면 다음과 같은 체크리스트가 됩니다. 지금 막 시작했다면 1단계와 2단계에 집중하면서 기본 동작을 관찰하고, 반복 업무가 생기면 3단계로 스킬을 만들고, MCP는 4단계에서 최소한만 연결합니다. 그리고 5단계에서 꼭 한 번 더 걸러야 합니다. 안 쓰는 MCP는 끄고, 자주 쓰지 않는 기능은 스킬이나 CLI로 빼서 초기 컨텍스트 비용을 줄여야 합니다. 이후 이상 행동이나 비용 문제가 보이기 시작하면 6단계와 7단계로 넘어가 `CLAUDE.md`, `/clear`, 작업 분해, 모델 선택을 정리합니다. 마지막으로 실제 소비 패턴을 숫자로 확인한 뒤에만 Max 플랜이나 하니스 레이어를 올리는 것이 가장 안전한 경로입니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=872)

```mermaid
flowchart TD
    classDef stage fill:#c5dcef,stroke:#5b8db8,color:#333
    classDef opt fill:#fde8c0,stroke:#c89a3d,color:#333
    classDef mature fill:#c0ecd3,stroke:#58a36f,color:#333

    A["기본 동작 관찰"]:::stage --> B["작은 프로젝트 제작"]:::stage
    B --> C["반복 업무를 스킬화"]:::stage
    C --> D["필요 최소한의 MCP 연결"]:::opt
    D --> E["CLAUDE.md / clear / 파일 범위 / 모델 선택 최적화"]:::opt
    E --> F["소비 패턴 측정 후 Max/Harness 검토"]:::mature
```

## 핵심 요약

- Claude Code를 잘 못 쓰는 가장 흔한 이유는 기능 부족이 아니라, 기본 동작을 이해하기 전에 플러그인과 MCP를 과하게 얹는 순서 문제입니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=33)
- 초반에는 실전 프로젝트를 직접 만들고, 두 번 이상 반복한 작업을 스킬로 추출하는 것이 튜토리얼 소비보다 훨씬 빠른 학습 경로입니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=186)
- MCP는 강력하지만 초기 컨텍스트 비용이 크므로, 자주 안 쓰는 기능은 스킬이나 CLI로 대체하는 편이 좋습니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=386)
- `CLAUDE.md`, `/clear`, 작업 분해, 필요한 파일만 읽히기 같은 컨텍스트 엔지니어링이 실제 속도와 품질을 크게 좌우합니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=445)
- Max 플랜이나 Harness는 마지막 단계에서 검토해야 하며, 먼저 내 소비 패턴과 위임 경계를 이해한 뒤 도입하는 것이 안전합니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=678)

## 결론

이 영상이 말하는 "왜 나만 느리지?"의 답은 재능이나 모델 선택보다 먼저 순서에 있습니다. Claude Code를 잘 쓰는 사람은 더 많은 도구를 먼저 붙인 사람이 아니라, **기본 동작을 관찰하고, 반복을 구조화하고, 기억과 비용을 관리한 다음, 마지막에 확장 레이어를 올린 사람**입니다. [근거 영상](https://youtu.be/d-iNXwtwdFU?t=900)

<!--
Evidence notes
- claim: The main problem is learning order, not the AI itself | transcript/time marker: "AI탓이 아닙니다. 순서 문제예요" / ~0:20 | video url: https://youtu.be/d-iNXwtwdFU?t=20 | confidence: high
- claim: Overloading plugins, MCPs, and frameworks too early creates confusion without understanding | transcript/time marker: "처음부터 플러그인 깔고 MCP 다섯 개 연결" / ~0:33 | video url: https://youtu.be/d-iNXwtwdFU?t=33 | confidence: high
- claim: Claude Code is powerful but forgetful across sessions and even during long conversations | transcript/time marker: "치매에 걸린 아인슈타인" / ~1:38 | video url: https://youtu.be/d-iNXwtwdFU?t=98 | confidence: high
- claim: Learn by building a small real project rather than staying in tutorial mode | transcript/time marker: "완성도 50%짜리 앱을 만들면서 배우는게" / ~3:06 | video url: https://youtu.be/d-iNXwtwdFU?t=186 | confidence: high
- claim: Repeated tasks should become skills, which load only when invoked | transcript/time marker: "스킬의 또 다른 장점 토큰을 거의 안 먹어요" / ~4:49 | video url: https://youtu.be/d-iNXwtwdFU?t=289 | confidence: high
- claim: MCP acts like extra limbs but has startup token cost; five MCP servers can consume large context budget according to community measurement | transcript/time marker: "MCP 서버 다섯 개 켜 놓으면 전체 용량의 41%" / ~6:26 | video url: https://youtu.be/d-iNXwtwdFU?t=386 | confidence: medium
- claim: Context engineering with CLAUDE.md is the most important advanced step | transcript/time marker: "전체 10단계 중에서 제일 중요한 단계" / ~7:25 | video url: https://youtu.be/d-iNXwtwdFU?t=445 | confidence: high
- claim: Compaction causes instruction drift and should be minimized with short CLAUDE.md, /clear, and smaller tasks | transcript/time marker: "컴팩션 전에는 지시를 100% 따르던" / ~8:40 | video url: https://youtu.be/d-iNXwtwdFU?t=520 | confidence: high
- claim: Token saving comes from limiting files, choosing the right model, and preferring CLI/skills over MCP when possible | transcript/time marker: "필요 없는 파일은 주지 마세요" / ~9:26 | video url: https://youtu.be/d-iNXwtwdFU?t=566 | confidence: high
- claim: Track your own consumption pattern before choosing plans and use Max/Harness only after fundamentals | transcript/time marker: "내 소모량을 파악" / "하니스를 10단계에 배치" / ~10:32 | video url: https://youtu.be/d-iNXwtwdFU?t=632 | confidence: high
-->
