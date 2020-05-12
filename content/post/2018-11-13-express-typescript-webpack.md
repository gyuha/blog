---
title: "Express Typescript Webpack"
date: 2018-11-13T23:11:37+09:00
draft: true
categories: [javascript]
tags: [webpack,typescript,express,node]
---

express를 타입스크립트롤 시작하는 방법을 설명합니다.
<!--more-->

## 기본 패키지 설정
package.json 파일을 만들어 줍니다.
```bash
npm init -y
```

express에 필요한 패키지를 설치해 줍니다.
```bash
yarn add express body-parser
```

## Typescript 설정

typescript에 사용할 패키지를 설치 합니다.
```bash
yarn add --dev typescript ts-loader ts-node tslint @types/node @types/express
```

typescript에 필요한 내용을 설치 합니다. 그리고 `tsconfig.json`파일을 아래와 같이 입력 해 줍니다.

```json
{
  "compilerOptions": {
    "target": "es6",
    "module": "commonjs",
    "moduleResolution": "node"
  },
  "exclude": [
    "node_modules"
  ]
}
```



## Webpack 설정

```bash
yarn add --dev webpack webpack-watch-server
```
`webpack.config.js`  파일을 아래와 같이 입력 합니다.

```javascript
var path = require('path');

module.exports = {
  entry: './src/index.ts',
  target: 'node',
  output: {
    filename: 'index.js',
    path: path.resolve(__dirname, 'dist')
  },
  devtool: 'source-map',
  resolve: {
    // Add `.ts` and `.tsx` as a resolvable extension.
    extensions: ['.ts', '.tsx', '.js']
  },
  module: {
    rules: [
      // all files with a `.ts` or `.tsx` extension will be handled by `ts-loader`
      { test: /\.tsx?$/, loader: 'ts-loader' }
    ]
  }
};
```

## Express 기본 제작

`src/index.ts`파일을 아래와 같이 작성 합니다.

```typescript
import * as bodyParser from "body-parser";
import * as express from "express";
import { Request, Response } from "express";
import * as http from 'http';

var app:express.Application = express();

app.get('/', (req: Request, res: Response) => {
  res.status(200).json({status: "ok"});
});


let httpPort = 3000;
app.set("port", httpPort);
var httpServer = http.createServer(app);

//listen on provided ports
httpServer.listen(httpPort, (data) => {
  console.log(`Listening on port ${httpPort}`)
});
```



위 내용은 [github](https://github.com/gyuha/express-typescript-webpack)에 올려져 있습니다.
