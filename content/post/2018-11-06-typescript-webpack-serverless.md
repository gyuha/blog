---
title: "Typescript Webpack Serverless 구성하기"
date: 2018-11-06T18:29:07+09:00
draft: true
categories: [typescript]
tags: [typescript,serverless,webpack,node,lambda]
---


serverless에서 webpack을 이용해서 typescript를 구성해 보면서 작업 하던걸 기록 해 둡니다.
<!--more-->


## 기본 환경 구성

기본적으로 `node.js`가 설치 되어 있어야 합니다.

serverless를 설치 합니다.

```bash
npm install -g serverless
```



그리고, 프로젝트를 생성해 줍니다.

```bash
$ serverless create -t aws-nodejs -p hello-lambda
Serverless: Generating boilerplate...
Serverless: Generating boilerplate in "/home/gyuha/workspace/hello-lambda"
 _______                             __
|   _   .-----.----.--.--.-----.----|  .-----.-----.-----.
|   |___|  -__|   _|  |  |  -__|   _|  |  -__|__ --|__ --|
|____   |_____|__|  \___/|_____|__| |__|_____|_____|_____|
|   |   |             The Serverless Application Framework
|       |                           serverless.com, v1.32.0
 -------'

Serverless: Successfully generated boilerplate for template: "aws-nodejs"
$ cd hello-lambda
```



`npm init`으로 `package.jon`을 설정해 주고 필요한 패키지를 설치 해 줍니다.

```bash
$ npm init
$ npm install --save-dev serverless-webpack serverless-offline ts-loader typescript webpack
```







## Severless 설정하기

`serverless.yml` 파일을 아래와 같이 편집 해 줍니다.

```yaml
service: aws-nodejs # NOTE: update this with your service name

provider:
  name: aws
  runtime: nodejs8.10
  stage: dev
  region: ap-northeast-2

plugins:
  - serverless-webpack
  - serverless-offline

functions:
  hello:
    handler: src/server.hello
    events:
     - http:
         path: hello
         method: get

```

여기서, 주 된 내용은 plugins의 추가와 functions에서 events의 추가 입니다.





## Typescript과 Webpack 설정하기

`tsconfig.json` 파일을 만들고 아래와 같이 입력해 줍니다.

```json
{
    "compilerOptions": {
      "module": "commonjs",
      "target": "es6",
      "sourceMap": true
    },
    "exclude": [
      "node_modules"
    ]
  }
```





`webpack.copnfg.js` 파일을 만들고 아래와 같이 입력해 줍니다.

```javascript
const path = require("path");

module.exports = {
  entry: path.join(__dirname, "src/server.ts"),
  output: {
    libraryTarget: "commonjs",
    filename: "src/server.js",
    path: path.resolve(__dirname, "dist")
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: "ts-loader",
        exclude: /node_modules/
      }
    ]
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"]
  }
};

```


## 소스 작성 해 주기

`src/server.ts` 파일을 생성하고 아래과 같이 입력 해 줍니다.

```typescript
interface SomeResponse {
  statusCode: number;
  body: string;
}

export async function hello (event: any, context: any) {
  const response: SomeResponse = {
    statusCode: 200,
    body: JSON.stringify({
      message: Math.floor(Math.random() * 10)
    })
  };

  return response
};
```

여기까지 완료 하면.. 기본 실행이 구성 됩니다.





## 오프라인 실행하기

```bash
sls offline
```



## 배포 하기

```bash
sls deploy
```

----


예제 코드는 [serverless-typescript-webpack](https://github.com/gyuha/serverless-typescript-webpack)에서 볼 수 있습니다.

