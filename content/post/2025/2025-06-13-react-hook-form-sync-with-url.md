---
title: Next.js에서 react-hook-form과 URL을 우아하게 동기화하는 법 🚀
date: 2025-06-13T21:00:01+09:00
draft: true
category:
  - react
tags:
  - next.js
  - react-hook-form
  - typescript
---

이번 포스트에서는 Next.js 프로젝트를 진행하면서 유용하게 사용할 수 있는 자작 커스텀 훅, `useFormUrlSync`에 대해 이야기하고자 합니다.

검색 필터나 정렬 기능이 있는 페이지를 개발할 때 이러한 경험이 있으실 겁니다. 사용자가 필터 값을 설정하고 검색 결과 페이지에서 특정 아이템을 클릭했다가 뒤로 가기 버튼을 누르면, 설정했던 필터 값들이 전부 초기화되는 상황 말입니다. 사용자 입장에서는 매우 불편한 순간이 아닐 수 없습니다.

이러한 문제를 해결하는 가장 효과적인 방법은 폼(Form)의 상태를 URL 쿼리 파라미터(Query Parameter)에 실시간으로 동기화하는 것입니다. 이렇게 하면 사용자가 설정한 필터 값이 URL에 그대로 남아, 페이지를 새로고침하거나 링크를 공유해도 동일한 상태가 유지됩니다.

이번 글에서는 이 기능을 구현하는 `useFormUrlSync` 커스텀 훅을 만들고, 사용법을 자세히 알아보겠습니다.

## 왜 URL과의 동기화가 필요합니까? 🤔

본격적으로 코드를 살펴보기 전에, 왜 폼 상태를 URL과 동기화해야 하는지 짚고 넘어갈 필요가 있습니다.

* **향상된 사용자 경험 (UX)**: 사용자가 뒤로 가기/앞으로 가기 버튼을 사용해도 필터링된 상태가 그대로 유지됩니다.
* **공유 가능한 링크**: 필터나 검색 조건이 포함된 URL을 다른 사람에게 그대로 공유할 수 있습니다.
* **북마크 가능**: 사용자는 특정 검색 결과 페이지를 북마크하고 나중에 다시 방문할 수 있습니다.

이 모든 것이 사소해 보일 수 있지만, 잘 만들어진 웹 애플리케이션의 디테일을 결정하는 중요한 요소입니다.

## `useFormUrlSync` 전체 코드 훑어보기 🧐

먼저 우리가 만들 커스텀 훅의 전체 코드를 살펴보겠습니다. Next.js(App Router 기준) 환경과 `react-hook-form` 라이브러리를 사용한다는 점을 참고해 주시기 바랍니다.

```typescript
import type { AliasAny } from "@/types/alias.types";
import { isNumber } from "es-toolkit/compat";
import { useRouter, useSearchParams } from "next/navigation";
import { useCallback, useEffect, useRef } from "react";
import { type DefaultValues, type FieldValues, type UseFormProps, type UseFormReturn, useForm } from "react-hook-form";

// ... (훅의 상세 코드는 이전과 동일) ...

export function useFormUrlSync<T extends FieldValues>(options: UseFormUrlSyncOptions<T>): UseFormReturn<T> {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { excludeFromUrl = [], replace = true, defaultValues, ...formOptions } = options;

  const isUpdatingFromUrl = useRef(false);

  const getUrlValues = useCallback(() => {
    return extractInitialValuesFromUrl<T>(searchParams, excludeFromUrl as (keyof T)[]);
  }, [searchParams, excludeFromUrl]);

  const initialValues = {
    ...defaultValues,
    ...getUrlValues(),
  } as DefaultValues<T>;

  const form = useForm({
    ...formOptions,
    defaultValues: initialValues,
  });

  const { watch, reset, getValues } = form;

  const updateUrl = useCallback(
    (values: T) => {
      const params = createUrlParamsFromValues(values, searchParams, excludeFromUrl as (keyof T)[]);
      const newSearchString = params.toString();
      const currentSearchString = new URLSearchParams(window.location.search).toString();

      if (newSearchString !== currentSearchString) {
        const newUrl = `${window.location.pathname}?${newSearchString}`;
        if (replace) {
          router.replace(newUrl, { scroll: false });
        } else {
          router.push(newUrl, { scroll: false });
        }
      }
    },
    [router, searchParams, excludeFromUrl, replace],
  );

  useEffect(() => {
    const subscription = watch(values => {
      if (isUpdatingFromUrl.current) {
        return;
      }
      updateUrl(values as T);
    });

    return () => subscription.unsubscribe();
  }, [watch, updateUrl]);

  useEffect(() => {
    const urlValues = getUrlValues();
    const currentFormValues = getValues();

    const relevantFormValues: Partial<T> = {};
    for (const key in urlValues) {
      if (Object.prototype.hasOwnProperty.call(urlValues, key)) {
        relevantFormValues[key as keyof T] = currentFormValues[key as keyof T];
      }
    }

    if (!deepEqual(urlValues, relevantFormValues)) {
      isUpdatingFromUrl.current = true;

      reset({
        ...currentFormValues,
        ...urlValues,
      } as DefaultValues<T>);

      setTimeout(() => {
        isUpdatingFromUrl.current = false;
      }, 0);
    }
  }, [getUrlValues, reset, getValues]);

  return form;
}
```

