---
title: "Claude Code Skill Creator 업데이트 정리: 평가, 벤치마크, 트리거 튜닝으로 스킬을 더 강하게 만드는 법"
date: 2026-03-16T17:07:49+09:00
draft: false
categories:
  - AI
  - Development
tags:
  - Claude Code
  - Anthropic
  - Skills
  - Skill Creator
  - Evals
  - Benchmark
  - Workflow
description: "Nate Herk 영상과 Anthropic 공식 자료를 바탕으로 skill-creator 업데이트의 핵심인 평가, 벤치마크, 트리거 튜닝, 그리고 실전 반복 개선 흐름을 정리합니다."
---

Claude Code에서 스킬을 오래 쓰다 보면 금방 부딪히는 문제가 있습니다. 초안은 쉽게 만들 수 있는데, **언제 스킬을 계속 유지해야 하는지, 언제 수정해야 하는지, 언제 아예 버려야 하는지** 는 감으로 판단하기 어렵다는 점입니다.

<!--more-->

<br>이 영상이 중요한 이유는 바로 그 지점을 건드립니다. Anthropic의 `skill-creator` 업데이트를 통해 스킬을 "만드는 단계"에서 끝내지 않고, 테스트하고 비교하고 설명 문구까지 다듬는 **운영 루프** 로 바꾸는 흐름을 실제 데모로 보여 주기 때문입니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=0)

영상의 메시지는 단순히 "새 기능이 추가됐다"가 아닙니다. 스킬을 더 이상 정적인 프롬프트 파일로 보지 말고, 모델 변화와 함께 계속 측정하고 개선해야 하는 자산으로 보라는 이야기입니다. 특히 capability uplift 스킬과 encoded preference 스킬을 구분해서 봐야 한다는 설명, 첫 결과가 예뻐 보여도 데이터가 틀리면 다시 설계해야 한다는 데모, 그리고 자연어 설명만으로도 앞으로 더 많은 부분을 모델이 스스로 채울 것이라는 전망이 한 줄로 연결됩니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=95)


## Sources

- https://www.youtube.com/watch?v=RAZVk5NPNtE
- https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills
- https://github.com/anthropics/skills/tree/main/skills/skill-creator

## 1) 스킬을 먼저 두 종류로 나눠 봐야 하는 이유

영상은 스킬을 그냥 한 덩어리로 설명하지 않습니다. 먼저 **capability uplift** 와 **encoded preference** 로 나눠서 봐야 한다고 말합니다. capability uplift는 기본 모델이 혼자서는 일관되게 잘하지 못하는 작업을 더 잘하게 만드는 쪽입니다. 예를 들면 프런트엔드 디자인, 문서 생성, 복잡한 형식 작업처럼 "모델의 기본 능력을 끌어올리는" 프롬프트 성격이 강합니다. 반면 encoded preference는 모델이 이미 할 수 있는 일들을 **특정 순서와 특정 기준으로 실행하게 만드는 팀 워크플로우** 에 가깝습니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=95)

이 구분이 중요한 이유는 내구성이 다르기 때문입니다. capability uplift 스킬은 모델 자체가 좋아지면 언젠가 쓸모가 줄어들 수 있습니다. 영상에서도 차세대 모델이 기본 상태만으로 더 잘해 버리면 프런트엔드 스킬 같은 것은 은퇴시켜야 할 수도 있다고 설명합니다. 반대로 encoded preference는 특정 팀이나 특정 사람의 작업 순서, 판단 기준, 병렬 분석 흐름을 담고 있기 때문에 모델이 좋아져도 쉽게 사라지지 않습니다. 즉 "무엇을 더 잘하게 만들려는가" 와 "어떤 방식으로 일하게 만들려는가" 를 분리해서 봐야 스킬 수명과 유지 전략이 보입니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=145)

```mermaid
flowchart TD
  A[Capability Uplift] --> B[기본 모델이 약한 작업 보강]
  B --> C[예: 디자인 품질<br>문서 형식화]
  C --> D[모델 기본 성능이 올라가면<br>중복될 가능성]

  classDef kind fill:#c5dcef,stroke:#6b9ac4,color:#333
  classDef work fill:#fde8c0,stroke:#d9a441,color:#333
  classDef result fill:#ffc8c4,stroke:#d47a75,color:#333
  class A kind
  class B,C work
  class D result
```

