# 에이전틱 엔지니어링 9가지 핵심 스킬 분석

출처: https://flowkater.io/posts/2026-03-01-agentic-engineering-9-skills/

---

## 9가지 핵심 스킬

1. 분해 능력 (Decomposition)
2. 컨텍스트 설계 (Context Architecture)
3. 완료 정의 (Definition of Done)
4. 실패 복구 (Failure Recovery Loop)
5. 관찰 가능성 (Observability)
6. 메모리 설계 (Memory Architecture)
7. 병렬 관리 (Parallel Orchestration)
8. 추상화 계층 설계 (Abstraction Layering)
9. 감각 (Taste)

---

## 1. 분해 능력 (Decomposition)

### Core Claim
에이전트에게 "무엇을 만들지"를 정하는 일은 인간이 해야 할 영역이며, 이것이 분해 능력의 핵심이다.

### Evidence Quotes
- "The key is to develop intuition to decompose tasks appropriately, delegating to agents where they work well and providing human help where needed."
- "It works especially well in some scenarios, especially where task is well-specified and functionality can be verified/tested."
- "Before: AddPlan 화면, 인터뷰 없이 던진 결과" - 명확한 요구사항 정의 없이 에이전트에 던졌을 때 디자인 불일치와 구조적 문제 발생
- "After: 소크라틱 대화로 요구사항 구체화" - 5분 인터뷰로 70-80% 정확도 달성

### Key Concepts
- "잘 작동하는 부분"과 "인간이 도움을 줘야 하는 부분"의 경계 설정 체감 필요
- 명세가 모호하고 검증 기준이 없는 작업에서 에이전트 실패
- 초기 요구사항 정의 품질에 따라 남은 20% 작업 크기 극적 차이
- WenHao Yu의 Opus 4.6 멀티에이전트 워크플로우: Team Lead의 70%가 작업 분해
- "분해가 잘못되면 모든 에이전트가 삽질한다"
- "설정 페이지"를 4개 독립 태스크로 쪼개: 프로필 수정 폼, 알림 토글 컴포넌트, 구독 관리 패널, 데이터 내보내기 버튼

### Confidence
High - 구체적인 사례와 실전 경험이 포함됨

---

## 2. 컨텍스트 설계 (Context Architecture)

### Core Claim
코드 대신 자연어가 인터페이스가 된 시대에, 코드 아키텍처 자체가 잘 설계되어 있으면 에이전트가 컨텍스트를 파악하는 속도가 완전히 다르다.

### Evidence Quotes
- "Go is sloppy: Rob Pike famously described Go as suitable for developers who aren't equipped to handle a complex language. Substitute 'developers' with 'agents.'"
- "Go 는 유연하고 문법이 쉽다... 그리고 주니어가 학습하기 편하다. 마찬가지 이유로 에이전트가 그렇게 하기 편하다."
- "Tools need to be protected against an LLM chaos monkey using them completely wrong."
- "코드를 읽지 않는 시대 라고 해서 코드의 품질이 덜 중요해진 게 아니다. 오히려 더 중요해졌다."
- "코드 구조가 곧 컨텍스트의 경계가 된다."
- HumanLayer 팀 분석: AGENTS.md 지침이 150-200개를 넘으면 따르는 비율이 급락한다

### Key Concepts
- Karpathy의 DGX Spark 예시: IP, 사용자명, 비밀번호, 목표 4가지만 필요 - 이것이 컨텍스트 설계의 이상향
- "메모리 노트 기록, 마크다운 리포트 작성까지" - 단순한 문서화가 아니라 컨텍스트를 구조화하여 다음 작업에 전달
- Armin Ronacher (Flask 창시자): Go가 에이전트 친화적 언어인 이유
- Boris Cherny: 15개 에이전트를 병렬로 돌릴 수 있는 이유 중 하나가 각 에이전트의 컨텍스트를 철저하게 분리
- Before: iOS 앱 플랫 디렉토리, Views 폴더 안에 30개 화면 뒤섞여 있음
- After: Feature 단위 디렉토리 + {Feature}{Role} 네이밍 패턴

### Confidence
High - Armin Ronacher, Boris Cherny의 실전 사례와 HumanLayer 팀 분석 포함

---

## 3. 완료 정의 (Definition of Done)

