---
title: "자바스크립트 배열 메서드 정리"
date: 2020-03-15T21:39:55+09:00
draft: true
categories: [javascript]
tags: [javascript, array]
---

자바스크립트의 배열을 메서드를 정리해 봅니다.
<!--more-->

## Array 추가/삭제  

### Array.push()  

배열의 마지막 요소를 추가해 줍니다.   

```javascript  
let number_arr = [ 1, 2, 3, 4, 5 ];  
number_arr.push(6);  
console.log(number_arr);  // [ 1, 2, 3, 4, 5, 6 ]  
```

**Output :**  

> [1, 2, 3, 4, 5, 6]  



### Array.unshift()  

배열의 가장 첫번째 요소를 추가해 줍니다.  

```javascript  
let number_arr = [ 1, 2, 3, 4, 5 ];  
number_arr.unshift(6);  
console.log(number_arr);  // [ 6, 1, 2, 3, 4, 5 ]  
```

**Output :**  

> [6, 1, 2, 3, 4, 5]  



### Array.pop()  

배열의 가장 마지막 요소를 삭제 합니다.  

```javascript  
let number_arr = [ 1, 2, 3, 4, 5 ];  
let pop = number_arr.pop();  
console.log(number_arr);  // [ 1, 2, 3, 4 ]  
console.log(pop);  // 5  
```

**Output :**  

> [1, 2, 3, 4]  
> 5  



### Array.shift()  

배열에서 가장 첫번째 요소를 삭제합니다.  

```javascript  
let number_arr = [ 1, 2, 3, 4, 5 ];  
let shift = number_arr.shift();  
console.log(number_arr);  // [ 2, 3, 4, 5 ]  
console.log(shift);  // 1  
```

**Output :**  

> [2, 3, 4, 5]  
> 1  



### Array.slice()   

기존 배열은 변하지 않고, 해당 요소를 반환 합니다. 

```javascript  
let number_arr = [ 1, 2, 3, 4, 5 ];  
// Syntax : Array.slice(시작위치, 끝위치)  
let sp = number_arr.slice(1, 3);  // 2번째 부터 3번째 까지 반환합니다. 
console.log(number_arr);  // [1, 2, 3, 4, 5] 
console.log(sp);  // [2, 3] 
sp = number_arr.slice(2); 
console.log(sp);  // [3, 4, 5] 
```

**Output :**  

> [1, 2, 3, 4, 5]  
> [2, 3]  
> [3, 4, 5] 



### Array.splice()   

지정한 위치의 배열을 삭제 합니다.  

```javascript  
let number_arr = [ 1, 2, 3, 4, 5 ];  
// Syntax : Array.splice(시작위치, 삭제할갯수, 추가_할_아이템...)  
let sp = number_arr.splice(1, 2);  // 2번째 요소부터 2개를 삭제 합니다.  
console.log(number_arr);  // [ 1, 4, 5 ]  
console.log(sp);  // [2, 3]  
let sp2 = number_arr.splice(1, 0, 7, 8, 9); // 2번재 요소 위치에 0개를 지우고 7,8,9를 추가해 줍니다.  
console.log(number_arr); // [1, 7, 8, 9, 4, 5]  
console.log(sp2); // undefined : 0개를 삭제해서 값이 없습니다.  
```

**Output :**  

> [1, 4, 5]  
> [2, 3]  
> [1, 7, 8, 9, 4, 5]  
> []  



### Array.concat()  

배열을 합쳐 줍니다.  

```javascript  
let num1 = [ 1, 2, 3];  
let num2 = [4,5,6];  
let combine = num1.concat(num2);  
console.log(combine); // [1, 2, 3, 4, 5, 6]  
let num3 = [7, 8, 9];  
combine = num1.concat(num2, num3);  
console.log(combine); // [1, 2, 3, 4, 5, 6, 7, 8, 9]  
```

**Output :**  

> [1, 2, 3, 4, 5, 6]  
> [1, 2, 3, 4, 5, 6, 7, 8, 9]  



### Array.of()  

함수의 인수로 새 인스터스 배열을 만들어 줍니다.  

```javascript  
let ar = Array.of(1, 2, 3)  
console.log(ar); // [1, 2, 3]  
let ch = Array.of("짜장", "짬뽕");  
console.log(ch); // ["짜장", "짬뽕"]  
```

**Output :**  

> [1, 2, 3]  
> [ "짜장", "짬뽕"]  



## Array 반복  

### Array.forEach()  

배열의 요소를 순차적으로 반복해 줍니다.  

```javascript  
let vl = [ 'one', 'two', 'three' ];  
vl.forEach((e) => {  
    console.log(e); // one, two, three를 차례대로 출력  
})  
```

**Output :**  

> one  
> two  
> three  

2번째 인자는 요소의 인덱스를 돌려 줍니다.  

```javascript  
let vl = [ 'one', 'two', 'three' ];  
vl.forEach((e, i) => {  
    console.log(e, i);  
})  
```

**Output :**  

> one 0  
> two 1  
> three 2  



### Array.values()  

