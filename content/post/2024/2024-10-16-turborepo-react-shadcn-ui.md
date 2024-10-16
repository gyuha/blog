---
title: "Turborepo를 이용해서 React Shadcn-ui 적용하기"
date: 2024-10-16T17:53:01+09:00
draft: true
categories: [React]
tags: ["react", "turborepo", "shadcn-ui"]
---

Turborepo를 Vite 및 shadcn-ui와 함께 사용하는 설정은 여러 프로젝트나 패키지를 효율적으로 관리할 수 있는 강력한 방법입니다. 
<!--more-->
아래는 이 스택을 처음부터 설정하는 데 도움이 되는 단계별 가이드입니다.

## 목차

- [목차](#목차)
- [1. 필수 사항](#1-필수-사항)
- [2. Turborepo 초기화](#2-turborepo-초기화)
- [3. Vite 및 shadcn-ui로 프론트엔드 설정](#3-vite-및-shadcn-ui로-프론트엔드-설정)
  - [a. 프론트엔드 패키지 생성](#a-프론트엔드-패키지-생성)
  - [b. 종속성 설치](#b-종속성-설치)
  - [c. shadcn-ui 및 Tailwind CSS 설치](#c-shadcn-ui-및-tailwind-css-설치)
  - [d. Tailwind CSS 구성](#d-tailwind-css-구성)
  - [e. shadcn-ui 컴포넌트 통합](#e-shadcn-ui-컴포넌트-통합)
- [4. Turborepo 구성](#4-turborepo-구성)
- [5. 스크립트 및 종속성 추가](#5-스크립트-및-종속성-추가)
- [6. 공유 패키지 생성 (선택 사항)](#6-공유-패키지-생성-선택-사항)
- [7. 모노레포 실행](#7-모노레포-실행)
  - [a. 개발 서버 시작](#a-개발-서버-시작)
  - [b. 모든 패키지 빌드](#b-모든-패키지-빌드)
  - [c. 린팅 및 테스트](#c-린팅-및-테스트)
- [8. 추가 팁](#8-추가-팁)

---

## 1. 필수 사항

시작하기 전에 다음이 설치되어 있는지 확인하세요:

- **Node.js** (v14 이상)
- **npm** 또는 **yarn**
- **Git** (선택 사항이지만 권장됨)

## 2. Turborepo 초기화

먼저, 새로운 Turborepo를 설정합니다. `create-turbo`를 사용하여 시작 템플릿을 생성할 수 있습니다.

```bash
npx create-turbo@latest
```

프롬프트에 따라 저장소 이름을 지정하고 구성을 선택하세요. 또는 수동으로 저장소를 설정할 수 있습니다:

```bash
mkdir my-monorepo
cd my-monorepo
git init
npm init -y
```

Turborepo를 개발 종속성으로 설치합니다:

```bash
npm install turbo --save-dev
```

루트 디렉토리에 `turbo.json` 구성 파일을 추가합니다:

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "dev": {
      "cache": false
    },
    "lint": {
      "outputs": []
    },
    "test": {
      "outputs": ["coverage/**"]
    }
  }
}
```

## 3. Vite 및 shadcn-ui로 프론트엔드 설정

다음으로, Vite를 사용하여 프론트엔드 애플리케이션을 생성하고 shadcn-ui를 통합합니다.

### a. 프론트엔드 패키지 생성

`packages` 디렉토리에 앱과 패키지를 두는 구조를 가정합니다:

```bash
mkdir -p packages/frontend
cd packages/frontend
```

새로운 Vite 프로젝트를 초기화합니다. shadcn-ui와 호환성을 위해 `react` 템플릿을 선택할 수 있습니다.

npm을 사용하는 경우:

```bash
npm create vite@latest . -- --template react
```

또는 Yarn을 사용하는 경우:

```bash
yarn create vite . --template react
```

### b. 종속성 설치

루트 디렉토리로 돌아가 필요한 종속성을 설치합니다:

```bash
cd ../../
npm install
```

### c. shadcn-ui 및 Tailwind CSS 설치

`shadcn-ui`, Tailwind CSS 및 관련 종속성을 설치합니다:

```bash
cd packages/frontend
npm install shadcn-ui tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### d. Tailwind CSS 구성

`tailwind.config.js`를 편집하여 컴포넌트 경로를 포함시킵니다:

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    // 필요한 경우 shadcn-ui 경로 추가
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('shadcn-ui/plugin'), // 필요 시 shadcn-ui 플러그인 추가
  ],
};
```

### e. shadcn-ui 컴포넌트 통합

이제 React 애플리케이션에서 shadcn-ui 컴포넌트를 사용할 수 있습니다.

예를 들어, `src/App.jsx`에서:

```jsx
import React from 'react';
import { Button } from 'shadcn-ui';

function App() {
  return (
    <div className="App">
      <Button>Click Me</Button>
    </div>
  );
}

export default App;
```

shadcn-ui의 공식 문서([shadcn-ui documentation](https://shadcn.com/docs/installation))에서 추가 설정 지침을 따라 컴포넌트 라이브러리를 완전히 통합하세요.

## 4. Turborepo 구성

Turborepo가 프론트엔드 패키지를 인식하는지 확인합니다. 모노레포 구조는 다음과 같아야 합니다:

```
my-monorepo/
├── packages/
│   └── frontend/
│       ├── node_modules/
│       ├── src/
│       ├── package.json
│       ├── tailwind.config.js
│       └── ...
├── package.json
├── turbo.json
└── ...
```

다른 패키지나 앱이 있다면 `packages` 디렉토리 안에 배치하세요.

## 5. 스크립트 및 종속성 추가

개발을 원활하게 진행하기 위해 루트 `package.json`에 모노레포 전체에서 작업을 실행할 수 있는 스크립트를 추가합니다.

```json
// package.json
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": [
    "packages/*"
  ],
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "lint": "turbo run lint",
    "test": "turbo run test"
  },
  "devDependencies": {
    "turbo": "^1.0.0"
  }
}
```

각 패키지(예: `frontend`)에 자체 `dev`, `build`, `lint`, `test` 스크립트가 `package.json`에 정의되어 있는지 확인하세요.

예를 들어, `packages/frontend/package.json`에서는:

```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "test": "jest"
  },
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "shadcn-ui": "^1.0.0",
    "vite": "^4.0.0",
    "tailwindcss": "^3.0.0"
  },
  "devDependencies": {
    "autoprefixer": "^10.0.0",
    "postcss": "^8.0.0"
  }
}
```

필요에 따라 버전을 조정하세요.

## 6. 공유 패키지 생성 (선택 사항)

공유 코드나 컴포넌트가 있는 경우, `packages` 디렉토리 내에 추가 패키지를 생성할 수 있습니다.

예를 들어, `ui` 패키지를 생성합니다:

```bash
mkdir -p packages/ui
cd packages/ui
npm init -y
```

필요한 종속성을 설치하고 공유 컴포넌트를 설정합니다. `package.json`을 적절히 업데이트하고 워크스페이스를 통해 종속성이 올바르게 연결되었는지 확인하세요.

## 7. 모노레포 실행

모노레포의 루트 디렉토리에서 개발 서버, 빌드 프로세스, 린팅 및 테스트를 모든 패키지에서 실행할 수 있습니다.

### a. 개발 서버 시작

```bash
npm run dev
```

이 명령은 Turborepo 덕분에 모든 패키지의 `dev` 스크립트를 병렬로 실행합니다.

### b. 모든 패키지 빌드

```bash
npm run build
```

Turborepo는 `turbo.json`을 기반으로 빌드 파이프라인을 처리하며, 종속성에 따라 올바른 순서로 작업이 실행되도록 합니다.

### c. 린팅 및 테스트

마찬가지로, 모든 패키지에서 린팅과 테스트를 실행할 수 있습니다:

```bash
npm run lint
npm run test
```

## 8. 추가 팁

- **캐싱 및 성능**: Turborepo는 빌드 출력을 지능적으로 캐싱하여 이후 실행 속도를 높입니다. `turbo.json`이 제대로 구성되어 있는지 확인하여 이를 최대한 활용하세요.
  
- **환경 변수**: 루트 또는 각 패키지별로 환경 변수를 관리하세요. [dotenv](https://github.com/motdotla/dotenv) 같은 도구가 도움이 될 수 있습니다.
  
- **버전 관리**: Git을 사용하여 모노레포를 관리하세요. 루트와 패키지 수준에서 `node_modules`를 무시하면 불필요한 용량 증가를 방지할 수 있습니다.
  
- **CI/CD 통합**: Turborepo는 CI/CD 파이프라인과 잘 작동합니다. 캐싱을 활용하여 빌드를 더 빠르게 설정하세요.
  
- **TypeScript 지원**: TypeScript를 사용하는 경우, 공유 패키지에 대한 경로 매핑과 함께 `tsconfig.json`이 제대로 설정되었는지 확인하세요.
  
- **ESLint 및 Prettier**: 루트에 ESLint와 Prettier를 설정하고 패키지에서는 설정을 확장하여 코드 스타일을 표준화하세요.

---

이 단계를 따르면 Turborepo, Vite 및 shadcn-ui를 사용하는 견고한 모노레포 설정을 갖추게 되어 개발 효율성과 확장성을 높일 수 있습니다.

문제가 발생하거나 더 고급 구성이 필요한 경우, 공식 문서를 참조하세요:

- [Turborepo 문서](https://turbo.build/docs)
- [Vite 문서](https://vitejs.dev/guide/)
- [shadcn-ui 문서](https://shadcn.com/docs/introduction)