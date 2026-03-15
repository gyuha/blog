---
title: "🚀 GSD + PM-Skills + UI-UX-Pro-Max: 최강의 바이브코딩 3종 세트 완벽 가이드"
date: 2026-03-15T12:44:58+09:00
draft: false
categories:
  - AI
  - Development
  - Productivity
tags:
  - Claude Code
  - AI Agents
  - Workflow
  - Multi-Agent
  - GSD
  - oh-my-claudecode
  - Superpowers
---

> *"프롬프트 하나로 아이디어에서 완성된 프로덕트까지"*  
> AI가 코드를 짜는 시대, 진짜 경쟁력은 **어떤 도구를 어떻게 조합하느냐**에 달려 있다.
<!--more-->

---

## 📌 들어가며: 바이브코딩이란?

**바이브코딩(Vibe Coding)** 은 AI 코딩 어시스턴트에게 자연어로 의도를 전달하고, AI가 코드를 생성하며, 개발자는 방향을 잡고 검증하는 새로운 개발 패러다임입니다.

하지만 "그냥 채팅하면서 코딩하는 것"으로는 한계가 뚜렷합니다. Context Rot(문맥 퇴화), 일관성 없는 UI, 요구사항 누락... 이런 문제를 한 번에 해결하는 **궁극의 3종 조합**이 있습니다.

| 도구 | 역할 | 한마디 설명 |
|------|------|-------------|
| **GSD (Get Shit Done)** | 🔧 개발 워크플로우 엔진 | Spec-Driven Development로 아이디어→코드 전체 사이클 관리 |
| **PM-Skills** | 📋 프로덕트 매니저 AI | 65개 PM 스킬 + 36개 워크플로우로 기획·전략·분석 자동화 |
| **UI-UX-Pro-Max-Skill** | 🎨 디자인 인텔리전스 | 67개 UI 스타일, 161개 컬러 팔레트, 57개 폰트 페어링으로 프로급 디자인 |

이 세 가지를 조합하면 **"1인 프로덕트 팀"** 이 완성됩니다.

---

## 🧩 각 도구 Deep Dive

### 1️⃣ GSD (Get Shit Done) — 개발의 뼈대를 세우는 엔진

GSD는 GitHub 23K+ 스타를 기록한 Spec-Driven Development 도구입니다. Claude Code의 네이티브 기능(Skills, Agents, Hooks)만으로 구성되어 있으며, 약 50개의 마크다운 파일이 전체 소프트웨어 개발 사이클을 오케스트레이션합니다.

**핵심 슬래시 커맨드:**

```
/gsd:new-project       → 아이디어 캡처, 도메인 리서치, 요구사항 & 로드맵 정의
/gsd:discuss-phase N   → Phase N의 구현 세부사항 논의
/gsd:plan-phase N      → Phase N의 태스크 분류 생성
/gsd:execute-phase N   → 계획을 병렬 실행, 태스크당 하나의 커밋
/gsd:verify-work N     → Phase 목표 달성 검증
/gsd:complete-milestone → 아카이브, 릴리스 태그, 다음 사이클 초기화
```

**GSD가 해결하는 핵심 문제: Context Rot**

긴 코딩 세션에서 토큰 컨텍스트 윈도우가 차면서 AI의 품질이 점진적으로 떨어지는 문제를 `.planning/` 디렉토리에 모든 상태를 파일로 기록해 해결합니다.

```
.planning/
├── PROJECT.md          # 무엇을, 왜 만드는지
├── config.json         # 워크플로우 설정
├── REQUIREMENTS.md     # 정확한 요구사항 (ID 포함)
├── ROADMAP.md          # 실행 순서
├── STATE.md            # 현재 진행 상태
└── research/           # 도메인 리서치 결과
```

### 2️⃣ PM-Skills — AI 프로덕트 매니저

PM-Skills Marketplace는 65개의 PM 스킬과 36개의 체인 워크플로우를 8개 플러그인으로 구성합니다. Teresa Torres, Marty Cagan, Alberto Savoia의 프레임워크를 AI 워크플로우로 구현한 것입니다.

