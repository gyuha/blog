---
title: "TypeScript Interface와 Type"
date: 2024-12-27T22:00:06+09:00
draft: true
categories: [typescript]
tags: [typescript]
---

TypeScript는 현대 웹 개발에서 필수로 자리 잡고 있는 정적 타이핑 언어입니다. <!--more--> JavaScript 위에서 작동하면서도 개발자가 안전성과 생산성을 향상시킬 수 있는 여러 고급 기능을 제공합니다. 이 글에서는 TypeScript의 고급 기능을 이해하기 쉽게 설명하고, 실무에서 활용 가능한 예제를 제공합니다.

## Interface
### 기본적인 Interface 선언
Interface는 주로 객체의 구조를 정의하는 데 사용됩니다. 각 속성의 이름과 타입을 정의하며, 클래스에서도 이를 구현할 수 있습니다.
```typescript
interface User {
  id: number;
  name: string;
  email: string;
}
const newUser: User = {
  id: 1,
  name: '철수',
  email: 'chulsoo@example.com',
};
```
### 선택적 속성(Optional Properties)과 읽기 전용(Readonly Properties)
Interface는 선택적 속성과 읽기 전용 속성도 지원합니다.
```typescript
interface Post {
  title: string;
  content?: string; // 선택적 속성
  readonly author: string; // 읽기 전용 속성
}
const blogPost: Post = {
  title: 'TypeScript Interface 사용법',
  author: '영희',
};
blogPost.title = '새로운 제목'; // 가능
// blogPost.author = '철수'; // 오류 발생
```
## Type
### Type 별칭 (Type Aliases)
Type은 다양한 타입을 결합하거나 새로운 이름으로 기존 타입을 정의할 때 사용됩니다. 유니언 타입, 인터섹션 타입 등을 정의하기에도 적합합니다.
```typescript
type Status = 'active' | 'inactive' | 'suspended';
const userStatus: Status = 'active';
```
### 객체 타입 정의
Type도 interface와 마찬가지로 객체의 구조를 정의할 수 있습니다.
```typescript
type Product = {
  id: number;
  name: string;
  price: number;
};
const newProduct: Product = {
  id: 101,
  name: '컴퓨터',
  price: 1500000,
};
```


## Interface와 Type의 차이
| 특징       | Interface                         | Type                                     |
| ---------- | --------------------------------- | --------------------------------------- |
| 타입 확장  | `extends` 키워드로 확장 가능     | 인터섹션(`&`)으로 확장 가능             |
| 병합       | 동일 이름의 Interface는 병합 가능 | Type은 병합이 불가                      |
| 사용 대상  | 주로 객체, 클래스 구조 정의에 사용 | 다양한 타입 표현에 적합                |