```mermaid
flowchart TD
  A[Encoded Preference] --> B[이미 가능한 작업을<br>특정 순서로 강제]
  B --> C[예: 조사 -> 병렬 분석 -> 점수화 -> 산출물 생성]
  C --> D[팀/개인 워크플로라서<br>상대적으로 오래 유지]

  classDef kind fill:#c0ecd3,stroke:#67a97c,color:#333
  classDef work fill:#fde8c0,stroke:#d9a441,color:#333
  classDef result fill:#c5dcef,stroke:#6b9ac4,color:#333
  class A kind
  class B,C work
  class D result
```

영상 속 `idea mining` 예시가 바로 encoded preference 쪽에 가깝습니다. 댓글, 니치 영상, X와 웹 트렌드를 보고, 두 개의 에이전트를 병렬로 돌리고, 결과를 점수화해 아이디어로 변환하는 흐름은 모델이 원래 못 하는 능력을 추가한다기보다 **한 번 검증된 작업 순서를 반복 가능하게 묶는 것** 에 더 가깝기 때문입니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=120)

## 2) 이번 skill-creator 업데이트가 바꾼 것은 "생성"이 아니라 "운영"이다

영상에서 가장 중요한 변화는 `skill-creator` 가 이제 초안 생성 도구에 머물지 않는다는 점입니다. 발표자는 이 스킬이 새 스킬 생성, 기존 스킬 개선, 성능 측정, 설명 최적화까지 담당한다고 설명합니다. 즉 예전에는 "스킬을 써 봤더니 괜찮은 것 같다" 수준이었다면, 이제는 **평가 세트로 검증하고, 스킬 유무를 비교하고, 잘못 발동되는 설명까지 손보는 운영 도구** 로 바뀐 셈입니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=230)

여기서 eval의 역할은 두 가지입니다. 첫째는 **회귀 감지** 입니다. 모델이 바뀌거나 주변 환경이 바뀌었을 때 기존 스킬이 예전만큼 잘 동작하지 않는지 빨리 알아차리는 용도입니다. 둘째는 반대 방향의 감지입니다. 모델이 너무 좋아져서 스킬 없이도 더 잘하는 순간이 오면, 그 스킬은 더 이상 필수가 아닐 수 있습니다. 영상은 이 점을 꽤 현실적으로 설명합니다. 스킬은 무조건 늘려야 하는 자산이 아니라, 평가를 돌려 봤을 때 기본 모델이 더 좋다면 정리하거나 아카이브할 수도 있는 자산이라는 뜻입니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=300)

Anthropic 공식 블로그도 이 방향을 뒷받침합니다. 2026년 3월 공개된 개선 사항은 skill-creator를 스킬 생성 도구에 그치지 않고, 테스트와 측정, 벤치마크, 트리거 조정까지 포함한 반복 개선 흐름으로 확장하는 데 초점을 둡니다. 즉 영상의 설명이 단순 데모 멘트가 아니라, 실제 공식 기능 방향과 맞닿아 있다는 뜻입니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=330)

```mermaid
flowchart TD
  A[스킬 초안 생성] --> B[테스트 프롬프트 준비]
  B --> C[eval 실행]
  C --> D[with skill / without skill 비교]
  D --> E[pass rate / time / token 확인]
  E --> F[description 트리거 튜닝]
  F --> G[개선 후 재측정]
  G --> H[유지 / 수정 / 은퇴 판단]

  classDef draft fill:#c5dcef,stroke:#6b9ac4,color:#333
  classDef test fill:#fde8c0,stroke:#d9a441,color:#333
  classDef refine fill:#c0ecd3,stroke:#67a97c,color:#333
  classDef decision fill:#e0c8ef,stroke:#9b77b0,color:#333
  class A draft
  class B,C,D,E test
  class F,G refine
  class H decision
```

trigger tuning도 실무적으로 꽤 중요합니다. 스킬이 나쁘지 않아도 `description` 이 모호하면 엉뚱한 요청에서 발동되거나, 반대로 꼭 써야 할 순간에 빠질 수 있습니다. 영상은 스킬이 많아질수록 false trigger와 misfire가 생긴다고 설명하고, 공식 자료 역시 실제 사용자 표현에 가까운 설명 문구 최적화가 발동 정확도에 큰 영향을 준다고 말합니다. 결국 좋은 스킬 운영은 본문 절차만 잘 쓰는 것으로 끝나지 않고, **언제 호출되어야 하는지까지 설계해야 완성** 됩니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=390)