**8개 플러그인 맵:**

| 플러그인 | 스킬 수 | 주요 커맨드 |
|----------|---------|-------------|
| pm-product-discovery | 13 | `/discover`, `/brainstorm`, `/interview` |
| pm-product-strategy | 12 | `/strategy`, `/business-model`, `/pricing` |
| pm-execution | 15 | `/write-prd`, `/plan-okrs`, `/sprint` |
| pm-market-research | 7 | `/research-users`, `/competitive-analysis` |
| pm-data-analytics | 3 | `/write-query`, `/analyze-test` |
| pm-go-to-market | 6 | `/plan-launch`, `/battlecard` |
| pm-marketing-growth | 5 | `/market-product`, `/north-star` |
| pm-toolkit | 4 | `/review-resume`, `/proofread` |

### 3️⃣ UI-UX-Pro-Max-Skill — 디자인 인텔리전스 엔진

GitHub 40K+ 스타의 이 스킬은 AI가 "그냥 예쁜" UI가 아니라 **산업별·브랜드별 맞춤 디자인 시스템**을 생성하도록 합니다.

**핵심 데이터베이스:**

- **67개 UI 스타일**: Glassmorphism, Neubrutalism, Bento Grid, AI-Native UI 등
- **161개 산업별 컬러 팔레트**: 각 산업에 맞는 색상 무드
- **57개 폰트 페어링**: Google Fonts 임포트 포함
- **161개 추론 규칙**: 프로젝트 유형 → 최적 디자인 시스템 자동 매칭
- **13개 테크 스택 지원**: React, Next.js, SwiftUI, Flutter 등

**작동 원리:**

```
사용자 요청 → 5개 병렬 검색(제품 유형, 스타일, 컬러, 패턴, 타이포그래피) 
           → 추론 엔진(BM25 랭킹) → 완성된 디자인 시스템 출력
```

---

## 🔗 3종 조합의 시너지: 왜 함께 써야 하는가?

```
[아이디어]
    │
    ▼
┌──────────────────────────────────────────────┐
│  PM-Skills: /discover, /strategy, /write-prd │  ← 기획 & 전략
│  "무엇을 왜 만들 것인가?"                      │
└──────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────┐
│  GSD: /gsd:new-project → /gsd:plan-phase    │  ← 구조화 & 계획
│  "어떤 순서로 어떻게 만들 것인가?"              │
└──────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────┐
│  UI-UX-Pro-Max + GSD: /gsd:execute-phase    │  ← 디자인 & 구현
│  "프로 수준의 UI로 실제 코드를 만든다"           │
└──────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────┐
│  GSD: /gsd:verify-work → /gsd:complete-milestone │  ← 검증 & 릴리스
│  PM-Skills: /sprint retro, /analyze-test     │
└──────────────────────────────────────────────┘
```

**각 도구가 채워주는 영역:**

| 없으면 생기는 문제 | 해결 도구 |
|-------------------|-----------|
| 요구사항이 모호해서 AI가 횡설수설 | **PM-Skills**가 구조화된 PRD 생성 |
| 코드가 뒤죽박죽, 커밋이 엉망 | **GSD**가 phase별 체계적 실행 |
| UI가 학생 프로젝트 수준 | **UI-UX-Pro-Max**가 프로급 디자인 시스템 적용 |
| 긴 세션에서 AI 품질 저하 | **GSD**의 파일 기반 상태 관리로 Context Rot 방지 |
| 출시 후 지표 분석 안 됨 | **PM-Skills**의 `/analyze-test`, `/north-star` 활용 |

---

## 🛠️ 설치 가이드 (5분 셋업)

### Step 1: GSD 설치

```bash
# Claude Code에서 실행
npx gsd-install
# 또는 수동 설치
git clone https://github.com/gsd-build/get-shit-done.git
cp -r get-shit-done/.claude/ ./.claude/
```

