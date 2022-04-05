---
title: 유용한 한 줄 자바스크립트
date: 2022-02-26T10:17:42+09:00
draft: true
categories: [javascript]
tags: [javascript]
---

## 
자바스크립에서 요긴하게 쓸 수 있는 한 줄 짜리 코드 들을 공유 합니다.

# 배열 섞기

```javascript
const shuffleArray = (arr) => arr.sort(() => Math.random() - 0.5);

const arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];  
console.log(shuffleArray(arr));
```

## 

# 클립보드 복사하기

```javascript
const copyToClipboard = (text) =>
  navigator.clipboard?.writeText && navigator.clipboard.writeText(text);

copyToClipboard("Hello World!");
```



# 유니크 배열

```javascript
const getUnique = (arr) => [...new Set(arr)];

const arr = [1, 1, 2, 3, 3, 4, 4, 4, 5, 5];
console.log(getUnique(arr));
```



# 배열 체크

```javascript
const isArray = (arr) => Array.isArray(arr);

console.log(isArray([1, 2, 3]));  // true
console.log(isArray({ name: 'Ovi' }));  // false
console.log(isArray('Hello World'));  // false
```



# 랜덤 숫자

```javascript
const randomInt = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);

console.log(random(1, 50));
```



# 타크 모드 검출

```javascript
const isDarkMode = () =>
  window.matchMedia &&
  window.matchMedia("(prefers-color-scheme: dark)").matches;

console.log(isDarkMode());
```



# 스크롤 맨 위로 / 아래로

```javascript
const scrollToTop = (element) =>
  element.scrollIntoView({ behavior: "smooth", block: "start" });

const scrollToBottom = (element) =>
  element.scrollIntoView({ behavior: "smooth", block: "end" });
```



# 랜덤 색상 생성기

```javascript
const generateRandomHexColor = () =>
  `#${Math.floor(Math.random() * 0xffffff).toString(16)}`;
```



# 날짜 사이 계산하기

```javascript
const daysDiff = (date, date2) => Math.ceil(Math.abs(date - date2) / 86400000);

console.log(daysDiff(new Date('2022-05-10'), new Date('2022-11-25')));  // 199
```



# 값 바꾸기

```javascript
let foo = 'foo';
let bar = 'bar';

[foo, bar] = [bar, foo];

console.log(foo, bar); // bar foo
```



# 배열 합치기

```javascript
// 배열을 합칩니다. 하지만, 중복은 유지
const merge = (a, b) => a.concat(b);
// 또는
const merge = (a, b) => [...a, ...b];

// 중복을 제거 하면서 합침
const merge = [...new Set(a.concat(b))];
// 또는
const merge = [...new Set([...a, ...b])];
```



# 자바스크립트 실제 유형 가져오기

```javascript
const trueTypeOf = (obj) => {
  return Object.prototype.toString.call(obj).slice(8, -1).toLowerCase();
};

console.log(trueTypeOf(''));  // string
console.log(trueTypeOf(0));  // number
console.log(trueTypeOf());  // undefined
console.log(trueTypeOf(null));  // null
console.log(trueTypeOf({}));  // object
console.log(trueTypeOf([]));  // array
console.log(trueTypeOf(0));   // number
console.log(trueTypeOf(() => {}));  // function
```



# 긴 문자열 자르기

```javascript
const truncateString = (string, length) => {
  return string.length < length ? string : `${string.slice(0, length)}...`;
};

console.log(truncateString('동해 물과 백두산이 마르고 닳도록', 10)); // 동해 물과 백두산이
```



# 현재 탭이 보이고 있는지 체크

```javascript
const isTabInView = () => !document.hidden; // Not hidden

console.log(isTabInView()); // true or false
```



# 숫자 앞에 0붙여서 출력하기

```javascript
const numberPad = (num, size) =>
  String(num)
    .padStart(size, '0')
    .substring(-size);

console.log(numberPad(5, 3)); // 005
```



# 빈 배열 체크

```javascript
const checkEmptyArray = (arr) => !Array.isArray(arr) || arr.length === 0;
 
console.log(checkEmptyArray([0, 2, 3, 4, 5])); // true
console.log(checkEmptyArray([])); // false
console.log(checkEmptyArray(""))y(arr3));  // false
```