### Interface 확장
```typescript
interface Animal {
  name: string;
}
interface Dog extends Animal {
  breed: string;
}
const myDog: Dog = {
  name: '나비',
  breed: '푸들',
};
```
### Type 확장
```typescript
type Animal = {
  name: string;
};
type Bird = Animal & {
  canFly: boolean;
};
const myBird: Bird = {
  name: '참새',
  canFly: true,
};
```
일반적으로 Interface는 객체에 적합하며, Type은 유연성과 간결성이 요구되는 상황에 더 적합합니다. 프로젝트의 요구 사항에 따라 적절히 선택하여 활용하세요.
### Interface와 Type을 활용한 함수 작성
Interface와 Type을 사용하면 함수의 매개변수와 반환값을 명확히 정의할 수 있습니다.
#### Interface로 함수 정의
Interface는 함수의 매개변수 객체의 구조를 정의하는 데 자주 사용됩니다.
```typescript
interface Book {
  title: string;
  author: string;
  publishedYear: number;
}
function printBookInfo(book: Book): void {
  console.log(`제목: ${book.title}, 저자: ${book.author}, 출판년도: ${book.publishedYear}`);
}
// 올바른 사용 예시
printBookInfo({
  title: '타입스크립트 마스터하기',
  author: '홍길동',
  publishedYear: 2023,
});
// 잘못된 사용 예시
printBookInfo({
  title: '타입스크립트 마스터하기',
  author: '홍길동',
}); // 오류: publishedYear 속성이 없음
```
#### Type으로 함수 정의
```typescript
type Status = 'active' | 'inactive' | 'suspended';
type User = {
  id: number;
  name: string;
  status: Status;
};
function updateUserStatus(user: User, newStatus: Status): User {
  return { ...user, status: newStatus };
}
const user: User = {
  id: 1,
  name: '철수',
  status: 'active',
};
const updatedUser = updateUserStatus(user, 'inactive');
console.log(updatedUser);
```
### Interface와 Type의 장점 비교
#### Interface의 주요 장점
1. **클래스와의 통합**: Interface는 클래스에서 implements 키워드를 사용하여 쉽게 구현할 수 있습니다.
2. **자동 병합**: 동일한 이름의 Interface는 자동으로 병합되므로 확장성이 높습니다.
#### Type의 주요 장점
1. **유연성**: 유니언 타입, 인터섹션 타입 등 다양한 복합 타입을 작성할 때 유리합니다.
2. **간결성**: 간단하고 가독성이 높은 코드 작성에 적합합니다.
#### 실무에서의 선택
실무에서는 Interface와 Type을 상황에 맞게 혼합하여 사용하는 방식이 일반적입니다. **객체의 모양을 설명해야 할 때는 Interface**를, **복합적인 타입을 정의할 때는 Type**을 사용하는 것이 좋습니다.





### 유니언(Union) 타입과 인터섹션(Intersection) 타입

TypeScript는 여러 타입을 결합하여 새로운 타입을 만들어낼 수 있는 강력한 기능을 제공합니다. 이는 JavaScript에서의 논리 연산자 OR(||)와 AND(&&)와 비슷한 개념으로, 코드 베이스에서 정교한 타입 검사를 수행할 수 있게 합니다.



### 유니언 타입

유니언 타입은 두 개 이상의 타입을 조합하여 생성하는 타입입니다. 이를 통해 변수나 매개변수가 여러 타입 중 하나를 가질 수 있도록 지정할 수 있습니다.

```ts
function orderProduct(orderId: string | number) {
  console.log('상품 주문 번호:', orderId);
}

// 올바른 사용 예시
orderProduct(1);
orderProduct('123-abc');

// 잘못된 사용 예시
orderProduct({ name: '상품명' });
```

위 코드는 string 또는 number 타입을 매개변수로만 허용합니다. 다른 타입이 들어올 경우 컴파일 단계에서 오류를 반환합니다.



### 인터섹션 타입

반면, 인터섹션 타입은 여러 타입의 모든 속성을 포함하는 새로운 타입을 생성합니다. 이는 객체 또는 변수 등이 여러 타입을 동시에 만족해야 할 때 유용합니다.

```ts
interface Person {
  name: string;
  firstname: string;
}

interface FootballPlayer {
  club: string;
}

function transferPlayer(player: Person & FootballPlayer) {
  console.log(`${player.firstname} ${player.name} 선수가 ${player.club}으로 이적합니다.`);
}

// 올바른 사용 예시
transferPlayer({
  name: '라마스',
  firstname: '세르히오',
  club: 'PSG',
});

// 잘못된 사용 예시
transferPlayer({
  name: '라마스',
  firstname: '세르히오',
});
```

여기서 transferPlayer 함수는 Person과 FootballPlayer의 모든 속성을 가지는 객체만 허용합니다. 속성이 누락되면 TypeScript는 컴파일 단계에서 오류를 반환합니다.



### Keyof 키워드

keyof 키워드는 인터페이스나 객체의 키를 추출하여 새로운 유니언 타입을 생성할 수 있게 해줍니다. 이는 타입 안정성을 유지하고, 리팩토링 시 실수를 줄이는 데 중요한 역할을 합니다.