## 3) 라이브 데모가 보여 준 진짜 포인트는 "원샷 생성"이 아니라 반복 개선이다

후반부 라이브 데모는 이 업데이트의 성격을 가장 잘 보여 줍니다. 발표자는 `YouTube weekly roundup` 이라는 새 스킬을 거의 원샷에 가깝게 요청합니다. 지난 7일간 업로드한 영상을 분석하고, 댓글·조회수·참여도·강점·약점·기회·위협을 포함한 PDF 보고서를 만들어 달라는 정도만 던졌는데, 에이전트는 먼저 기간과 리포트 구성, PDF 스타일 같은 빠진 조건을 질문으로 메웁니다. 여기서 이미 중요한 변화가 드러납니다. 스킬 생성이 단순 복붙이 아니라, **애매한 요구를 질문으로 구조화하는 설계 단계** 를 앞에 두고 있다는 점입니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=525)

이후 생성된 산출물도 `SKILL.md` 하나로 끝나지 않습니다. 데모를 보면 스킬 본문이 어떤 스크립트를 호출해야 하는지 가리키고, 기존 프로젝트 안에 있던 YouTube 데이터 수집 스크립트까지 재사용합니다. 즉 skill-creator가 잘하는 것은 "빈 종이에 마법처럼 답을 쓰는 것" 보다, **이미 있는 자산과 새 지침을 연결해 하나의 실행 경로로 정리하는 것** 에 가깝습니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=780)

```mermaid
flowchart TD
  A[거친 요청 입력] --> B[누락 조건 질문]
  B --> C[계획 생성]
  C --> D[SKILL.md 작성]
  D --> E[기존 스크립트 재사용 또는 연결]
  E --> F[테스트와 eval 실행]
  F --> G[실제 스킬 실행]
  G --> H[PDF 보고서 출력]

  classDef input fill:#c5dcef,stroke:#6b9ac4,color:#333
  classDef plan fill:#fde8c0,stroke:#d9a441,color:#333
  classDef build fill:#c0ecd3,stroke:#67a97c,color:#333
  classDef output fill:#e0c8ef,stroke:#9b77b0,color:#333
  class A input
  class B,C plan
  class D,E,F,G build
  class H output
```

그리고 이 데모는 "한 번에 끝났다"가 아니라, 첫 결과를 보고 다시 피드백을 넣는 장면까지 포함하기 때문에 더 의미가 있습니다. 발표자도 처음 PDF는 디자인은 괜찮았지만 데이터가 틀리고 비어 있는 칸이 많다고 솔직하게 지적합니다. 즉 skill-creator가 생겼다고 해서 처음부터 완벽한 스킬이 나오는 것이 아니라, **출력의 보기 좋은 정도와 데이터의 실제 정확도를 분리해서 평가해야 한다** 는 점을 데모 자체가 보여 줍니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=645)

## 4) 첫 결과가 틀렸던 이유가 오히려 더 중요한 교훈이다

첫 번째 PDF에서 드러난 문제는 보고서 형식이 아니라 연구 깊이였습니다. 레이아웃은 그럴듯했지만, 실제 통계가 맞지 않았고 SWOT 분석이나 경쟁 채널 맥락도 비어 있었습니다. 그래서 발표자는 두 번째 요청에서 "디자인은 좋지만 데이터가 틀렸다"고 짚은 뒤, 채널 데이터 수집 방식, 댓글 분석, 경쟁 영상 탐색, AI 트렌드 조사까지 더 깊게 보라고 피드백합니다. 이 장면이 중요한 이유는 평가 기준이 단순히 보기 좋은 산출물인지가 아니라, **실제 의사결정에 쓸 수 있을 만큼 근거가 채워졌는지** 로 이동하기 때문입니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=690)

두 번째 실행에서는 결과가 달라집니다. 영상은 더 정확해진 조회수·좋아요·댓글 수치, 영상별 성과, SWOT 분석, 상위 댓글과 시청자 신호, 경쟁 채널 문맥, 이번 주 AI 트렌드까지 채워진 PDF를 보여 줍니다. 여기서 얻을 수 있는 가장 실용적인 교훈은 명확합니다. skill-creator의 진짜 가치는 스킬을 대신 만들어 주는 것보다, **부족한 성공 기준을 피드백으로 드러내고 그 기준을 다시 스킬에 주입해 반복 개선하게 만드는 것** 에 있습니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=870)