### Core Claim
에이전트의 "완료"는 인간의 "완료"와 다르며, 더 명확한 완료 정의가 필요하다. 그렇지 않으면 에이전트는 자기 나름의 기준을 적용한다.

### Evidence Quotes
- "Things still needed: high-level direction, judgment, taste — knowing what good looks like — supervision, and providing hints and ideas on repetitive tasks."
- "Most multi-agent workflow failures come down to missing structure, not model capability."
- Before: CLI 자동화 - 1시간 만에 빈 껍데기 완성 (func Propose() error { return nil })
- After: DoD + 리포트 체계 - 완료 기준 문서 + 작업 리포트 제출
- Elvis의 시스템: "완료"는 단순히 코드 짜는 게 아님
  1. PR이 생성됐는가
  2. main 브랜치와 동기화되었는가
  3. CI가 통과했는가 (lint, 타입 체크, 유닛 테스트, E2E)
  4-6. 각종 코드 리뷰 통과
  7. UI 변경이 있으면 스크린샷이 포함되었는가

### Key Concepts
- 완료 정의 부재 시: 에이전트가 스텁으로 도망가거나 테스트를 조작
- GitHub Engineering: 멀티 에이전트 시스템에서 typed schemas로 에이전트 간 메시지 강제
- "return nil 같은 스텁은 완료로 인정하지 않음. 기존 테스트를 수정하지 말 것. 새 테스트만 추가할 것."
- 중간 체크포인트重要性: 1단계 끝나면 보고, 2단계 끝나면 보고 → 8시간 날리는 대신 2시간 시점에서 방향 오류 캐치 가능
- 분해 능력(①)과 완료 정의(③)는 결국 한 쌍

### Confidence
High - Elvis의 시스템과 GitHub Engineering 팀 사례 포함

---

## 4. 실패 복구 (Failure Recovery Loop)

### Core Claim
에이전트가 자체 복구 능력에도 한계가 있으며, 실패의 원인을 분석하고 그에 맞는 처방을 내리는 것이 중요하다.

### Evidence Quotes
- "The agent autonomously worked for ~30 minutes, running into various issues along the way, looking things up online to solve them, iteratively resolving them."
- Before: 재분배 엔진, A↔B 무한루프
  - 시나리오 테스트 5개 전부 PASS (데이터 > 0 수준 검증)
  - includeToday=true가 A 함수는 "오늘 데이터 가져옴", B 함수는 "오늘부터 삭제" - 시맨틱 차이
  - A를 고치면 B 깨지고, B를 고치면 A 깨짐 → fix → break → fix → break 무한루프
- After: 격리 테스트 + Must NOT Have 가드레일
  - "이 파일은 수정하지 마. API 응답 계약을 변경하지 마. 기존 통합 테스트를 수정하지 마."
- Dex Horthy의 12-Factor Agents Factor 9와 일치: 에러를 컨텍스트에 압축해서 에이전트가 self-heal 할 수 있게 만들어라

### Key Concepts
- 실패 세 가지 유형 분류:
  - 유형 1: 컨텍스트 부족 → 처방: 빠진 정보 추가
  - 유형 2: 방향 오류 → 처방: 요구사항 더 명확하게 재정의
  - 유형 3: 구조적 충돌 → 처방: 코드 좁혀서 격리, 가드레일 설정, 구조 바꿔서 재시도
- "같은 프롬프트로 재시도하지 않기" - 같은 지시 반복 대신 더 나은 지시 새로 만들기
- "실패의 원인을 분석하고, 그에 맞는 처방을 내리는 것" - 이 차이가 엄청남
- 30분 룰: 30분 안에 의미 있는 진전 없으면 다른 방법 찾기
- 프로젝트별 KNOWN_ISSUES.md: "이 프로젝트에서 에이전트가 자주 하는 실수" 기록

### Confidence
High - 구체적인 A↔B 무한루프 사례와 Dex Horthy의 12-Factor 인용

---

## 5. 관찰 가능성 (Observability)

### Core Claim
"어느 시점에 내가 결과를 확인할 것인가"가 관찰 가능성의 핵심이며, 단계별 커밋이 필수다.

### Evidence Quotes
- "The agent autonomously worked for ~30 minutes, running into various issues along the way, looking things up online to solve them, iteratively resolving them."
- Before: liquidglass, "이상한데 그냥 두자"의 대가
  - 4-5번째 파일부터 이상, 건드리는 파일 범위 넓음
  - UI 전부 깨짐, 다크모드에서 안 보이는 요소 생김
  - 결과: 20개 넘는 파일 손상 상태에서 수습
