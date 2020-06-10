---
title: "Typescript를 사용한 Express 프로젝트 설정하기(with Eslint)"
date: 2020-06-10T23:36:41+09:00
draft: true
categories: [typescript]
tags: [express,typescript,node]
---

vscode에서 typescript를 사용한 express 프로젝트를 시작 하면서 설정하는 기본적인 작업을 정리해 봅니다.

<!--more-->   

## VSCode의 설치 할 확장 프로그램

우선 VSCode에 `ESLint`와 `Prettier`를 설치해 줍니다.

- `ESLint` : https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint
- `Prettier` : https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode

`ESLint`는 자바스크립트 코드의 문법적인 오류나 안티 패턴을 찾아주고 일관된 코드 스타일을 작성하도록 도와줍니다. 원래는 `TSLint`라고 해서 타입스크립트용 Lint가 별도로 있었지만, 작년(2019)부터  `ESLint`로 통합되서 운영하게 되었습니다. 

`Prettier`는 정해진 규칙에 따라서 자동으로 코드를 수정/정리해 주는 도구 입니다. 다양한 언어를 지원하고 있습니다.



## Express 기본 설정하기

먼저 `npm init`을 통해서 `package.json`파일을 만들어 줍니다.

```bash
npm init -y
```

그리고 express를 설치해 줍니다.

```bash
npm install express
```

설치가 완료 되면 `typescript`와 `@types/express`를 설치해 줍니다.

```bash
npm install --save-dev typescript @types/express
```

`@types`로 시작하는 패키지를 타입스크립트에서 자료형을 설정해 둔 패키지로 소스코드에서 타입을 검사하고, vscode에서 자동 완성 할 때 도움이 됩니다.

`./src` 폴더를 만들고 `app.ts` 파일을 만들어서 아래와 같이 입력해 주세요.

`./src/app.ts` 

```typescript
import * as express from 'express';
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req: express.Request, res: express.Response) => {
  res.send('Hello World!');
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}!`);
});
```



`ts-node-dev`를 설치해 줍니다.  

```bash
npm install -D ts-node-dev
```

`ts-node-dev` 는 `ts-node`와 흡사해서 `.ts`을 자바스크립트 파일을 컴파일 하지 않고도 바로 실행 할 수 있도록 해 줍니다. 그리고 추가로 파일이 변경 되었을 경우 다시 실행 하는 기능과 `inspect`를 통해서 디버깅을 할 수 있도록 도와 줍니다.

그러면 파일을 실행하기 위해서, `package.json` 파일의 `scripts` 부분에 아래와 같이 추가해 줍니다.

```json
{
  // ...
  "scripts": {
    "dev": "ts-node-dev --inspect --watch -- ./src/app.ts"
  },
  //...
}
```

- `--inspect` : vscode에서 디버깅 할 때 사용 됩니다.
- `--watch` : 소스 코드를 수정하면 다시 로드해 줍니다.
- `--` : 뒤에 실행할 파일을 넣어 줍니다. 앞 쪽에 옵션이 들어가 있을경우 사용합니다.



위와 같이 실행 환경이 설정 되면 아래와 같이 실행을 해 주시면 됩니다.

```bash
npm run dev
```



웹 브라우저에서 `http://127.0.0.1:3000` 주소로 접속해서 정상적으로 접속이 되는지 확인 합니다.



## tsconfig.json 파일 설정하기

타입스크립트를 프로젝트에서 사용하기 위해서는 `tsconfig.json`라는 파일을 통해서 타입스크립트 설정을 해 줘야 합니다.  직접 파일을 생성해서 넣어 줄 수도 있겠지만 `tsc` 명령어를 통해서 설정을 할 수도 있습니다.

```bash
npx tsc --init
```

`tsconfig.json` 파일의 대부분의 스펙이 들어 있습니다. 간단하게 `express`만 사용하려면 아래와 같은 정도만 설정을 하시면 됩니다.

`tsconfig.json` 

