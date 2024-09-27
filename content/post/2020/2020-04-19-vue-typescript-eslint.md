---
title: "Vscode에서 vue 프로젝트 생성시 ESlint와 Prettier 설정해 주기"
date: 2020-04-19T03:50:46+09:00
draft: true
categories: [typescript]
tags: [vscode, vue, typescript, eslint, tslint]
---

## Vue 프로젝트 생성하기

![vscode-vue](/img/2020-04-19-vue-typescript-eslint/vscode-vue.jpg)

기존에 사용하던 [TSLint가 더이상 지원](https://www.npmjs.com/package/tslint)을 받지 못 하게 되면서, ESlint로 넘어가야 상태가 되었습니다.
<!--more-->
여기서는 Vue 프로젝트를 생성하면서 ESlint와 Prettier를 사용하는 세팅을 간단하게 설정하려고 합니다. 사용하는 툴은 vscode입니다.

`vue create myproject` 형태로 기본 프로젝트를 선택 합니다.

```bash {hl_lines=[11,18,27,31]}
> npx vue create myproject

? Please pick a preset: Manually select features
? Check the features needed for your project:
 (*) Babel
 (*) TypeScript
 ( ) Progressive Web App (PWA) Support
 ( ) Router
 ( ) Vuex
 (*) CSS Pre-processors
>(*) Linter / Formatter
 ( ) Unit Testing
 ( ) E2E Testing     

? Use Babel alongside TypeScript (required for modern mode, auto-detected polyfills, transpiling JSX)? (Y/n) Y 

? Pick a CSS pre-processor (PostCSS, Autoprefixer and CSS Modules are supported by default):
> Sass/SCSS (with dart-sass)
  Sass/SCSS (with node-sass)
  Less
  Stylus      

? Pick a linter / formatter config:
  ESLint with error prevention only
  ESLint + Airbnb config
  ESLint + Standard config
> ESLint + Prettier
  TSLint (deprecated)    

? Pick additional lint features: (Press <space> to select, <a> to toggle all, <i> to invert selection)
>(*) Lint on save
 ( ) Lint and fix on commit 

? Where do you prefer placing config for Babel, ESLint, etc.? (Use arrow keys)
> In dedicated config files
  In package.json                  
```

여기서 처음 체크 박스에서 Linter / Formatter를 꼭 선택해 주시고, Linter / Formatter는 ESLint + Prettier를 선택해 줍니다.

```bash
> cd myproject
> code .
```
그리고 위와 같이 `vscode`를 실행 해 줍니다.

## VSCode 설정하기

만약 VSCode에는 아래와 같은 확장 프로그램을 설치가 되어 있지 않으면 설치를 해 줍니다.

-   [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
-   [Prettier - Code formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
-   [Vetur](https://marketplace.visualstudio.com/items?itemName=octref.vetur)



그리고, vscode의 설정에서 아래와 내용을 추가해 줍니다.

```json
{
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[vue]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  }
}
```

여기까지 하면 vscode에서 파일을 저장 할 때 알아서 포맷팅을 해 주고 저장을 해 주게 됩니다.

마지막으로 추가로 좀 더 상세한 설정을 하고 싶다면, 프로젝트 루트 폴더에 `.prettierrc.json`파일을 만들고 상세한 설정을 해 주시면 됩니다. 아래와 같은 형식으로 만들어 주시면 됩니다.

```json
{
  "tabWidth": 2,
  "semi": true,
  "singleQuote": false,
  "trailingComma": "es5",
  "bracketSpacing": false,
  "arrowParens": "always"
}
```

상세한 내용은 아래 링크를 확인 하시면 됩니다.

* https://prettier.io/docs/en/options.html



## 참고

* [Setup Prettier and ESLint for Typescript](https://www.anthonygonzales.dev/blog/setup-eslint-prettier-with-typescript.html)
* https://prettier.io/
* [Typescript ESLint 설정하기](https://velog.io/@kyusung/eslint-config-3)
* [ESLint - 4. Prettier 적용](https://velog.io/@kyusung/eslint-config-4)





