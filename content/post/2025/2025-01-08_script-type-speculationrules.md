---
title: "Speculation Rules 사이트 로딩 속도 개선하기"
date: 2025-01-08T11:13:22+09:00
draft: true
categories: [web]
tags: [html, javascript]
---

웹 성능은 사용자 경험(UX)을 결정짓는 핵심 요소 중 하나입니다. 사용자가 페이지에서 다른 페이지로 이동할 때 추가적인 로딩 지연 없이 빠르게 전환할 수 있다면, 더 높은 만족도가 보장됩니다.  
<!--more-->

구글 크롬을 중심으로 제안된 Speculation Rules는 브라우저가 사용자 행동을 예상하여 사전에 리소스를 로드해 두는 새로운 방식으로, 향상된 UX를 제공합니다.  

이번 글에서는 보다 자세하게 Speculation Rules의 개념과 활용 방법, 주의 사항 등을 단계별로 살펴보겠습니다.

## 1. Speculation Rules란?
Speculation Rules는 브라우저가 미래에 사용자가 페이지나 리소스를 요청할 가능성이 높다고 판단되는 경우, 해당 리소스를 미리 가져오거나(prefetch) 심지어 완전히 렌더링(prerender)하여 준비해 두는 기술입니다.  
대표적인 예로, 사용자가 A 페이지에서 B 페이지로 이동할 것이 거의 확실한 상황에서는 브라우저가 B 페이지를 사전에 로드해둡니다. 사용자가 실제로 B 페이지를 클릭하는 시점에는 이미 모든 데이터가 준비되어 있어, 즉시 표시가 가능합니다.

### 기존 기법과 차이점

- **Resource Hint (prefetch, preload)**  
  HTML <link rel="prefetch"> 같은 리소스 힌트(Resource Hint)는 요청을 미리 가져오도록 브라우저에 알리는 역할을 합니다. 다만, 개별 리소스 단위로 적용하고, 더 세밀한 제어는 어렵습니다.
- **Speculation Rules**  

  JSON 형태의 규칙 집합을 통해 브라우저가 보다 총체적(페이 로드 단위)인 관점에서 ‘이러이러한 상황에서 해당 페이지(혹은 리소스)를 미리 로드하라’고 명시합니다.  
  자바스크립트와 DOM에서 얻은 정보를 기반으로 클릭 가능성 등을 종합적으로 분석하므로, 더 정교한 사전 로드가 가능합니다.

## 2. \<script type="speculationrules"\> 개요

Speculation Rules는 다음과 같은 형태로 작성합니다:

```html
<script type="speculationrules">
{
  "prefetch": [
    {
      "source": "list",
      "urls": [
        "/users",
        "/info"
      ]
    }
  ],
  "prerender": [
    {
      "source": "list",
      "urls": [
        "/main"
      ]
    }
  ]
}
</script>
```
- **`type="speculationrules"`**: JSON 형식의 규칙을 가진 스크립트 파일임을 브라우저에게 알림  
- **prefetch**: 브라우저가 리소스를 미리 가져오기만 하고, 렌더링은 하지 않음  
- **prerender**: 브라우저가 페이지를 뒤에서 완전히 렌더링까지 완료해 둠  

### JSON 구조 설명
- **prefetch**: 해당 리소스를 미리 다운로드하여 네트워크 지연을 최소화 (렌더링은 하지 않음)  
- **prerender**: 페이지 전체를 미리 불러온 뒤 메모리에 로드된 상태로 대기시켜, 사용자가 이동할 때 즉각적으로 표시  
- **source**: `"list"` 외에 `"document"` 등 다양한 타입이 있을 수 있으며, 이 값에 따라 브라우저가 어떤 방식으로 URL을 해석할지 결정  
- **urls**: 실제로 미리 처리할 대상 URL 배열  
- **eagerness**: 브라우저가 Speculation Rules를 얼마나 공격적으로 적용할지를 설정 (예: `"conservative"`, `"eager"`)  

## 3. Speculation Rules 동작 원리
1. **브라우저 파싱**  
   브라우저가 HTML 문서를 파싱하며 speculationrules 스크립트를 만나면, 내부의 JSON을 분석합니다.  

1. **규칙 적용**  
   JSON의 prefetch, prerender, eagerness 설정에 따라 해당 URL들을 우선순위 큐에 등록합니다.  

1. **사전 로드(조건부)**  
    - 브라우저는 네트워크 상황, 메모리 상황, CPU 리소스 등을 고려하여 과도한 사전 로드를 막으려 할 수 있습니다.  
    - 사용자가 예상 경로를 벗어날 경우에는 해당 사전 로드가 무의미할 수 있음.  

1. **UX 개선**  
   실제로 사용자가 사전에 로드된 리소스나 페이지를 요청하면, 이미 브라우저 캐싱 또는 메모리에 준비된 상태이므로 지연 시간이 거의 들지 않습니다.
1. Speculation Rules 설정 옵션
###  prerender 옵션
```json
{
  "prerender": [
    {
      "source": "list",
      "urls": [
        "https://example.com/next-page"
      ]
    }
  ]
}
```
- **`source: "list"`**: 단순히 사전에 선언한 URL만을 prerender 대상으로 지정  
- **활용 상황**: 다음 단계로 넘어갈 URL을 이미 파악하고 있거나, ‘다음 버튼’과 같이 사용자가 누를 확률이 매우 높은 경우