```json
{
  "compilerOptions": {
    "target": "es5",		/* 컴파일 후 생성될 파일의 ECMAScript 버전 */
    "module": "commonjs",	/* 컴파일 후 생성될 파일이 사용하는 모듈 버전 */
    "outDir": "dist/",		/* 파일이 생성될 폴더 */
    "esModuleInterop": true	/* 'require'와 'import' 호환 */
  },
  "include": ["src/*.ts"]	/* 사용할 폴더 및 파일 */
}
```

하지만, 이것저것 다른 패키지와 타입스크립트의 데코레이션 기능등을 사용 하시려면 아래와 같이 설정하시길 추천 듭니다.

`tsconfig.json`

```json
{
  "compilerOptions": {
    "lib": ["es2016","esnext.asynciterable"], /* 컴파일에 포함될 라이브러리 */
    "types": ["node"], /* 타입 정의가 포함될 이름의 목록 */
    "target": "es2016", /* 타겟의 ECMASCript 버전 */
    "module": "commonjs", /* 모듈 코드 생성 지정 */
    "moduleResolution": "node", /* 모듈 해석 방법 */
    "outDir": "./dist", /* 결과물 디렉토리 */
    "strict": true, /* 엄격한 타입 검사 옵션 활성화 */
    "emitDecoratorMetadata": true, /* 소스에 데코레이터 선언에 대한 설계-타입 메타 데이터를 보냄 */
    "experimentalDecorators": true, /* ES 데코레이터에  활성화 */
    "sourceMap": true,  /* 소스맵 사용 */
    "allowSyntheticDefaultImports": true, /* default export가 없는 모듈에서 default imports를 허용 */
    "esModuleInterop": true, /* 'require'와 'import' 호환 */
    "skipLibCheck": true, /* 모든 선언 파일(*.d.ts)의 타입 검사 생략 */
    "resolveJsonModule": true, /* .json 확장자로 import된 모듈을 포함 */
  },
  "include": [
    "./src/**/*",
  ],
  "exclude": [
    "node_modules",
    "src/test",
    "**/*.spec.ts",
    "**/*.test.ts",
  ]
}
```



이렇게 설정까지 설정을 하시고 `tsc`를 실행 하시면 `dist`폴더에 소스가 컴파일 되서 실행 되는걸 확인 할 수 있습니다.

```bash
npx tsc
```





## VSCode 디버깅 설정

