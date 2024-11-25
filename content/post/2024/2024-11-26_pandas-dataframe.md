---
title: "Pandas의 DataFrame에서 자주 사용되는 유용한 메서드들 소개"
date: 2024-11-26T08:18:54+09:00
draft: true
categoies: ["Python"]
tags: ["pandas", "python"]
---

Pandas는 데이터 분석 및 조작을 위한 강력한 라이브러리로, 특히 DataFrame 객체는 표 형식의 데이터를 다루는 데 매우 유용합니다. 
<!--more-->
본 포스트에서는 Pandas의 DataFrame에서 자주 사용되는 메서드들을 소개하고자 합니다. 이 메서드들은 데이터의 효율적인 탐색, 선택, 조작, 결측치 처리 및 집계를 가능하게 하여 데이터 분석 작업을 한층 더 수월하게 만들어 줍니다.

### 1. 데이터 조회 및 탐색

- **`head(n)`**: DataFrame의 처음 n개의 행을 반환합니다. 기본값은 5입니다.
  ```python
  df.head(3)
  ```

- **`tail(n)`**: DataFrame의 마지막 n개의 행을 반환합니다. 기본값은 5입니다.
  ```python
  df.tail(3)
  ```

- **`info()`**: DataFrame의 요약 정보를 제공합니다. 데이터 타입, 결측치 수 등 다양한 정보를 쉽게 확인할 수 있습니다.
  ```python
  df.info()
  ```

- **`describe()`**: 수치형 데이터의 통계 요약을 제공합니다. 평균, 표준편차, 최소값, 최대값 등의 값들을 포함하고 있습니다.
  ```python
  df.describe()
  ```

### 2. 데이터 선택 및 필터링

- **`loc[]`**: 라벨 기반 인덱싱을 사용하여 특정 행과 열을 선택합니다.
  ```python
  df.loc[0]  # 첫 번째 행 선택
  df.loc[:, '이름']  # '이름' 열 선택
  ```

- **`iloc[]`**: 정수 기반 인덱싱을 사용하여 특정 행과 열을 선택합니다.
  ```python
  df.iloc[0, 1]  # 첫 번째 행, 두 번째 열의 값 선택
  ```

- **조건 필터링**: 특정 조건을 만족하는 행을 선택합니다.
  ```python
  df[df['나이'] > 30]  # 나이가 30보다 큰 행 선택
  ```

### 3. 데이터 조작

- **`sort_values(by)`**: 특정 열을 기준으로 DataFrame을 정렬합니다.
  ```python
  df.sort_values(by='나이', ascending=False)
  ```

- **`drop(labels)`**: 특정 행이나 열을 삭제합니다.
  ```python
  df.drop(columns='도시')  # '도시' 열 삭제
  ```

- **`rename(columns)`**: 열의 이름을 변경합니다.
  ```python
  df.rename(columns={'이름': '이름_변경'}, inplace=True)
  ```

### 4. 데이터 추가 및 수정

- **`assign()`**: 새로운 열을 추가하거나 기존 열을 수정합니다.
  ```python
  df = df.assign(성별=['여', '남', '남'])
  ```

- **`append()`**: 다른 DataFrame을 현재 DataFrame에 추가합니다.
  ```python
  df2 = pd.DataFrame({'이름': ['David'], '나이': [40], '도시': ['광주']})
  df = df.append(df2, ignore_index=True)
  ```

### 5. 결측치 처리

- **`isnull()`**: 결측치가 있는지 확인합니다.
  ```python
  df.isnull()
  ```

- **`fillna(value)`**: 결측치를 특정 값으로 채웁니다.
  ```python
  df.fillna(0)
  ```

- **`dropna()`**: 결측치가 있는 행이나 열을 삭제합니다.
  ```python
  df.dropna()
  ```

### 6. 그룹화 및 집계

- **`groupby(by)`**: 특정 열을 기준으로 데이터를 그룹화합니다.
  ```python
  df.groupby('도시').mean()  # 도시별 평균 나이 계산
  ```

- **`agg()`**: 그룹화된 데이터에 대해 여러 집계 함수를 적용합니다.
  ```python
  df.groupby('도시').agg({'나이': ['mean', 'max']})
  ```

Pandas의 DataFrame은 다양한 데이터 분석 작업에 매우 유용한 메서드들을 제공합니다. 위에서 소개한 메서드를 적절히 활용하면 데이터를 보다 효율적으로 탐색하고 조작할 수 있습니다.