```mermaid
flowchart TD
  A[1차 결과: 보기 좋은 PDF] --> B[문제 발견: 데이터 부정확 / 빈 섹션]
  B --> C[피드백: 댓글 분석<br>경쟁 맥락<br>트렌드 조사 강화]
  C --> D[재실행]
  D --> E[2차 결과: 실제 데이터와 인사이트 강화]

  classDef weak fill:#ffc8c4,stroke:#d47a75,color:#333
  classDef review fill:#fde8c0,stroke:#d9a441,color:#333
  classDef strong fill:#c0ecd3,stroke:#67a97c,color:#333
  class A,B weak
  class C,D review
  class E strong
```

이 지점은 앞서 나온 capability uplift와 encoded preference 구분과도 연결됩니다. 리포트 제작 스킬이 단순히 "PDF를 예쁘게 만드는 능력" 에 머물면 capability uplift에 가깝게 남을 수 있습니다. 하지만 어떤 데이터를 모으고, 어떤 비교를 해야 하며, 어떤 보고 순서를 따라야 하는지까지 고정되면 encoded preference로 진화합니다. 즉 오래 살아남는 스킬은 보통 **표현 방식보다 판단 순서와 검증 기준을 더 많이 담고 있는 스킬** 입니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=145)

## 실전 적용 포인트

이 영상을 실제 Claude Code 운영에 옮기면 적용 포인트는 꽤 선명합니다. 첫째, 스킬을 만들기 전에 "이 스킬은 기본 모델 능력을 보강하는가, 아니면 우리 팀 절차를 고정하는가" 를 먼저 분류해야 합니다. 이 분류가 있어야 benchmark 결과를 해석할 수 있습니다. capability uplift라면 with-skill과 without-skill 비교에서 기본 모델이 더 좋아지는 순간 은퇴 후보가 되고, encoded preference라면 일관성·재현성·팀 적합성을 더 중요한 지표로 봐야 합니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=300)

둘째, eval은 결과물 점수만 보는 용도가 아닙니다. 어떤 실패가 있었는지, 그 실패가 트리거 문제인지, 데이터 수집 문제인지, 워크플로우 순서 문제인지 분해하는 도구로 써야 합니다. 영상의 PDF 데모도 결국 첫 출력이 틀렸다는 사실보다, **왜 틀렸는지를 다음 스킬 버전에 반영하는 피드백 루프** 가 더 핵심이었습니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=690)

셋째, description은 부가 정보가 아니라 호출 정확도를 좌우하는 인터페이스입니다. 스킬이 많아질수록 본문보다 description 충돌이 먼저 문제가 되기 때문에, 실제 사용자가 말할 법한 문장으로 trigger tuning을 반복하는 편이 낫습니다. 넷째, 앞으로는 스킬이 점점 상세 구현서보다 사양서에 가까워질 가능성이 있습니다. 영상 마지막 메시지도 자연어로 원하는 바를 더 상위 수준에서 말하면 모델이 나머지를 더 많이 채워 넣는 방향을 가리킵니다. 그래서 지금부터는 절차를 너무 장황하게 늘어놓기보다, **성공 기준과 판단 조건을 선명하게 적는 습관** 이 더 중요해질 수 있습니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=430)

## 핵심 요약

- 이 영상은 스킬을 capability uplift와 encoded preference로 나눠 봐야 유지 전략이 보인다고 설명합니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=95)
- skill-creator 업데이트의 핵심은 초안 생성이 아니라 eval, benchmark, trigger tuning을 포함한 운영 루프입니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=230)
- 평가의 목적은 회귀를 잡는 것뿐 아니라, 기본 모델이 더 좋아졌을 때 불필요해진 스킬을 정리하는 데도 있습니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=300)
- 라이브 데모는 첫 결과가 틀릴 수 있음을 숨기지 않고, 피드백을 통해 데이터 정확도와 조사 깊이를 보강하는 과정을 보여 줍니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=690)
- 결국 오래 남는 스킬은 예쁜 출력보다도 팀의 판단 순서, 검증 기준, 반복 가능한 절차를 더 많이 담고 있는 스킬입니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=145)

## 결론