코드가 다소 길어 보일 수 있지만, 핵심 로직은 간단합니다. 이제부터 하나씩 분석해 보겠습니다.

## 핵심 로직 파헤치기 💡

이 훅은 **양방향 동기화**를 구현하는 것이 핵심입니다.

1.  **폼 상태 변경** → **URL 업데이트**
2.  **URL 변경** (예: 뒤로 가기) → **폼 상태 업데이트**

이 두 가지 흐름이 어떻게 구현되었는지 살펴보겠습니다.

### 1. 폼 변경 → URL 업데이트

이 부분은 `react-hook-form`의 `watch` 함수와 `useEffect`를 사용하여 구현합니다.

```typescript
  // ...

  useEffect(() => {
    const subscription = watch(values => {
      // isUpdatingFromUrl 플래그에 대해서는 잠시 후에 설명하겠습니다.
      if (isUpdatingFromUrl.current) {
        return;
      }
      updateUrl(values as T); // 폼 값이 변경되면 URL을 업데이트하는 함수 호출
    });

    return () => subscription.unsubscribe();
  }, [watch, updateUrl]);

  // ...
```

`watch`는 폼의 모든 값 변경을 감지하는 구독(subscription)을 생성합니다. 값이 바뀔 때마다 `updateUrl` 함수를 호출하여 변경된 값을 URL 쿼리 파라미터로 만들어줍니다.

### 2. URL 변경 → 폼 상태 업데이트

이것은 사용자가 브라우저의 뒤로 가기/앞으로 가기 버튼을 눌렀을 때를 위한 기능입니다. `useSearchParams` 훅이 URL의 변경을 감지하면, `useEffect`가 실행됩니다.

```typescript
  // ...

  useEffect(() => {
    const urlValues = getUrlValues(); // URL에서 현재 폼 관련 값들을 가져옴
    const currentFormValues = getValues(); // react-hook-form의 현재 값들을 가져옴

    // ... (비교 로직) ...

    // URL의 값과 폼의 값이 다를 경우
    if (!deepEqual(urlValues, relevantFormValues)) {
      isUpdatingFromUrl.current = true; // 무한 루프 방지 플래그 ON

      // URL 값으로 폼 상태를 리셋(업데이트)
      reset({
        ...currentFormValues,
        ...urlValues,
      } as DefaultValues<T>);

      // 아주 잠깐의 딜레이 후 플래그 OFF
      setTimeout(() => {
        isUpdatingFromUrl.current = false;
      }, 0);
    }
  }, [getUrlValues, reset, getValues]); // URL이 변경될 때마다 실행
```

URL이 바뀌면 `searchParams` 객체가 변경되고, 이를 의존하는 `getUrlValues`가 새로운 값을 반환하면서 이 `useEffect`가 다시 실행됩니다. 그리고 URL에서 가져온 값(`urlValues`)과 현재 폼의 값(`currentFormValues`)을 비교해서, 다르다면 `form.reset`을 호출하여 폼을 업데이트해줍니다.

### 3. 무한 루프 방지: `isUpdatingFromUrl` ⚠️

여기서 매우 중요한 부분은 바로 `isUpdatingFromUrl`이라는 `useRef` 값입니다. 이것이 왜 필요합니까?

만약 이 플래그가 없다면 다음과 같은 **무한 루프**에 빠질 수 있습니다.

1.  URL 변경 → `useEffect` 실행 → `form.reset()` 호출 (폼 업데이트)
2.  폼 업데이트 → `watch` 감지 → `updateUrl()` 호출 (URL 업데이트)
3.  URL 업데이트 → `useEffect` 실행 → `form.reset()` 호출 (폼 업데이트)
4.  ... 무한 반복 ...

`isUpdatingFromUrl.current = true`는 "지금은 URL 변경 때문에 폼을 강제로 업데이트하는 중이니, `watch`는 잠시 반응하지 말라"고 알려주는 신호탄과 같습니다. 폼을 `reset` 한 직후 `setTimeout`으로 플래그를 다시 `false`로 바꿔서, 그 이후의 사용자 입력에는 정상적으로 반응하도록 만듭니다. 매우 효율적인 방법입니다.