`.vscode` 폴더가 없다면 폴더를 생성하고 `./.vscode/launch.json`파일을 아래와 같이 입력해 줍니다.

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Launch Program",
      "program": "${workspaceFolder}/src/app.ts",
      "preLaunchTask": "npm: build",
      "env": {
        "SRC_PATH": "dist/"
      },
      "sourceMaps": true,
      "smartStep": true,
      "internalConsoleOptions": "openOnSessionStart",
      "outFiles": [
        "${workspaceFolder}/dist/**/*.js"
      ]
    },
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to Inspector",
      "protocol": "inspector",
      "port": 9229,
      "cwd": "${workspaceRoot}"
    }
  ]
}                       
```



이제 브레이크 포인트를 걸고 싶은 행 앞을 클릭하거나 `F9`키를 누르면 행 앞에 빨간색 원이 생깁니다.

![디버깅 설정](/img/2020-06-10-express-typescript-eslint/Code_bE0dJpgBKJ.png)

이게 왼쪽의 디버그메뉴를 선택하거나 `Ctrl+Shift+D`키를 눌러서 디버그 메뉴로 이동하고 `Launch Program`을 선택하고 `F5` 버턴을 누르면 설정했던 중단점에 로직이 가게 되면 프로그램이 중단되면서 프로그램의 상태를 확인 할 수 있게 됩니다.



또는 터미널에서 `npm run dev`로  프로그램을 실행 후 디버그 메뉴에서 `Attach to Inspector`를 선택하고 `F5`를 누르면 일일히 실행하지 않고도 중간 부터 디버깅을 하실 수 있게 됩니다. 





## ESLint 설정

이제 ESLint를 설정해 줄 차례입니다. 먼저 `eslint`를  아래와 같이 설치해 줍니다. 

```bash
npm install --save-dev eslint
```

그리고 `eslint --init`을 통해서 기본 설정을 해 줍니다.

```bash
npx eslint --init
```



![디버깅 설정](/img/2020-06-10-express-typescript-eslint/Code_NKDX3QtoO4.png)

전 위 그림과 같이 설정을 했습니다.

위와 같이 선택을 한 경우에는 `@typescript-eslint/eslint-plugin`와  `@typescript-eslint/parser` 패키지가 자동으로 설치가 됩니다.



## Prettier 설정

`prettier`에 사용될 패키지를 아래와 같이 설채해 줍니다.

```bash
npm install --save-dev prettier eslint-config-prettier eslint-plugin-prettier
```

그리고 `prettier`의 설정 파일인 `.prettierrc.json`파일을 생성하고 아래와 같이 편집해 줍니다.

`.prettierrc.json`

```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": true,
  "quoteProps": "consistent",
  "trailingComma": "es5",
  "bracketSpacing": true,
  "arrowParens": "always",
  "endOfLine": "auto"
}
```

제 프리티어의 설정은 위와 같습니다.

`.eslintrc.json`를 편집해서  `eslint`와 `prettier`를 연결해 줍니다.

```json {hl_lines=[10,11,23,24,25]}
{
    "env": {
        "es2020": true,
        "node": true
    },
    "extends": [
        "eslint:recommended",
        "plugin:@typescript-eslint/eslint-recommended",
        "plugin:@typescript-eslint/recommended",
        "plugin:prettier/recommended",
        "prettier/@typescript-eslint"
    ],
    "parser": "@typescript-eslint/parser",
    "parserOptions": {
        "ecmaVersion": 11,
        "sourceType": "module"
    },
    "plugins": [
        "@typescript-eslint"
    ],
    "rules": {
    },
    "ignorePatterns": [
        "dist/", "node_modules/"
    ]
}

```

`extends`에서 설정은 `eslint`와 `prettier`를 연결해 주고, 

`ignorePatterns`에서 `eslint`검사를 `dist `폴더와 `node_modules` 폴더의 파일은 생략하는 코드 입니다.



## 저장시 자동 포맷 설정하기

이제 파일을 저장 할 때 

`./vscode/settings.json` 파일을 아래와 같이 편집해 줍니다.

```json
{
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.codeActionsOnSave": {
      "source.fixAll": true,
      "source.organizeImports": true
    }
  }
}
```

위와 같이 설정하면 타입스크립트 파일 일 경우 위와 같은 아래와 같은 동작을 합니다.

* `editor.defaultFormatter` : 파일을 포맷터를 지정 합니다.
* `source.fixAll` : 소스를 저장 할 때 설정에 맞게 포맷팅을 해 줍니다. 
* `source.organizeImports` : 소스 저장시 import를 정리해 줍니다.



여기까지 설정을 하게 되면 기본적인 개발 환경 설정이 완료 됩니다.

여기까지 내용은 `github`에 정리해서 소스로 올려 뒀습니다.

## 소스 주소

* https://github.com/gyuha/express-typescript-eslint





## 참고 사이트

* [VSCode에서 ESLint와 Prettier (+ TypeScript) 사용하기](https://velog.io/@das01063/VSCode%EC%97%90%EC%84%9C-ESLint%EC%99%80-Prettier-TypeScript-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0)
* [Express with TypeScript setup](https://medium.com/@xfor/express-with-typescript-setup-8d4863e4317e)
* [타입스크립트 컴파일러 옵션](https://typescript-kr.github.io/pages/Compiler%20Options.html)
* [Intro to the TSConfig Reference](https://www.typescriptlang.org/v2/tsconfig)
* [How to use ESLint with TypeScript](https://khalilstemmler.com/blogs/typescript/eslint-for-typescript/)