```ts
interface MovieCharacter {
  firstname: string;
  name: string;
  movie: string;
}

type characterProps = keyof MovieCharacter;
// characterProps는 'firstname' | 'name' | 'movie' 타입
```

keyof를 사용하지 않고 직접 타입을 명시할 수도 있습니다:

```ts
type characterProps = 'firstname' | 'name' | 'movie';
```

하지만 keyof를 사용하면 MovieCharacter 인터페이스를 변경하더라도 타입이 자동으로 반영되어 코드의 유지보수가 더 쉬워집니다.



#### 응용 예제

```ts
interface PizzaMenu {
  starter: string;
  pizza: string;
  beverage: string;
  dessert: string;
}

const simpleMenu: PizzaMenu = {
  starter: '샐러드',
  pizza: '페퍼로니',
  beverage: '콜라',
  dessert: '바닐라 아이스크림',
};

function adjustMenu(
  menu: PizzaMenu,
  menuEntry: keyof PizzaMenu,
  change: string,
) {
  menu[menuEntry] = change;
}

// 올바른 사용 예시
adjustMenu(simpleMenu, 'pizza', '하와이안 피자');
adjustMenu(simpleMenu, 'beverage', '맥주');

// 잘못된 사용 예시
adjustMenu(simpleMenu, 'coffee', '아메리카노');
```

위의 예제에서 adjustMenu 함수는 메뉴를 조정할 수 있도록 구현되었습니다. keyof를 사용함으로써 인터페이스 변경 시 함수가 자동으로 변화를 반영하며 타입 안정성이 유지됩니다.



### Typeof 키워드

typeof 키워드는 변수의 타입을 추출하여 사용할 수 있도록 해줍니다. 이는 특히 함수의 반환 타입을 기반으로 새로운 타입을 생성할 때 유용합니다.

#### 간단한 예제
```ts
let firstname = '프로도';
let name: typeof firstname; // name은 'string' 타입
```

단순한 예제에서는 효과가 크지 않지만, 더 복잡한 코드에서는 강력한 도구가 됩니다. 아래는 ReturnType과 결합하여 함수의 반환 타입을 추출하는 예제입니다.



#### 응용 예제
```ts
function getCharacter() {
  return {
    firstname: '프로도',
    name: '배긴스',
  };
}

type Character = ReturnType<typeof getCharacter>;
/* Character 타입은 아래와 같습니다:
{
  firstname: string;
  name: string;
}
*/
```

위 코드에서는 getCharacter 함수의 반환 타입을 기반으로 Character 타입을 생성합니다. 함수의 반환 타입이 변경되면 Character 타입도 자동으로 갱신됩니다. 이는 리팩토링과 코드 유지보수의 부담을 크게 줄여줍니다.



### 조건부 타입 (Conditional Types)

조건부 타입은 JavaScript의 삼항 연산자와 유사한 개념으로, 조건에 따라 다른 타입을 반환합니다. 이는 TypeScript에서 더욱 강력하고 유연한 타입 시스템을 지원합니다.

#### 기본 문법

T extends 조건 ? 참일 때 타입 : 거짓일 때 타입;


#### 활용 예제

```ts
interface StringId {
  id: string;
}

interface NumberId {
  id: number;
}

type Id<T> = T extends string ? StringId : NumberId;

// 사용 예시
let idOne: Id<string>; // StringId 타입
let idTwo: Id<number>; // NumberId 타입
```

위 예제에서는 Id라는 조건부 타입을 정의했습니다. 만약 T가 string 타입으로 확장 가능하다면, 반환 타입은 StringId이고, 그렇지 않으면 NumberId 타입이 됩니다.

조건부 타입은 타입에서 더욱 정교한 제어와 타입 기반 로직을 구현할 수 있도록 도와줍니다.