# Threads.net API 참고 문서

이 문서는 Threads.net 포스트를 크롤링하고 처리하는 데 필요한 API 및 웹 구조 정보를 제공합니다.

---

## URL 형식

### 기본 URL 구조

```
https://www.threads.com/@username/post/POST_ID
```

### 예시

- `https://www.threads.com/@choi.openai/post/DVQamrZj4vp`
- `https://www.threads.com/@anthropic/post/ClaudeOpus4`

### URL 파싱

```python
import re

def parse_threads_url(url):
    """Threads URL에서 사용자명과 포스트 ID 추출"""
    pattern = r'threads\.com/@([^/]+)/post/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return {
            'username': match.group(1),
            'post_id': match.group(2)
        }
    return None
```

---

## 포스트 구조

### Threads API 응답 형식 (공식 API 사용 가능 시)

```json
{
  "data": {
    "id": "DVQamrZj4vp",
    "text": "포스트 내용",
    "media_type": "image|video|carousel",
    "media_url": "https://...",
    "permalink": "https://www.threads.com/@username/post/DVQamrZj4vp",
    "timestamp": "2026-02-27T10:00:00Z",
    "author": {
      "username": "username",
      "name": "표시 이름"
    },
    "reply_to_id": "C-J3zK6JiH",
    "thread_items": [
      {
        "id": "DVQamrZj4vp",
        "text": "첫 번째 포스트",
        "media": [...]
      },
      {
        "id": "C-J3zK6JiH",
        "text": "두 번째 포스트 (연속)",
        "media": [...]
      }
    ]
  }
}
```

### 웹 스크래핑용 HTML 구조

```html
<!-- 포스트 콘텐츠 -->
<div class="x1i10hfl xjbqb8w">
  <div class="post-content">
    <span class="post-text">포스트 내용</span>
  </div>
</div>

<!-- 이미지 -->
<img src="https://scontent-xxx.cdninstagram.com/..." alt="...">

<!-- 비디오 -->
<video src="https://scontent-xxx.cdninstagram.com/...">
  <source type="video/mp4">
</video>
```

---

## 작성자 연속 포스트 필터링

### 로직

1. 첫 번째 포스트의 작성자 username 확인
2. 연속된 포스트 중 같은 username인 것만 수집
3. 다른 username이 나오면 중단 (댓글로 간주)

### 파이썬 구현

```python
def filter_authors_posts(thread_items):
    """첫 번째 작성자의 연속된 포스트만 추출"""
    if not thread_items:
        return []

    first_author = thread_items[0]['author']['username']
    result = []

    for item in thread_items:
        current_author = item['author']['username']
        if current_author == first_author:
            result.append(item)
        else:
            # 다른 작성자가 나오면 중단
            break

    return result
```

---

## 미디어 임베드

### 이미지

```markdown
![이미지 설명](이미지_URL)
```

### 비디오

Threads 비디오는 직접 임베드가 어려울 수 있음. 두 가지 옵션:

1. **링크로 제공**:
```markdown
[비디오 보기](비디오_URL)
```

2. **HTML 비디오 태그** (지원되는 플랫폼에서):
```html
<video width="600" controls>
  <source src="비디오_URL" type="video/mp4">
</video>
```

### 캐러셀 (여러 이미지)

```markdown
### 이미지 갤러리

1. ![첫 번째 이미지](URL1)
2. ![두 번째 이미지](URL2)
3. ![세 번째 이미지](URL3)
```

---

## API 접근 방법

### 옵션 1: Threads 공식 API (권장)

Meta 개발자 포털에서 앱 등록 필요:
- [Meta for Developers](https://developers.facebook.com/)
- Threads Graph API 사용
- OAuth 인증 필요

### 옵션 2: 웹 스크래핑 (백업)

```python
import requests
from bs4 import BeautifulSoup

def scrape_thread(url):
    """웹 스크래핑으로 포스트 데이터 추출"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; ThreadBot/1.0)'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 메타 데이터 추출
    title = soup.find('meta', property='og:title')
    description = soup.find('meta', property='og:description')
    image = soup.find('meta', property='og:image')

    return {
        'title': title.get('content') if title else None,
        'description': description.get('content') if description else None,
        'image': image.get('content') if image else None
    }
```

### 옵션 3: RapidAPI 등 제3자 API

- [Threads API on RapidAPI](https://rapidapi.com/)
- 유료이지만 구현이 간단

---

## Rate Limiting

```python
import time

def fetch_with_retry(url, max_retries=3):
    """재시도 로직이 포함된 fetch 함수"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 429:  # Too Many Requests
                wait_time = 2 ** attempt  # 지수 백오프
                time.sleep(wait_time)
                continue
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
    return None
```

---

## 에러 처리

### 일반적인 에러 상황

1. **URL이 유효하지 않음**: 404 에러
2. **포스트가 삭제됨**: 410 Gone 또는 리디렉션
3. **비공개 계정**: 인증 필요 또는 접근 거부
4. **Rate Limiting**: 429 Too Many Requests

### 에러 핸들링 예시

```python
def handle_fetch_error(url, error):
    """적절한 에러 메시지 반환"""
    if isinstance(error, requests.exceptions.HTTPError):
        if error.response.status_code == 404:
            return f"포스트를 찾을 수 없습니다: {url}"
        elif error.response.status_code == 429:
            return "요청이 너무 많습니다. 잠시 후 다시 시도해주세요."
    elif isinstance(error, requests.exceptions.ConnectionError):
        return "네트워크 연결 오류가 발생했습니다."
    return f"알 수 없는 오류가 발생했습니다: {str(error)}"
```

---

## 참고 링크

- [Threads Graph API 공식 문서](https://developers.facebook.com/docs/threads/)
- [Meta for Developers](https://developers.facebook.com/)
- [Threads Web](https://www.threads.net/)