### Step 2: PM-Skills 설치

```bash
# Claude Code 마켓플레이스 방식
claude plugin marketplace add phuryn/pm-skills

# 개별 플러그인 설치 (필요한 것만)
claude plugin install pm-product-discovery@pm-skills
claude plugin install pm-product-strategy@pm-skills
claude plugin install pm-execution@pm-skills
claude plugin install pm-market-research@pm-skills
claude plugin install pm-go-to-market@pm-skills
```

### Step 3: UI-UX-Pro-Max-Skill 설치

```bash
# CLI 설치
npm install -g uipro-cli

# 프로젝트 디렉토리에서 초기화
cd /path/to/your/project
uipro init --ai claude

# Python 3.x 필요 (검색 스크립트용)
python3 --version  # 확인
```

### Step 4: 설치 확인

```bash
# GSD 커맨드 확인
/gsd:new-project --help

# PM-Skills 확인
/discover --help

# UI-UX-Pro-Max 확인
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "test" --domain style
```

---

## 📝 실전 프롬프트 예제 모음

### 🎯 시나리오 1: SaaS 프로덕트를 처음부터 만들기

#### Phase 0: PM-Skills로 디스커버리

```
/discover AI 기반 회의록 자동 요약 SaaS for 원격 근무 팀
```

> PM-Skills가 자동으로 실행하는 흐름:
> brainstorm-ideas → identify-assumptions → prioritize-assumptions → brainstorm-experiments

#### Phase 0.5: PM-Skills로 전략 수립

```
/strategy AI 회의록 요약 SaaS - 타겟: 50인 이상 IT 기업의 PM/엔지니어링 팀,
차별점: 실시간 요약 + 액션 아이템 자동 추출 + Jira 연동
```

```
/write-prd 
AI 회의록 요약 서비스 "MeetFlow"
- 문제: 회의 후 정리에 30분+ 소요, 핵심 결정사항 누락 빈번
- 해결: 실시간 음성→텍스트→구조화된 요약→액션 아이템 자동 추출
- 사용자: 10-200명 규모 IT 기업의 PM, 엔지니어링 리드
- 핵심 기능: 실시간 트랜스크립션, AI 요약, 액션 아이템 추출, Jira/Slack 연동
- 성공 지표: 회의 후 정리 시간 70% 감소
```

#### Phase 1: GSD로 프로젝트 초기화

```
/gsd:new-project

→ "What do you want to build?" 질문에 답변:

MeetFlow - AI 회의록 요약 SaaS
- Next.js 14 + TypeScript 프론트엔드
- Supabase 백엔드
- OpenAI Whisper API 음성→텍스트
- Claude API 요약/추출
- shadcn/ui 컴포넌트
- Jira, Slack REST API 연동

PRD는 .planning/ 폴더에 이미 생성되어 있음 (.planning/PRD.md 참조)
```

#### Phase 1.5: UI-UX-Pro-Max로 디자인 시스템 생성

```
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "SaaS productivity meeting" --design-system -p "MeetFlow" --persist
```

또는 자연어로:

```
MeetFlow의 디자인 시스템을 만들어줘.
- SaaS 프로덕티비티 도구
- 타겟: IT 기업의 PM/엔지니어
- 톤: 프로페셔널하면서 친근한
- 모드: 다크모드 우선 (코드 에디터 친화적)
- 스택: Next.js + shadcn/ui + Tailwind
```

#### Phase 2: GSD로 실행

```
/gsd:plan-phase 1

→ GSD가 Phase 1을 태스크로 분해:
  Task 1: 프로젝트 스캐폴딩 (Next.js + Supabase)
  Task 2: 인증 시스템 (Supabase Auth)
  Task 3: 대시보드 레이아웃 (디자인 시스템 적용)
  Task 4: 회의 목록 페이지

/gsd:execute-phase 1

→ 4개 태스크가 병렬로 실행, 각각 독립 커밋 생성
→ UI-UX-Pro-Max 스킬이 자동 활성화되어 디자인 시스템 적용
```

