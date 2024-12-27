---
title: "Docker 이미지 최적화: 더 빠른 배포를 위한 크기 줄이기"
date: 2024-12-27T22:00:06+09:00
draft: true
categories: [system]
tags: [docker, "docker compose", "ci/cd"]
---

![Docker image optimization](/img/2024/docker/docker-opti.png)

Docker의 이미지에는 사용자가 생각하는 것보다 더 많은 내용이 포함되는 경우가 많습니다. 
<!--more-->
이러한 불필요한 파일, 라이브러리, 의존성 등으로 인해 이미지 크기가 커지고 배포 및 실행 속도가 느려질 수 있습니다. 이 글에서는 Docker 이미지 최적화를 통해 크기와 실행성을 개선하는 다양한 방법을 소개합니다.

## Docker 이미지를 최적화해야 하는 이유
1. **이미지 크기 감소**: 최적화를 통해 이미지 크기를 줄임으로써 저장소 및 네트워크 사용량을 절약할 수 있습니다. 이는 개발 및 배포 시간을 단축하고 비용을 절감하는 데 크게 기여합니다.
2. **배포 속도 향상**: 이미지 크기가 작아지면 컨테이너의 배포와 로딩 속도가 빨라지며, 이는 CI/CD 워크플로우의 효율성을 높입니다.
3. **보안성 향상**: 불필요한 파일과 의존성을 제거하면 공격 표면이 감소하여 잠재적인 보안 취약점을 줄일 수 있습니다.
4. **자원 절약**: 작고 간결한 이미지는 시스템 리소스를 효율적으로 사용하며, 메모리 및 디스크 공간 낭비를 방지합니다.
5. **유지보수 용이**: 최적화된 이미지에는 필수 구성 요소만 포함하므로 쉽게 관리와 디버깅을 할 수 있습니다. 불필요한 복잡성을 줄여 유지보수가 훨씬 간단해집니다.

