---
name: threads-blog-post
description: Threads.net 포스트를 블로그 글로 변환
version: 1.0.0
author: threads-glm
---

# Threads Blog Post 변환 스킬

## Purpose

이 스킬은 Threads.net에 공유된 포스트를 크롤링하여, 기술 블로그에 적합한 형식의 Markdown 문서로 자동 변환합니다. 개발자들이 SNS에 간단히 공유한 생각이나 코드 조각을 체계적인 블로그 포스트로 재가공하여 지식 베이스를 확장할 수 있도록 돕습니다.

### 왜 필요한가?

- **지식 보존**: SNS 포스트는 시간이 지나면 묻히지만, 블로그는 검색 가능한 지식이 됩니다
- **자동화**: 수동으로 복사-붙여넣기 하는 번거로움을 제거합니다
- **형식 표준화**: 일관된 기술 블로그 템플릿을 적용합니다
- **미디어 처리**: 첨부된 이미지를 자동으로 다운로드하고 블로그에 맞게 변환합니다

## When to Activate

이 스킬은 다음 상황에서 자동으로 활성화됩니다:

1. **URL 기반**: 사용자가 Threads.net URL을 입력하는 경우
   - 예: `https://www.threads.net/@username/post/...`
   - 예: `threads 블로그로 변환: https://threads.net/...`

2. **명시적 요청**: 다음 키워드를 포함하는 요청
   - "threads 블로그로 변환"
   - "threads 포스트 변환"
   - "threads 글 블로그화"

3. **스킬 직접 호출**: `/threads-blog-post <URL>` 명령어 사용

## Team Workflow

이 스킬은 3명의 전문화된 에이전트가 협력하여 작업을 완료합니다.

### 1. Fetcher Agent (크롤러)

**담당**: Threads URL에서 원본 콘텐츠 추출

- **agent-browser** 스킬을 사용하여 브라우저 자동화로 페이지 접근
- Threads.net 페이지를 크롤링하여 포스트 내용 수집
- 텍스트, 이미지, 작성자 정보, 작성일 추출
- Open Graph 메타데이터 및 JSON-LD 데이터 추출
- 인라인 코드/코드 블록 식별

**출력 형식**:
```json
{
  "url": "원본 Threads URL",
  "author": "작성자 이름",
  "handle": "@username",
  "content": "포스트 본문",
  "code_blocks": ["코드 블록 배열"],
  "images": ["이미지 URL 배열"],
  "created_at": "ISO 8601 날짜",
  "likes": 0,
  "replies": 0
}
```

### 2. Content Agent (콘텐츠 변환)

**담당**: 크롤링 데이터를 블로그 포스트로 변환

- 기술 블로그 스타일로 내용 재구성
- 한국어 자연스러운 문장으로 변환
- 마크다운 형식 적용
- SEO 친화적 제목 생성
- 요약, 태그 추천

**출력 형식**: 마크다운 블로그 포스트 (아래 템플릿 참조)

### 3. Media Agent (미디어 처리)

**담당**: 이미지 다운로드 및 변환

- 원격 이미지 로컬 다운로드
- 최적화 (크기 조정, WebP 변환)
- 블로그에 맞는 경로로 변환
- 대체 텍스트(alt text) 생성

**출력 형식**:
```markdown
![이미지 설명](/assets/images/threads/2025-02-27-filename.webp)
```

## Blog Post Template

모든 변환된 포스트는 다음 템플릿을 따릅니다:

```markdown
---
title: "자동 생성된 제목: 원래 내용 요약"
date: 2025-02-27
tags: [태그1, 태그2, 태그3]
category: 기술 노트
original_url: https://www.threads.net/@username/post/...
---

## 요약

원본 포스트의 핵심 내용을 2-3문장으로 요약합니다.

## 본문

변환된 포스트 내용이 여기에 위치합니다.
코드 블록, 인용, 강조 등이 적절히 적용됩니다.

```javascript
// 코드 예시
console.log('Hello Threads');
```

## 참고

- 원본: [Threads 포스트](https://www.threads.net/...)
- 작성일: 2025년 2월 27일
```

## Configuration

### 출력 언어

모든 출력은 **한국어**로 생성됩니다. 영문 포스트라도 한국어 설명과 함께 제공됩니다.

### 블로그 스타일

- **기술 블로그**: 개발/기술 중심의 전문적인 톤
- **친근함**: 전문적이지만 읽기 쉬운 문체
- **구조화**: 명확한 섹션 구분

## Usage Example

```bash
# URL로 호출
/threads-blog-post https://www.threads.net/@dev/post/...

# 자연어 호출
threads 블로그로 변환해줘: https://threads.net/@username/post/...
```

## Output Files

- `{date}-{slug}.md`: 생성된 블로그 포스트
- `assets/images/threads/{date}-{filename}.webp`: 다운로드된 이미지

## Agent Coordination

1. **Skill Lead** → Fetcher에게 URL 전달
2. **Fetcher** → 원본 데이터 반환
3. **Skill Lead** → Content, Media에게 데이터 병렬 전달
4. **Content** → 마크다운 포스트 생성
5. **Media** → 이미지 처리 완료
6. **Skill Lead** → 최종 파일 병합 및 저장

## Error Handling

- **비공개 포스트**: 접근 권한 없음 알림
- **삭제된 포스트**: 404 처리 및 사용자 안내
- **이미지 다운로드 실패**: 대체 텍스트로 대체
- **파싱 오류**: 원본 HTML 보존 및 수동 편집 요청