---

### 🎯 시나리오 2: 이커머스 랜딩 페이지 빠르게 만들기

#### 한 번에 전체 흐름 프롬프트:

```
/strategy 프리미엄 반려동물 용품 D2C 이커머스 "PawLux"

→ 전략 완료 후:

/write-prd PawLux 랜딩 페이지
- 히어로 섹션: 감성적 반려동물 이미지 + 가치 제안
- 베스트셀러 제품 4개 쇼케이스
- 고객 후기 섹션 (별점 + 반려동물 사진)
- 구독 혜택 안내 (월 정기배송)
- FAQ 아코디언
- 뉴스레터 가입 CTA
```

#### UI-UX-Pro-Max로 디자인 시스템:

```
PawLux 랜딩 페이지를 만들어줘.
프리미엄 반려동물 용품 D2C 브랜드야.
- 따뜻하고 프리미엄한 느낌
- 타겟: 30-45세 반려동물 집사, 프리미엄 소비 성향
- Hero-Centric + Social Proof 패턴
- HTML + Tailwind 스택
- 모바일 우선 반응형
```

> UI-UX-Pro-Max가 자동으로 추론:
> - 스타일: Organic Biophilic 또는 Soft UI Evolution
> - 컬러: Warm earth tones + Gold accents
> - 폰트: Playfair Display / Inter (고급+가독성)
> - 안티패턴: Cyberpunk, Neon 컬러, Dark Mode 회피

#### GSD로 실행:

```
/gsd:new-project --auto
→ 자동 모드로 빠르게 프로젝트 초기화

/gsd:plan-phase 1
/gsd:execute-phase 1
```

---

### 🎯 시나리오 3: 기존 프로젝트에 새 기능 추가

#### PM-Skills로 기능 분석:

```
/brainstorm experiments existing
우리 SaaS의 온보딩 플로우에서 이탈률이 40%야.
현재 플로우: 가입 → 프로필 설정 → 팀 초대 → 첫 프로젝트 생성 (4단계)
가설: 단계를 2개로 줄이면 이탈률이 20% 이하로 떨어질 것
```

```
/write-prd
온보딩 개선 v2
- 현재: 4단계 (이탈률 40%)
- 개선: 2단계 (가입 → 가이디드 첫 프로젝트)
- 프로필/팀 초대는 후속 넛지로 이동
- 인터랙티브 튜토리얼 + 프로그레스 바 추가
- A/B 테스트: 기존 vs 새 플로우
```

#### GSD로 계획 & 실행:

```
/gsd:discuss-phase 3
이 프로젝트에 온보딩 개선 기능을 추가하려고 해.
.planning/PRD-onboarding-v2.md 파일을 참조해줘.
기존 코드베이스의 /src/features/onboarding/ 폴더를 수정해야 해.

/gsd:plan-phase 3
/gsd:execute-phase 3
```

#### 결과 검증:

```
/gsd:verify-work 3

→ 검증 완료 후:

/analyze-test
온보딩 A/B 테스트 결과:
- 컨트롤 그룹(4단계): 완료율 60%, n=1,200
- 실험 그룹(2단계): 완료율 78%, n=1,150
- 기간: 14일
- 주요 지표: 온보딩 완료율, 7일 리텐션, 첫 프로젝트 생성률
```

---

### 🎯 시나리오 4: 대시보드 UI 디자인 특화

```
핀테크 분석 대시보드를 만들어줘.

요구사항:
- 실시간 거래 모니터링
- 포트폴리오 성과 차트 (Line + Area)
- 자산 배분 파이차트
- 거래 내역 테이블 (정렬/필터)
- 알림 패널

디자인:
- Executive Dashboard 스타일
- 다크모드 기본
- 데이터 밀도 높게
- React + shadcn/ui + Recharts 스택

PM 관점:
- 타겟: 30-50대 개인투자자
- 핵심 지표: 포트폴리오 수익률, 리스크 스코어
- 1분 이내에 핵심 정보 파악 가능해야 함
```

