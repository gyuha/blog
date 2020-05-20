---
title: "VSCode에 live2d 사용하기"
date: 2019-01-22T23:42:22+09:00
draft: true
categories: [utillity]
tags: [vscode, live2d]
---


먼저 띄운 화면을 보고 가시죠~
<!--more-->

캐릭터 얼굴이 마우스 움직이는 방향으로 움직입니다.

너무 귀엽죠? 

![sample](https://github.com/summerscar/vscode-live2d/raw/master/screenshot/test.gif)





그러면, 설치를 해 볼까요?

먼저, 확장프로그램에서 live2d를 검색해서 설치해 줍니다.

그리고 재실행을 해주시면, 아무것도 안 나옵니다. -_-;

![live2d](/img/2019-01-23-vscode-live2d/vscode-live2d-01.png)

`F1` 또는 `Ctrl+Shit+P`을 누르고 `live2d install`을 해 줍니다. 그리고 다시 VSCode를 실행 해 줍니다.

그러면, 고양이가 왼쪽 하단에 나옵니다.

![live2d-3](/img/2019-01-23-vscode-live2d/vscode-live2d-02.png)

그리고, 나오는 경고... 살포시 무시하기 위해서 고양이를 살짝 옮기시고, 기어 버튼을 누릅니다.

![live-2d](/img/2019-01-23-vscode-live2d/vscode-live2d-03.png)

그리고 그만볼래(`Don't Show Again`)을 눌러 줍니다.

우리는 고양이에 만족 할 순 없으니.. 다른 캐릭터를 찾아 봅니다.

https://github.com/summerscar/live2dDemo

위 주소를 이동해서 쭈욱 보시면서 캐릭터를 선택 해 주시면 됩니다.

그리고, 그 캐릭터는 아래 주소에서 테스트 해 보시면 됩니다.

http://summerscar.me/live2dDemo/

![test](https://github.com/summerscar/live2dDemo/blob/master/screenshot/42.jpg?raw=true)

전 위에 캐릭터를 이용해서 표시를 했습니다.

설정하는 방법은 약간 귀찮습니다.

`File > Preferences > Settings`를 선택 하거나 `Ctrl+,`으로 설정 화면을 들어 갑니다.

Live2d를 검색 하시거나 직접 입력을 하시거나, 좌측 상단에 `{}`버튼을 누르셔서 코드를 넣어 주시면 됩니다.

저 같은 경우는 위 기본 값에서 사이즈를 반으로 줄여서 넣어 봤습니다.

```json
{
    "live2d.width": 150,
    "live2d.height": 200,
    "live2d.model": "33.2017.newyear",
    "live2d.headPos": 0.5,
    "live2d.scale": 1   
}
```

하지만, 수정한다고 해서 바로 적용 되지 않습니다.

`F1` 또는 `Ctrl+Shit+P`을 다시 누르고 `live2d uninstall`을 하고 다시 `live2d install`을 해 줘야 합니다.

꼭!!! 지웠다가 다시 설치를 해야 적용이 됩니다. 

결과는 아래와 같습니다.

![적용 화면](/img/2019-01-23-vscode-live2d/vscode-live2d-04.png)

참.. 이쁘죠? ㅎㅎㅎ