## Docker 이미지 최적화를 위한 효과적인 방법
### 1. 최소한의 베이스 이미지 선택하기
기본적으로 ubuntu:latest와 같은 큰 이미지를 사용하는 대신, 우리는 alpine으로 전환했습니다. 이 간단한 변화로 이미지 크기를 800MB에서 30MB 이하로 줄일 수 있었습니다.
**예시:**
```javascript
FROM alpine:latest
```
### 2. 다단계 빌드 사용하기
React 애플리케이션 같은 프로젝트에서는 빌드 의존성(Node.js, npm 등)이 빌드 과정에서만 필요하고 프로덕션 이미지에서는 필요하지 않습니다. 다단계 빌드를 사용하면 빌드 환경과 런타임 환경을 분리하여 훨씬 작은 이미지를 생성할 수 있습니다.
**예시:** React 애플리케이션에 다단계 빌드를 적용한 Dockerfile은 다음과 같습니다:
```javascript
# 빌드 단계 (Build Stage)
FROM node:16 AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build
# 런타임 단계 (Runtime Stage)
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]
```
이 방법은 빌드 파일들만 최종 이미지에 포함되도록 보장해, 프로덕션에 적합하고 크기가 작아진 이미지를 제공합니다.
### 3. 불필요한 파일 제거하기
디버깅 과정에서 임시 파일들이 빌드에 포함되는 경우가 많았습니다. .dockerignore 파일을 추가함으로써 이러한 파일들이 이미지에 포함되지 않도록 방지했습니다.
**예시:**
```javascript
node_modules
*.log
.git
```
### 4. 레이어 결합 및 최소화하기
Dockerfile의 각 명령어(RUN, COPY, ADD 등)는 이미지에 새로운 레이어를 생성합니다. 레이어가 많아지면 이미지 크기가 커질 수 있습니다. 여러 명령어를 하나의 RUN 명령어로 결합하여 레이어 수를 줄이면 이미지를 최적화할 수 있습니다.
**예시:** 다음과 같이 작성하기보다는:
```javascript
RUN apt-get update
RUN apt-get install -y curl nodejs
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
```
다음처럼 한 줄로 결합하면 좋습니다:
```javascript
RUN apt-get update && apt-get install -y curl nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
```
이렇게 하면 레이어 수를 줄이고 같은 레이어 안에서 캐시와 같은 임시 파일을 제거할 수 있어 이미지가 더 작고 깔끔해집니다.
### 5. 불필요한 의존성 설치 피하기
Docker 이미지 초기 상태에서는 "혹시 필요할지도 몰라서" 추가 라이브러리를 설치하는 경우가 많았습니다. 그러나 시간이 지나면서 이는 이미지의 불필요한 비대화와 불필요한 보안 위험을 초래한다는 것을 깨달았습니다. 런타임에 실제로 필요한 의존성만 지정함으로써 이미지를 더 작고 안전하게 유지할 수 있었습니다.
### 6. 캐시 활용하기
도커 이미지 빌드 과정에서 캐시를 잘 활용하면 이미지 빌드 시간을 크게 단축할 수 있습니다. 예를 들어, 변경되지 않는 의존성 파일(COPY 명령어)은 Dockerfile 최상단에 배치하여 캐시를 재사용할 수 있게 설계할 수 있습니다.예시:
```javascript
COPY package.json package-lock.json ./
RUN npm install
```
### 7. docker-slim 사용하기
이미지 최적화에 혁신을 가져온 도구 중 하나는 docker-slim이었습니다. 이 도구는 이미지를 자동으로 분석하고 사용되지 않는 파일, 바이너리, 라이브러리를 제거하여 크기를 줄여주며, 기능에는 영향을 주지 않습니다.
docker-slim을 사용한 이후, 최대 80%까지 이미지 크기를 줄일 수 있었으며 이는 최적화 전략의 필수 도구가 되었습니다.
**이미지를 최적화하는 명령어:**
```javascript
docker-slim build <image-name>
```
### 8. 이미지 정기적으로 점검 및 정리하기
Docker 이미지는 시간이 지남에 따라 쌓이는데, 사용되지 않는 이미지나 레이어는 공간을 낭비하게 됩니다. 정기적으로 사용하지 않는 이미지를 점검하고 정리하는 것은 깨끗한 환경을 유지하는 데 중요합니다.
**사용하지 않는 이미지를 정리하는 명령어:**
```javascript
docker system prune -f
```
**모든 사용하지 않는 이미지를 제거하는 명령어:**
```javascript
docker image prune -a -f
```
정기적인 정리 작업을 통해 Docker 환경을 효율적으로 유지할 수 있습니다.
### 9. 압축 파일 활용하기
이미지 크기를 줄이는 또 다른 방법으로, 압축된 애플리케이션 소스를 Docker 이미지에 포함할 수 있습니다. 소스 파일을 압축하면 전송량이 줄어들고 크기가 최적화됩니다. 또한, 컨테이너 안에서 압축 해제를 통해 필요한 파일만 사용할 수 있습니다.
**예시:**
```dockerfile
COPY app.tar.gz /app/
RUN tar -zxvf /app/app.tar.gz -C /app && rm /app/app.tar.gz
```
이 방법은 특히 파일 구조가 복잡하거나 대량의 데이터를 포함하고 있을 때 유용하게 사용할 수 있습니다.
### 10. 이미지에 메타데이터 추가하기
Dockerfile에 LABEL 명령어를 사용해 주요 메타데이터를 추가하면 이미지 관리와 검색이 더 쉬워집니다. 이는 이미지가 서로 다른 팀이나 빌드 파이프라인에서 사용될 때 유용합니다.
**예시:**
```dockerfile
LABEL maintainer="your_email@example.com"
LABEL version="1.0"
LABEL description="This is an optimized Docker image."
```
이렇게 메타데이터를 추가하면 관리가 용이하고, 다양한 태그로 이미지를 명확히 식별할 수 있습니다.

## 결론

Docker 이미지를 최적화하는 작업은 단순히 이미지 크기를 줄이고 배포 속도를 높이는 것뿐만 아니라, 보안성과 자원 효율성까지 향상시킬 수 있는 중요한 과정입니다. 다양한 최적화 방법을 통해 Docker 이미지를 간소화하면 운영 환경에서의 안정성과 관리 효율성이 증가합니다. 특히 다단계 빌드나 캐시 활용, 그리고 도구를 적극 활용하는 전략들은 시간을 절약하고 비용을 줄이는 데 큰 도움이 됩니다. 결과적으로, 최적화된 Docker 이미지는 개발 및 운영의 전체적인 생산성을 높이는 핵심 요소로 자리매김합니다.

## 참고 자료
1. [Docker 공식 문서](https://docs.docker.com/)
2. [Dockerfile 모범 사례](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)