---
title: Python의 uv 패키지 매니저
date: 2025-05-06T21:35:29+09:00
draft: true
categories:
  - utillity
tags:
  - obsidian
  - application
---

Obsidian을 쓰다 보면, 쫍은 편집창의 폭 때문에 불편 할 수 있습니다.

편집창의 넓이를 방법을 소개 합니다.


Obsidian의 설정 → 외관 → CSS 스니펫에서 커스텀 CSS를 추가하여 편집창의 넓이를 조절할 수 있습니다.

css 파일의 이름은 원하는 이름으로 설정 후, 아래와 같이 입력 해 줍니다.
```css
.markdown-source-view {
  --file-line-width: 900px; /* 기본값은 보통 700px 정도입니다 */
}

/* 또는 전체 콘텐츠 영역의 최대 너비를 설정할 수도 있습니다 */
.markdown-preview-view {
  --file-line-width: 900px;
}
```
이 값을 더 크게 설정하면 편집창의 넓이가 더 넓어집니다.

편집을 완료 하면, css 파일이 목록에 나옵니다.
옆에 체크 박스를 켜주면, css가 적용 됩니다