### prefetch 옵션
```json
{
  "prefetch": [
    {
      "source": "list",
      "urls": [
        "https://example.com/assets/images/banner.jpg"
      ]
    }
  ]
}
```
- **`prefetch`**: 큰 이미지, JS, CSS 파일 등 다음 페이지 로딩에 필요한 리소스를 미리 다운받아 둘 때 사용  
- **주의점**: 너무 많은 리소스를 무분별하게 prefetch하면, 자원 낭비와 네트워크 혼잡이 발생할 수 있음

### eagerness 옵션
- **`eagerness`**: 이 옵션은 사전 로드의 “공격성”을 조절하며, 주요 값은 다음과 같습니다:  
  - `"immediate"` : 프리패치와 프리랜더를 가능한 한 빠르게 가져옴
  - `"conservative"`: 리소스 소모를 최소화하며 신중하게 처리 (예: 마우스다운, 포인터다운) 
  - `"eager"`: 보다 공격적으로 사전 로드를 수행, 더 많은 자원을 사용 가능 (예: 마우스 커서 오버, 스크롤 시 화면 노출 후 중단)
  - `"moderate"` : eager와 conservative 사이 값. (예: 스크롤 시 화면 노출 후 마우스 커서 이동)
- **활용 상황**: 사용자 경험이 특히 중요한 경우 `"eager"`를 사용할 수 있지만, 장치 성능과 네트워크 상황을 고려해야 합니다.

## 5. Speculation Rules의 장점과 단점
### 장점
1. **빠른 페이지 전환**  
  - 사용자가 이동할 가능성이 높은 페이지를 미리 랜더링해 둔다면, *즉각적인 반응성*을 제공할 수 있습니다.
2. **정교한 제어**  
  - JSON 형태의 설정을 통해 어떤 리소스를 얼마만큼 사전에 불러올지 세부적으로 결정할 수 있습니다.
3. **향상된 UX**  
  - 페이지 전환 시 대기 시간이 현저히 감소해 사용자 만족도 상승

### 단점
1. **호환성 이슈**  
  - 모든 브라우저가 지원하지 않습니다. 크롬이 먼저 도입했으며, 다른 브라우저는 도입 계획이 다릅니다.
2. **과도한 리소스 낭비**  
  - 예측이 빗나갔을 때 불필요한 리소스를 미리 로드해 네트워크 트래픽과 메모리 사용량이 증가할 수 있습니다.
3. **보안, 개인정보 문제**  
  - 사전 로딩 시 쿠키나 인증 데이터가 의도치 않게 전송될 수 있습니다. 민감 정보가 없는 리소스 위주로 시도하는 것이 좋습니다.

## 6. 브라우저 호환성과 주의 사항
Speculation Rules는 아직 크롬 계열 브라우저 중심으로만 비교적 실험적으로 지원됩니다.  
따라서 프로덕션 환경에서 전면적으로 적용하기보다는, 아래와 같은 단계를 거치는 것이 좋습니다:

1. **Feature Detection**  
    - 사용자 브라우저가 Speculation Rules를 지원하는지 판별하고, 미지원 시 기존 방식(예: `rel="prefetch"`)으로 대체
2. **점진적 적용 (Progressive Enhancement)**  
    - 일부분의 페이지나 리소스에서 먼저 Speculation Rules를 적용해 효과를 측정
3. **효과 측정 & 모니터링**  
    - 실제 페이지 전환 속도, 사용자 이동 경로, 리소스 사용량 등을 분석해 Speculation Rules의 효용성을 확인

## 7. 사용 예시
```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <title>Speculation Rules Demo</title>
</head>
<body>
  <h1>Speculation Rules 테스트</h1>
  <p>
    아래 버튼을 누르면 다음 페이지로 이동합니다. 다만, 사전에 페이지를
    미리 렌더링해 두어, 클릭 즉시 새 페이지가 뜰 것입니다.
  </p>
  <button onclick="location.href='next.html'">다음 페이지로 이동</button>
  <!-- Speculation Rules Script -->
  <script type="speculationrules">
  {
    "prerender": [
      {
        "source": "list",
        "urls": ["https://example.com/next.html"]
      }
    ],
    "prefetch": [
      {
        "source": "list",
        "urls": [
          "/users",
          "/info"
        ]
      }
    ],
    "eagerness": "eager"
  }
  </script>
</body>
</html>
```
위 예시는 다음 페이지 next.html을 미리 렌더링(prerender) 해 두고, 필요한 JS/CSS 파일은 미리 다운로드(prefetch)하며, eagerness를 "eager"로 설정해 보다 적극적으로 자원을 활용하도록 설정합니다.

## 8. 문서가 prerendering인지 확인하는 방법

문서의 통계를 위해서 자바스크립트가 실행을 제한 해야 할 경우가 있을 수도 있습니다.
이런 경우에는 아래와 같은 스크립트를 통해서 제어가 가능 합니다.

```javascript
if (document.prerendering) {
  document.addEventListener("prerenderingchange", main, { once: true });
} else {
  main();
}
function main() {
  setTimeout(() => {
    document.body.append("Timeout Finished");
  }, 1000);
}
```

## 9. 참고
- [MDN: Resource Hint 사양](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel/prefetch)  
- [MDN: Speculation Rules 사양](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script/type/speculationrules)  
- [YouTube: Speculation Rules 소개](https://www.youtube.com/watch?v=LEF4UaM5m4U)
- [How to Use Speculation Rules API to Load Web Pages Instantly](https://uxify.com/blog/post/speculation-rules-api)