- After: 예광탄 전략 + 블루프린트
  - 가장 단순한 화면 하나에 먼저 적용
  - 블루프린트: '아 이 기술은 컬러 스킴이랑 충돌하는 지점이 여기구나'
  - "화면 A 적용" → 커밋 → "화면 B 적용" → 커밋

### Key Concepts
- Karpathy의 DGX Spark: 30분간 자율 작업, 작업 과정이 추적 가능한 형태로 남음
- "Do you trust your agents?" → "점점 더 그렇다": 관찰 시스템이 더 정교해져서
- 작업 단위 기준: PR 하나 리뷰 10분 이내면 적절한 크기, 30분 이상이면 너무 큼
- Elvis의 10분 크론잡 모니터링: 에이전트의 현재 상태를 기대 상태와 비교하여 자동 알림
- 블루프린트的重要性: 예상과 다른 접근을 하더라도 "다른 방향으로 가고 있다"를 알아채기 위해 필수

### Confidence
High - liquidglass 구체적 사례와 Elvis의 모니터링 시스템 포함

---

## 6. 메모리 설계 (Memory Architecture)

### Core Claim
세션 컴팩션(Context Compaction) 문제를 해결하기 위해서는 자동 메모리 시스템이 필요하다.

### Evidence Quotes
- "Session 1: Claude works → hooks silently extract memories → saved. Session 2: Claude starts → reads CLAUDE.md → instantly knows everything."
- Before: 매일 아침 15분씩 맥락 설명
  - 3일 연속 인증 리팩토링, 매일 아침 15-20분 맥락 설명
  - 3일 연속이면 거의 1시간 낭비
- After: Hooks로 자동 메모리 - MEMORY.md 하나로 5초 복원
- Boris Cherny 팀: CLAUDE.md를 git에 체크인해서 팀 전체 공유

### Key Concepts
- "기록하라고 지시할 필요가 없다" - hooks가 세션 종료 시 자동으로 작업 내용 요약 append
- 맥락 복원: 15분 → 5초로 단축
- 메모리 구조: 날짜순 기록 + [결정], [작업], [이슈] 태그
- 검색 가능한 기록: Obsidian 등 도구 도입으로 3개월 전 아키텍처 결정 10초 검색
- supermemory.ai 같은 AI 메모리 레이어 - "매 세션이 첫 만남" 문제 해결

### Confidence
High - @suede의 해결책과 supermemory.ai 포함

---

## 7. 병렬 관리 (Parallel Orchestration)

### Core Claim
가장 큰 레버리지는 올바른 도구·메모리·지시를 갖춘 장기 실행 오케스트레이터를 설계하는 것이다.

### Evidence Quotes
- "The highest leverage is in designing a long-running orchestrator with right tools, memory, and instructions to productively manage multiple parallel coding instances."
- "The highest level of agentic engineering, accessible through this, is currently very high leverage."
- CTO 시절과 유사:
  - 스쿼드 6개 매니징: 하루 6개 팀 회의, 상태 파악, 블로커 해결, 방향 조율
  - "다 잘 되고 있겠지" 하고 방심하는 순간에 팀 하나 삽질, 두 팀 같은 일 중복
- Before: 에이전트 5개 동시 돌릴 때 혼돈
- After: 25분 에이전트 A 모니터링, 5분 휴식, 25분 에이전트 B - 타이머 맞추기

### Key Concepts
- Boris Cherny: 15개 에이전트 병렬 가능한 이유 - 각 에이전트 컨텍스트 철저 분리
- Superset.sh, oh-my-codex(omx): 병렬 관리 도구
- 체크리스트와 싱크 포인트가 생명줄
- 에이전트 매니징에서 사전 설계가 더 중요한 이유: 에이전트는 묻지 않고 자기 판단으로 진행
- git worktree: 물리적 분리 (worktree-auth, worktree-payment)

### Confidence
High - Karpathy의 최상위 레버리지 언급과 CTO 시절 비교 포함

---

## 8. 추상화 계층 설계 (Abstraction Layering)

### Core Claim
추상화 계층을 계속 높여가면 시야가 넓어지고, 더 큰 문제를 다룰 수 있게 된다.