---

### 🎯 시나리오 5: 모바일 앱 컨셉 → 프로토타입

#### PM-Skills로 시장 조사:

```
/competitive-analysis 명상 & 수면 앱 시장 (Calm, Headspace, Meditopia)

/research-users
타겟: 25-40세 직장인, 수면 문제 + 스트레스 관리 니즈
특히 한국 시장에서의 차별화 포인트 찾기

/value-proposition 
AI 기반 개인화 명상 앱 "ZenFlow"
기존 명상 앱과 다르게 사용자의 스트레스 레벨을 
웨어러블 데이터(심박수, HRV)로 실시간 분석하여
최적의 명상 콘텐츠를 자동 추천
```

#### UI-UX-Pro-Max로 디자인:

```
ZenFlow 명상 앱 UI를 만들어줘.
- 플랫폼: React Native (iOS + Android)
- 스타일: Organic Biophilic + Soft UI
- 핵심 화면: 홈(오늘의 추천), 명상 플레이어, 수면 트래커, 통계
- 부드럽고 차분한 애니메이션
- 다크모드 기본 (수면 전 사용)
- 접근성: WCAG AA 준수
```

#### GSD로 구현:

```
/gsd:new-project

ZenFlow - AI 개인화 명상 앱
- React Native (Expo)
- Supabase 백엔드
- Apple HealthKit / Google Fit 연동
- React Navigation v7
- Reanimated 3 애니메이션

/gsd:plan-phase 1
→ Phase 1: 앱 스캐폴딩 + 네비게이션 + 홈 화면 + 디자인 시스템 적용

/gsd:execute-phase 1
```

---

### 🎯 시나리오 6: GTM(Go-to-Market) 전략 + 랜딩 페이지

```
/plan-launch 
AI 코드 리뷰 도구 "CodeOwl"
타겟: 10-50명 규모 엔지니어링 팀
가격: 월 $29/시트 (프리미엄), 무료 5명까지
채널: Product Hunt, Dev.to, Twitter/X, Discord

/north-star
CodeOwl - AI 코드 리뷰 도구
비즈니스 모델: B2B SaaS, 시트 기반 요금
핵심 가치: 코드 리뷰 시간 50% 절감
```

그 후 바로 랜딩 페이지 구현:

```
CodeOwl의 Product Hunt 런칭용 랜딩 페이지를 만들어줘.
/plan-launch 결과를 기반으로:

- Conversion-Optimized 패턴
- 히어로: "코드 리뷰, 이제 AI와 함께" + 데모 GIF 영역
- 3가지 핵심 기능 카드
- 가격표 (Free vs Pro 비교)
- 얼리 어답터 대기열 CTA
- 기술 스택: Next.js + shadcn/ui
- 스타일: AI-Native UI (Developer 친화적)
```

---

## 🔄 통합 워크플로우: 전체 프로세스 한눈에

```
┌─────────────────────────────────────────────────────┐
│                    PHASE 0: DISCOVERY                │
│  PM-Skills                                           │
│  /discover → /strategy → /value-proposition          │
│  /competitive-analysis → /research-users             │
│                                                      │
│  Output: 전략 문서, 경쟁 분석, 사용자 리서치           │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                    PHASE 1: SPECIFICATION            │
│  PM-Skills + GSD                                     │
│  /write-prd → /plan-okrs → /gsd:new-project          │
│                                                      │
│  Output: PRD, OKR, PROJECT.md, REQUIREMENTS.md       │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                    PHASE 2: DESIGN                   │
│  UI-UX-Pro-Max                                       │
│  Design System Generation → MASTER.md                │
│  Page-specific overrides → pages/*.md                │
│                                                      │
│  Output: 완성된 디자인 시스템 (컬러, 폰트, 스타일)     │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                    PHASE 3: EXECUTION                │
│  GSD + UI-UX-Pro-Max                                 │
│  /gsd:plan-phase N → /gsd:execute-phase N            │
│  (UI-UX-Pro-Max 자동 활성화)                          │
│                                                      │
│  Output: 실제 코드, Phase별 커밋                      │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                    PHASE 4: VERIFY & ITERATE         │
│  GSD + PM-Skills                                     │
│  /gsd:verify-work N → /sprint retro                  │
│  /analyze-test → /north-star                         │
│                                                      │
│  Output: 검증 완료, 회고, 다음 사이클 계획             │
└─────────────────────────────────────────────────────┘
```