배열의 요소를 새로운 반복형 객체로 만들어 줍니다.  

```javascript  
let vl = [ 'one', 'two', 'three' ];  
let iterator = vl.values();  

console.log(iterator.next().value);  // one  
console.log(iterator.next().value);  // two  
console.log(iterator.next().value);  // three  
console.log(iterator.next().value);  // undefined  
```

**Output :**  

>one  
>two  
>three  
>undefined  

```javascript  
let vl = [ 'one', 'two', 'three' ];  
let iterator = vl.values();  

for (let i of iterator) {  
    console.log(i);  
}  
console.log(iterator.next().value);  // undefined : 위에서 모두 반복해서 없음.  
```

**Output :**  

> one  
> two  
> three  



### Array.entries()  

배열의 요소를 키(key)와 값(value)로 짝지어진 반복형 객체로 만들어 줍니다.  

```javascript  
let vl = [ 'one', 'two', 'three' ];  
let iterator = vl.values();  
for (let i of iterator) {  
    console.log(i);  
}  
```

**Output :**  

>[0, \"one"]  
>[1, \"two"]  
>[2, \"three"]  



## Array 찾기  

### Array.some()  

배열중에서 요소가 조건식에 맞는게 1개라도 있으면 true를 반환합니다.  

```javascript  
console.log([2, 5, 8, 1, 4].some((e) => e > 5));  
console.log([2, 5, 8, 1, 4].some((e) => e > 9));  
```

**Output :**  

>true  
>false  



### Array.every()  

배열의 요소가 모두 조건식에 맞아야 true를 반환합니다.  

```javascript  
console.log([2, 5, 8, 1, 4].every((e) => e < 9));  
console.log([2, 5, 8, 1, 4].every((e) => e > 4));  
```

**Output :**  

>true  
>false  



### Array.find()  

배열에서 조건식에 맞는 첫번째 요소를 반환합니다.  

```javascript  
console.log([2, 5, 8, 1, 4].find((e) => e < 9));  
console.log([2, 5, 8, 1, 4].find((e) => e > 4));  
```

**Output :**  

>2  
>5  



2번째 값은 배열의 index, 3번째는 현재 배열을 입니다.  

```javascript  
console.log([2, 5, 8, 1, 4].find((e, i) => e > 3  && i < 2));  
```

**Output :**  

>5  



### Array.findIndex()  

배열에서 조건식에 맞는 첫번째 요소의 인덱스를 반환합니다.  

```javascript  
console.log([2, 5, 8, 1, 4].findIndex((e) => e < 9));  
console.log([2, 5, 8, 1, 4].findIndex((e) => e > 4));  
```

**Output :**  

>0  
>1  



### Array.filter()  

배열에서 조건식에 맞는 요소들을 배열로 반환합니다.  

```javascript  
console.log([2, 5, 8, 1, 4].filter((e) => e < 9));  
console.log([2, 5, 8, 1, 4].filter((e) => e > 4));  
```

**Output :**  

>[ 2, 5, 8, 1, 4 ]  
>[ 5, 8 ]  





### Array.indexOf()  

배열에서 요소의 위치를 찾는다. 찾을수가 없으면 -1을 반환합니다.  

두번째 값을 찾을 시작 위치 입니다.  

```javascript  
console.log([2, 5, 8, 1, 4].indexOf(2));  
console.log([2, 5, 8, 1, 4].indexOf(8));  
console.log([2, 1, 8, 1, 4].indexOf(1, 3));  
```

**Output :**  

>0  
>2  
>3  





## Array 변환하기  

### Array.fill()  

배열을 요소를 채워 줍니다.  

```javascript  
let arr = [1, 2, 3, 4];  
arr.fill(7); // 모두 7로 채워 넣는다.  
console.log(arr);  
```

**Output :**  

>[ 7, 7, 7, 7 ]  



시작 지점을 정해서 채워 줄 수 있습니다. 시작 위치는 원하는 위치의 -1을 해서 넣어 줍니다.  

```javascript  
let arr = [1, 2, 3, 4];  
arr.fill(7, 1); // 2번째 부터 끝까지 7로 채움, 0부터 시작이다.  
console.log(arr);  
```

**Output :**  

>[ 1, 7, 7, 7 ]  



시작과 끝 지점을 지정해서 채워 줄 수 있습니다. 끝 지점은 위치를 넣어 줘야 합니다.  

```javascript  
let arr = [1, 2, 3, 4];  
arr.fill(7, 1, 3); // 2번째 부터 3번째 까지 7로 채움  
console.log(arr);  
```

**Output :**  

>[ 1, 7, 7, 4 ]  



### Array.copyWithin()  

지정한 위치에 값을 복사해서 넣어 줍니다.  

첫번째는 복사할 위치, 두번째는 시작위치 (기본값:0), 세번째는 끝위치(기본값:  array.length)  

```javascript  
var array = [ 1, 2, 3, 4, 5, 6, 7 ];   
console.log(array.copyWithin(1, 3, 5));   
```

**Output :**  

>[ 1, 4, 5, 4, 5, 6, 7 ] 
