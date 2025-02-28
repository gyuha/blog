---
title: "SVG 아이콘의 인덱스 파일을 생성하는 Vite 플러그인"
date: 2025-02-28T09:15:19+09:00
draft: true
categories: [React]
tags: [svg, react, typescript, vite]
---

SVG 아이콘 폴더를 모니터링하고 자동으로 index.ts 파일을 생성하는 Vite 플러그인입니다.
<!--more-->
이 플러그인은 웹사이트의 기능을 확장하고 관리 효율성을 높이기 위해 필요합니다. 사용자가 원하는 특정 기능들을 쉽게 추가할 수 있도록 도와주며, 설치 후에는 사용자 친화적인 인터페이스를 통해 간편하게 설정 및 활용할 수 있습니다. 특히 svgr을 사용하면 ?react가 붙은 URL을 일일이 import할 필요 없이 손쉽게 SVG 아이콘을 import할 수 있어 매우 유용합니다. 이러한 편리함 덕분에 개발자는 더욱 빠르고 효과적으로 사이트를 개발을 할 수 있습니다.

## 설치. 
```bash
npm install vite-plugin-svgr vite-plugin-svgr-indexer --save-dev
# 또는
yarn add vite-plugin-svgr vite-plugin-svgr-indexer -D
# 또는
pnpm add vite-plugin-svgr vite-plugin-svgr-indexer -D
```

## 사용 방법
```js
// vite.config.js / vite.config.ts
import { defineConfig } from 'vite';
import svgr from 'vite-plugin-svgr';
import svgrIndexer from 'vite-plugin-svgr-indexer';
export default defineConfig({
  plugins: [
    svgr(), // 먼저 vite-plugin-svgr 구성
    svgrIndexer({
      // 모니터링할 SVG 아이콘 디렉토리 경로 (필수)
      iconDirs: ['src/assets/icons'],
      // 생성할 인덱스 파일 이름 (기본값: 'index.ts')
      indexFileName: 'index.ts',
      // 파일 감시 활성화 (기본값: true)
      watch: true,
      // 하위 폴더 감시 활성화 (기본값: true)
      recursive: true,
      // 컴포넌트 이름에 추가할 접두사 (기본값: '')
      componentPrefix: 'Icon'
    }),
  ],
});
```

## TypeScript 지원
TypeScript를 사용하는 경우 tsconfig.json에 다음을 추가하세요:
```json
{
  "compilerOptions": {
    "types": ["vite-plugin-svgr/client"]
  }
}
```
또는 더 나은 타입 추론을 위한 선언 도우미도 있습니다. vite-env.d.ts에 다음을 추가하세요:

```
/// <reference types="vite-plugin-svgr/client" />
```

이렇게 하면 SVG 임포트에 대한 적절한 타입 정의가 제공됩니다.

## 기능
- 지정된 디렉토리의 SVG 파일을 모니터링합니다.
- SVG 파일이 추가, 삭제 또는 수정될 때 자동으로 index.ts 파일을 생성합니다.
- 생성된 index.ts 파일은 모든 SVG 파일을 React 컴포넌트로 가져와서 내보냅니다.
- 각 하위 디렉토리에 대한 별도의 index.ts 파일을 생성하여 해당 디렉토리의 SVG 파일만 가져옵니다.
- 컴포넌트 이름에 접두사 추가를 지원합니다 (예: `Icon` 접두사: `arrow.svg` → `IconArrow`).

## 예시
SVG 파일 구조:

```
src/assets/icons/
  ├── arrow.svg
  ├── close.svg
  ├── menu.svg
  └── navigation/
      ├── back.svg
      └── forward.svg
```

메인 디렉토리에 생성된 index.ts:

```typescript
import IconArrow from './arrow.svg?react';
import IconClose from './close.svg?react';
import IconMenu from './menu.svg?react';
export {
  IconArrow,
  IconClose,
  IconMenu
};
```

navigation 하위 디렉토리에 생성된 index.ts:

```typescript
import IconBack from './back.svg?react';
import IconForward from './forward.svg?react';
export {
  IconBack,
  IconForward
};
```

React 컴포넌트에서의 사용법

```tsx
// 메인 디렉토리에서 가져오기
import { IconClose, IconMenu } from './assets/icons';
// 하위 디렉토리에서 가져오기
import { IconBack } from './assets/icons/navigation';
function App() {
  return (
    <div>
      <IconClose />
      <IconMenu />
      <IconBack />
    </div>
  );
}
```