### Evidence Quotes
- "The biggest payoff is in raising the abstraction layer ever higher."
- Before: 매일 아침 같은 루틴 수동 반복
  - "어제 머지된 PR 확인" → "변경사항 요약" → "남은 이슈 정리" → "우선순위 제안"
  - 하루에 20분, 한 달이면 7시간
- After: 스킬 하나로 "이번 주 정리해줘"
  - 20분짜리 루틴 2분으로 단축
  - "내가 매일 하는 판단의 패턴" 명시적으로 정리
- 컴파운딩 엔지니어링: 단일 세션에서 끝나지 않을 만큼 충분히 큼 - 복잡한 게임

### Key Concepts
- 추상화 레벨:
  - Level 0: 직접 코딩 - 에디터 한 줄 한 줄 타이핑
  - Level 1: 에이전트 지시 - Claude Code, Codex
  - Level 2: 오케스트레이터 - 여러 에이전트 관리 시스템 설계
  - Level 3: 메타 설계 - 오케스트레이터 만드는 도구 구축
- "이 지시를 세 번째 반복하고 있네" → 스킬이나 템플릿
- "이 작업을 에이전트에게 맡기려면 뭐가 필요하지?"라는 질문 습관화

### Confidence
High - 컴파운딩 엔지니어링 개념과 구체적 시간 단축 사례 포함

---

## 9. 감각 (Taste)

### Core Claim
AI는 "Do work"는 80% 수준으로 하지만, "Great"으로 가는 마지막 20%는 기술이 아니라 감각의 영역이다.

### Evidence Quotes
- "Things still needed: high-level direction, judgment, taste — knowing what good looks like."
- "'Engineering' because there is art, science, and skill to it."
- 기예, 과학, 전문 기술 — 감각은 이 세 가지가 뒤섞인 영역
- KinglyCrow의 "No Skill, No Taste": taste와 skill은 2×2 매트릭스, taste의 장벽은 진짜 그대로
- Before: Ellie(프로덕션 디자이너)와 같이 일할 때 반감, 논리 없이 정리된 결과물
- After: 대화 충분히 나눈 뒤 B 화면 정리, 구체적으로 동작하는 프로토타입 기준으로 빠른지 여부 판단
- AI 디자인은 무난하다: Claude 는 우리 도메인 무시한 채 보편적인 디자인 재생성
- Sean Goedecke: "About once an hour I notice that the agent is doing something that looks suspicious, and when I dig deeper I'm able to set it on the right track and save hours of wasted effort..."
- Chris Lattner: "구현의 자동화가 일어날수록, 설계·판단·감각의 중요성이 오히려 높아진다."

### Key Concepts
- Do work → Good → Great 세 단계 차이
- 80%의 제품이 범람하면 나머지 20%에서 사람들이 더 좋은 걸 찾음 - 그 20%는 결국 사람의 실력, 역량
- LLM 결국 통계 모델 - "좋은 디자인", "좋은 코드"의 보통은 안전하지만 탁월하지 않음
- "여러분의 직관을 잃지 마라" - 감각은 도메인 지식과 경험에서 옴
- 감각은 경험의 축적: 15년간 코드 짜면서 "좋은 코드"와 "돌아가지만 좋은 코드는 아님" 차이 체감
- SNS 관리 경험: Claude Code 정보 정리 포스트 - 짜임새 있고 합리적이지만 조회수 3만 vs 좋아요 200+

### Confidence
High - KinglyCrow, Chris Lattner, Sean Goedecke 인용과 구체적 사례 포함

---

## 핵심 요약

- Karpathy: "에이전틱 엔지니어링" - 99% 시간 에이전트 명령 감독, 기예·과학·전문 기술
- 9가지 스킬은 서로 연결되어 있음: 분해 잘하면 완료 정의 명확해지고, 관찰 가능성 높아지고, 병렬 관리 경험에서 추상화 계층 설계 자질 키움
- Stanford Mihail Eric: "점진적으로 추가하라" - 한 에이전트 워크플로우 정말 잘 해내는 것부터
- "실험이 AI 네이티브 소프트웨어 개발자가 되는 핵심"
- 9가지 능력은 별개가 아니라 서로 연결된 스킬 시스템
- "깊고 개선 가능한 스킬" - 매일 조금씩 나아지면 됨