---

## 💡 프로 팁: 3종 조합 시 알아야 할 것들

### ✅ DO — 이렇게 하세요

1. **항상 PM-Skills로 시작하세요** — `/discover`나 `/write-prd`로 요구사항을 먼저 명확히 하면 GSD와 UI-UX-Pro-Max의 결과물 품질이 확연히 올라갑니다.

2. **디자인 시스템을 persist하세요** — `--persist` 플래그로 `design-system/MASTER.md`를 생성하면 세션 간에도 일관된 디자인이 유지됩니다.

3. **GSD의 Phase를 작게 나누세요** — Phase당 3-5개 태스크가 이상적입니다. 너무 크면 Context Rot이 발생합니다.

4. **새 세션마다 `/gsd:resume-work`** — GSD가 `.planning/STATE.md`를 읽어 이전 상태를 자동 복구합니다.

### ❌ DON'T — 이건 피하세요

1. **모든 것을 한 세션에 하려 하지 마세요** — Phase 단위로 세션을 나누는 게 품질 유지의 핵심입니다.

2. **디자인 시스템 없이 UI 코드를 생성하지 마세요** — "예쁘게 만들어줘"는 프롬프트가 아닙니다. UI-UX-Pro-Max의 추론 엔진을 먼저 돌리세요.

3. **PM-Skills의 출력을 무시하고 바로 코딩하지 마세요** — PRD와 전략 문서가 GSD의 `.planning/` 파일에 반영되어야 전체 파이프라인이 작동합니다.

---

## 📋 바이브코딩 프롬프트 템플릿

### 🗂️ Template 1: 새 프로젝트 킥오프 통합 템플릿

```markdown
# 📋 프로젝트 킥오프 프롬프트

## 1. Discovery (PM-Skills)
/discover [프로덕트 이름] - [한 줄 설명]

## 2. Strategy (PM-Skills)
/strategy [프로덕트 이름]
- 타겟 사용자: [구체적 페르소나]
- 핵심 문제: [해결하려는 문제]
- 차별화 포인트: [경쟁사 대비 우위]
- 비즈니스 모델: [수익화 방식]

## 3. PRD (PM-Skills)
/write-prd
[프로덕트 이름] v1.0
- 문제 정의: [___]
- 타겟 사용자: [___]
- 핵심 기능 (v1 스코프):
  1. [기능 1]: [설명]
  2. [기능 2]: [설명]
  3. [기능 3]: [설명]
- 성공 지표: [___]
- 기술 제약: [___]

## 4. 프로젝트 초기화 (GSD)
/gsd:new-project

[프로덕트 이름] - [한 줄 설명]
Tech Stack:
- Frontend: [___]
- Backend: [___]
- Database: [___]
- 기타: [___]

PRD 위치: .planning/PRD.md

## 5. 디자인 시스템 (UI-UX-Pro-Max)
[프로덕트 이름]의 디자인 시스템을 만들어줘.
- 산업/카테고리: [___]
- 타겟 사용자: [나이대, 성향]
- 브랜드 톤: [___]
- 다크모드/라이트모드: [___]
- 스택: [___]
- 참고 브랜드/사이트: [___] (선택사항)

## 6. 실행 (GSD)
/gsd:plan-phase 1
/gsd:execute-phase 1
```

---

### 🗂️ Template 2: 기능 추가 템플릿

