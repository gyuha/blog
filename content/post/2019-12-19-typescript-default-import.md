---
title: "Typescript에서 default import 개선.."
date: 2019-12-19T21:32:11+09:00
draft: true
categories: [javascript]
tags: [javascript,typescript]
---

express를 import하면 아래와 같이 import 했을 겁니다.
<!--more-->

```javascript
import * as Express from 'express';
```

하지만 tsconfig.json 파일에 아래 내용을 추가 하면..

```json
{
   "compilerOptions": {
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
   }
}
```

이렇게 import가 가능해 집니다.

```javascript
import Express from 'express'
```