이 영상이 보여 준 skill-creator의 진짜 가치는 "스킬 제작 자동화" 자체가 아닙니다. 더 큰 변화는 스킬을 한 번 만들고 잊는 프롬프트 파일이 아니라, **측정하고 비교하고 폐기 여부까지 판단하는 운영 대상** 으로 다루게 만들었다는 점입니다.<br>그래서 앞으로 Claude Code에서 스킬을 더 많이 쓰게 될수록 중요한 질문은 "이 스킬을 만들 수 있는가" 가 아니라, **"이 스킬이 아직도 필요한가, 제대로 발동하는가, 우리 방식대로 일하게 만드는가"** 가 될 가능성이 큽니다. [근거 영상](https://youtu.be/RAZVk5NPNtE?t=930)

<!--
Evidence notes
- claim: The video frames the update as making skills much easier to build and stronger to use, then explains and live-builds a new skill | transcript/time marker: "skills just got 10 times easier to build and stronger to use" / intro and setup / ~0:00 | video url: https://youtu.be/RAZVk5NPNtE?t=0 | confidence: high
- claim: Skills are presented as text recipes, and the video distinguishes capability uplift from encoded preference skills | transcript/time marker: "it's basically just a recipe" / "two different types of skills" / ~1:35 | video url: https://youtu.be/RAZVk5NPNtE?t=95 | confidence: high
- claim: capability uplift skills may become redundant as base models improve, while encoded preference skills are more durable because they encode specific workflows | transcript/time marker: comparison of front-end design skill vs process-specific skill / ~2:25 | video url: https://youtu.be/RAZVk5NPNtE?t=145 | confidence: high
- claim: The idea-mining example is presented as a sequential workflow that checks comments, niche videos, X/web trends, runs parallel agents, and scores outputs into ideas | transcript/time marker: "idea mining" workflow with YouTube agent + research agent + scoring / ~2:00 | video url: https://youtu.be/RAZVk5NPNtE?t=120 | confidence: high
- claim: The updated skill-creator can create, improve, measure, benchmark, and optimize triggering for skills | transcript/time marker: walkthrough of the official skill-creator description and eval discussion / ~3:50 | video url: https://youtu.be/RAZVk5NPNtE?t=230 | confidence: high
- claim: The video ties the update to official capabilities around testing, benchmarking, and trigger tuning rather than just one-shot skill generation | transcript/time marker: official skill-creator walkthrough and benchmark discussion / ~5:30 | video url: https://youtu.be/RAZVk5NPNtE?t=330 | confidence: high
- claim: Evals are used both to catch regressions and to detect when a base model outperforms the skill, making the skill removable | transcript/time marker: regression and growth explanation / ~5:00 | video url: https://youtu.be/RAZVk5NPNtE?t=300 | confidence: high
- claim: Trigger tuning improves skill activation accuracy when many skills cause false triggers or misfires | transcript/time marker: trigger tuning explanation and score chart / ~6:30 | video url: https://youtu.be/RAZVk5NPNtE?t=390 | confidence: high
- claim: The presenter installs skill-creator, gives a vague weekly-report request, and the agent asks clarifying questions before producing a plan | transcript/time marker: install flow, project-scope prompt, and follow-up questions / ~8:45 | video url: https://youtu.be/RAZVk5NPNtE?t=525 | confidence: medium
- claim: The demo shows the generated skill wiring `SKILL.md` to scripts and reusing an existing YouTube data script from the project | transcript/time marker: walkthrough of skill file and existing script reuse / ~13:00 | video url: https://youtu.be/RAZVk5NPNtE?t=780 | confidence: high
- claim: The first generated PDF looked good aesthetically but had wrong or missing data, leading to a second round of feedback focused on deeper research quality | transcript/time marker: first PDF review and criticism of incorrect data / ~11:30 | video url: https://youtu.be/RAZVk5NPNtE?t=690 | confidence: high
- claim: The improved result included stronger metrics, SWOT, comments, competitor context, and AI trend analysis after rerunning the skill | transcript/time marker: final report walkthrough / ~14:30 | video url: https://youtu.be/RAZVk5NPNtE?t=870 | confidence: high
- claim: The video ends by arguing that future skills may move closer to natural-language specifications rather than detailed implementation instructions | transcript/time marker: "natural language description" and future direction discussion / ~7:10 and closing summary / video url: https://youtu.be/RAZVk5NPNtE?t=430 | confidence: medium
- claim: The closing message reframes the update as a system for repeatedly improving and rerunning skills rather than building once and stopping | transcript/time marker: closing emphasis on keep running it and keep saying what you liked or disliked / ~15:30 | video url: https://youtu.be/RAZVk5NPNtE?t=930 | confidence: medium
-->