```markdown
# 📋 기능 추가 프롬프트

## 1. 기능 분석 (PM-Skills)
/brainstorm [ideas|experiments] [existing|new]
[현재 상황 설명]
[해결하려는 문제]
[가설]

## 2. PRD 작성 (PM-Skills)
/write-prd
[기능 이름]
- 배경: [왜 이 기능이 필요한지]
- 영향 범위: [어떤 기존 기능에 영향을 주는지]
- 핵심 유저 스토리:
  As a [___], I want to [___], so that [___]
- 수용 기준:
  - [ ] [기준 1]
  - [ ] [기준 2]
  - [ ] [기준 3]

## 3. Phase 논의 (GSD)
/gsd:discuss-phase [N]
[기능 설명]
관련 파일: [경로]
기존 아키텍처 고려사항: [___]

## 4. 실행 (GSD)
/gsd:plan-phase [N]
/gsd:execute-phase [N]

## 5. 검증 (GSD + PM-Skills)
/gsd:verify-work [N]
/sprint retro — [스프린트 노트]
```

---

### 🗂️ Template 3: 랜딩 페이지 빠른 생성 템플릿

```markdown
# 📋 랜딩 페이지 프롬프트

## 1. 가치 제안 (PM-Skills)
/value-proposition [프로덕트 이름]
- 누구를 위한 것: [___]
- 왜 필요한지: [___]
- 기존 대안: [___]

## 2. 디자인 + 구현 (UI-UX-Pro-Max)
[프로덕트 이름]의 랜딩 페이지를 만들어줘.

### 섹션 구성:
1. 히어로: [헤드라인] + [서브 카피] + [CTA 텍스트]
2. 문제 제기: [타겟의 페인포인트 3가지]
3. 솔루션: [핵심 기능 3-4개, 각각 아이콘+제목+설명]
4. 소셜 프루프: [후기/로고/숫자]
5. 가격: [플랜 비교표]
6. FAQ: [질문 5-7개]
7. CTA: [최종 전환 유도]

### 디자인 방향:
- 랜딩 페이지 패턴: [Hero-Centric | Conversion-Optimized | Social Proof-Focused | ...]
- 브랜드 톤: [___]
- 스택: [HTML+Tailwind | Next.js+shadcn | ...]

## 3. GTM 준비 (PM-Skills)
/plan-launch [프로덕트 이름]
- 런칭 채널: [___]
- 타겟 세그먼트: [___]
- 런칭 일정: [___]
```

---

### 🗂️ Template 4: 대시보드/앱 UI 설계 템플릿

```markdown
# 📋 대시보드/앱 UI 프롬프트

## 1. 지표 설계 (PM-Skills)
/north-star [프로덕트 이름]
- 비즈니스 모델: [___]
- 핵심 가치: [___]

/setup-metrics
- 핵심 지표: [___]
- 보조 지표: [___]
- 알림 임계값: [___]

## 2. 디자인 시스템 (UI-UX-Pro-Max)
[프로덕트 이름] [대시보드/앱]을 만들어줘.

### 화면 구성:
| 화면 | 핵심 요소 | 우선순위 |
|------|-----------|---------|
| [화면1] | [요소들] | P0 |
| [화면2] | [요소들] | P0 |
| [화면3] | [요소들] | P1 |

### 차트/시각화:
- [차트 유형 1]: [표현할 데이터]
- [차트 유형 2]: [표현할 데이터]

### 디자인 방향:
- 대시보드 스타일: [Executive | Data-Dense | Real-Time Monitoring | ...]
- 데이터 밀도: [높음 | 중간 | 낮음]
- 다크/라이트: [___]
- 스택: [___]

## 3. GSD 실행
/gsd:new-project (또는 /gsd:discuss-phase N)
→ /gsd:plan-phase N
→ /gsd:execute-phase N
→ /gsd:verify-work N
```

---

### 🗂️ Template 5: 스프린트 회고 & 다음 사이클 템플릿