## 실제로 사용해보기 📝

이제 이 훅을 실제 컴포넌트에서 어떻게 사용하는지 살펴보겠습니다. 간단한 검색 폼을 예시로 들어보겠습니다.

```tsx
// components/SearchForm.tsx
"use client";

import { useFormUrlSync } from "@/hooks/useFormUrlSync"; // 우리가 만든 훅

interface SearchFormValues {
  keyword: string;
  category: string;
  inStockOnly: boolean;
  page: number;
}

export function SearchForm() {
  const { register, handleSubmit, formState: { errors } } = useFormUrlSync<SearchFormValues>({
    // 폼의 기본값 설정
    defaultValues: {
      keyword: "",
      category: "all",
      inStockOnly: false,
      page: 1,
    },
    // URL에 포함시키고 싶지 않은 필드
    excludeFromUrl: ["page"],
    // URL 변경 시 히스토리를 남기고 싶을 때
    replace: false,
  });

  const onSubmit = (data: SearchFormValues) => {
    // 실제 검색 로직 수행
    console.log("검색 실행:", data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="keyword">검색어</label>
        <input id="keyword" {...register("keyword")} />
      </div>
      <div>
        <label htmlFor="category">카테고리</label>
        <select id="category" {...register("category")}>
          <option value="all">전체</option>
          <option value="electronics">전자기기</option>
          <option value="books">도서</option>
        </select>
      </div>
      <div>
        <input type="checkbox" id="inStockOnly" {...register("inStockOnly")} />
        <label htmlFor="inStockOnly">재고 있음</label>
      </div>
      <button type="submit">검색</button>
    </form>
  );
}
```

사용법은 기존 `react-hook-form`의 `useForm`과 거의 동일합니다. 단순히 `useForm` 대신 `useFormUrlSync`를 쓰고, 몇 가지 옵션만 추가하면 됩니다.

> 📌 **팁: `replace` 옵션은 언제 사용합니까?**
>
> `useFormUrlSync` 훅의 `replace` 옵션은 URL을 업데이트할 때 Next.js의 `router.replace()`를 쓸지, `router.push()`를 쓸지 결정하는 중요한 키입니다.
>
> * ✅ **`replace: true` (기본값)**
>     * **사용 시나리오:** 실시간으로 변하는 필터 값(체크박스, 검색어 입력 등)에 적합합니다.
>     * **장점:** `router.replace()`는 브라우저의 히스토리 스택에 새 기록을 추가하지 않고 현재 URL을 **대체**합니다. 만약 사용자가 검색어를 한 글자씩 입력할 때마다 히스토리가 쌓인다면, 뒤로 가기 버튼을 누를 때마다 한 글자씩 지워지는 불편한 경험을 하게 될 것입니다. `replace`는 이런 불필요한 히스토리를 방지합니다.
>
> * ❌ **`replace: false`**
>     * **사용 시나리오:** 사용자의 명시적인 액션(예: '검색' 버튼 클릭, '다음 페이지' 버튼 클릭)으로 URL이 변경될 때 적합합니다.
>     * **장점:** `router.push()`는 브라우저 히스토리 스택에 새 기록을 **추가**합니다. 예를 들어, '검색 조건 A'로 검색했다가 '검색 조건 B'로 다시 검색했을 때, 사용자는 뒤로 가기 버튼을 눌러 '검색 조건 A'의 결과로 돌아가고 싶을 수 있습니다. 이때 `replace: false` (즉, `router.push`)를 사용하면 자연스러운 브라우저 탐색 경험을 제공할 수 있습니다.
>
> 이 옵션을 통해 우리는 사용자의 행동 의도에 맞는 최적의 URL 업데이트 방식을 선택할 수 있습니다.

이제 이 폼에 값을 입력하면, URL이 실시간으로 변하고 브라우저 히스토리에도 차곡차곡 쌓이는 것을 볼 수 있습니다.

> `http://localhost:3000/search?keyword=Next.js&category=books&inStockOnly=true`

## 마무리하며

이번 글에서는 Next.js 환경에서 `react-hook-form`의 상태를 URL 쿼리 파라미터와 동기화하는 `useFormUrlSync` 커스텀 훅에 대해 알아보았습니다.

이 훅 하나만 잘 만들어두면, 앞으로 필터나 검색 기능이 필요한 모든 페이지에서 사용자 경험을 크게 향상시킬 수 있을 것입니다. 상태 유지를 위해 더 이상 복잡한 전역 상태 관리 라이브러리에 의존할 필요가 없습니다.

독자 여러분께서는 프로젝트에서 폼 상태를 어떻게 관리하고 계십니까? 더 좋은 아이디어나 방법이 있다면 댓글을 통해 공유해 주시기 바랍니다. 😊