```markdown
# 📋 스프린트 회고 & 계획 프롬프트

## 1. 작업 검증 (GSD)
/gsd:verify-work [N]

## 2. 회고 (PM-Skills)
/sprint retro
- 이번 스프린트 기간: [___]
- 완료한 것: [___]
- 못 한 것: [___]
- 잘 된 것: [___]
- 개선할 것: [___]

## 3. 데이터 분석 (PM-Skills)
/analyze-test [A/B 테스트 결과]
또는
/analyze-cohorts [코호트 데이터]

## 4. 다음 사이클 (GSD + PM-Skills)
/gsd:complete-milestone
/plan-okrs [다음 분기 OKR]
/transform-roadmap [현재 로드맵 → 성과 중심으로 변환]
```

---

## 🎁 보너스: "복사해서 바로 쓰는" 원샷 프롬프트

### 원샷 1: MVP 전체 파이프라인

```
나는 [프로덕트 이름]을 만들려고 해.

[프로덕트 설명 2-3문장]

이 프로젝트를 시작하기 위해 다음 순서로 진행해줘:

1. 먼저 /discover로 디스커버리 사이클을 돌려줘
2. 결과를 바탕으로 /write-prd로 PRD를 만들어줘
3. PRD 완성 후 /gsd:new-project로 프로젝트를 초기화해줘
4. 디자인 시스템을 생성하고 persist 해줘
5. /gsd:plan-phase 1으로 첫 번째 단계를 계획해줘

Tech Stack: [___]
타겟 사용자: [___]
핵심 차별점: [___]
```

### 원샷 2: 랜딩 페이지 올인원

```
[프로덕트 이름] 랜딩 페이지를 만들어줘.

프로덕트: [한 줄 설명]
타겟: [타겟 사용자]
톤: [브랜드 톤]
CTA: [전환 목표]

먼저 /value-proposition으로 가치 제안을 정리하고,
UI-UX-Pro-Max 디자인 시스템을 적용해서
[스택]으로 완성된 랜딩 페이지 코드를 생성해줘.

반드시 포함할 것:
- 반응형 (모바일 우선)
- 접근성 (WCAG AA)
- SEO 메타 태그
- 성능 최적화 (이미지 lazy loading)
```

### 원샷 3: 경쟁 분석 → 전략 → PRD

```
[시장/도메인]에서 새 프로덕트를 기획 중이야.

1. /competitive-analysis [주요 경쟁사 3개]로 경쟁 환경을 분석해줘
2. 분석 결과를 바탕으로 /strategy로 제품 전략을 수립해줘
3. 전략에서 도출된 핵심 기능으로 /write-prd를 만들어줘
4. /plan-launch로 GTM 전략도 함께 만들어줘

우리의 강점: [___]
예산 규모: [___]
런칭 목표일: [___]
```

---

## 🏁 마무리: 이 조합이 바꾸는 것

| Before (맨땅에 바이브코딩) | After (3종 조합) |
|---------------------------|------------------|
| "뭔가 만들어줘" → 횡설수설 | 구조화된 PRD → 정확한 구현 |
| 세션 넘기면 컨텍스트 소실 | `.planning/`으로 완벽한 상태 복구 |
| UI가 부트스트랩 기본 테마 | 산업별 맞춤 디자인 시스템 |
| 끝없는 수정 루프 | Phase별 계획→실행→검증 사이클 |
| 혼자 기획+개발+디자인 | AI PM + AI 아키텍트 + AI 디자이너 |

**GSD는 뼈대**, **PM-Skills는 두뇌**, **UI-UX-Pro-Max는 감각**입니다.

이 세 가지를 조합하면, 한 사람이 프로덕트 팀 전체의 역할을 수행할 수 있습니다. 바이브코딩의 미래는 "더 좋은 프롬프트"가 아니라 **"더 좋은 시스템"**에 있습니다.

---

*이 글이 도움이 되었다면, 각 프로젝트에 ⭐를 남겨주세요:*
- [GSD (Get Shit Done)](https://github.com/gsd-build/get-shit-done)
- [PM-Skills Marketplace](https://github.com/phuryn/pm-skills)
- [UI-UX-Pro-Max-Skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
