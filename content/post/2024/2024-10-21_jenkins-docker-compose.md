---
title: "Jenkins Docker Compose 설정 가이드"
date: 2024-10-21T20:13:39+09:00
draft: true
categories: [system]
tags: ["jenkins", "docker", "docker compose", "ci/cd"]
---
Jenkins는 소프트웨어 개발에서 지속적 통합 및 배포(CI/CD)를 위한 강력한 도구입니다. Docker Compose를 사용하여 Jenkins를 설정하면 환경 구성이 간편해지고 일관성 있는 배포가 가능해집니다.

<!--more-->

이 가이드에서는 Docker Compose를 사용하여 Jenkins를 설정하는 방법을 단계별로 설명하겠습니다.

## 1. docker-compose.yml 파일 생성

먼저, 프로젝트 디렉토리에 `docker-compose.yml` 파일을 생성합니다. 이 파일은 Docker Compose가 컨테이너를 어떻게 구성하고 실행할지 정의합니다.

## 2. docker-compose.yml 내용 작성

다음은 Jenkins를 Docker Compose로 실행하기 위한 기본적인 `docker-compose.yml` 파일의 내용입니다:

```yaml
version: '3'
services:
  jenkins:
    image: jenkins/jenkins:lts
    privileged: true
    user: root
    ports:
      - 8080:8080
      - 50000:50000
    container_name: jenkins
    volumes:
      - ./jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
    restart: always
```

이 설정은 Jenkins의 기본적인 실행 환경을 제공합니다. 각 설정의 의미와 중요성에 대해 자세히 살펴보겠습니다.

## 3. 설정 설명

### image: jenkins/jenkins:lts
이 설정은 공식 Jenkins LTS (Long Term Support) 이미지를 사용하도록 지정합니다. LTS 버전은 안정성이 검증된 버전으로, 프로덕션 환경에 적합합니다.

### privileged: true 및 user: root
이 설정들은 Jenkins 컨테이너에 필요한 권한을 부여합니다. 특히 Docker 명령어를 실행하거나 특정 시스템 리소스에 접근해야 할 때 필요합니다. 단, 보안상의 이유로 프로덕션 환경에서는 최소한의 권한만 부여하는 것이 좋습니다.

### ports
- `8080:8080`: Jenkins 웹 인터페이스에 접근하기 위한 포트입니다. 호스트의 8080 포트를 컨테이너의 8080 포트에 매핑합니다.
- `50000:50000`: Jenkins 슬레이브 에이전트와의 통신을 위한 포트입니다. 분산 빌드 환경을 구성할 때 사용됩니다.

### volumes
- `./jenkins_home:/var/jenkins_home`: Jenkins의 데이터와 설정을 호스트 시스템의 `./jenkins_home` 디렉토리에 저장합니다. 이를 통해 컨테이너가 삭제되더라도 데이터를 유지할 수 있습니다.
- `/var/run/docker.sock:/var/run/docker.sock`: 호스트의 Docker 소켓을 Jenkins 컨테이너와 공유합니다. 이를 통해 Jenkins 내에서 Docker 명령어를 실행할 수 있게 됩니다.

### restart: always
시스템이 재시작되거나 Docker 데몬이 재시작될 때 Jenkins 컨테이너를 자동으로 시작하도록 설정합니다.

## 4. Jenkins 실행

설정이 완료되면, `docker-compose.yml` 파일이 있는 디렉토리에서 다음 명령어를 실행하여 Jenkins를 시작합니다:

```bash
docker-compose up -d
```

`-d` 옵션은 백그라운드에서 컨테이너를 실행하도록 합니다.

## 5. Jenkins 초기 설정

Jenkins를 처음 실행하면 초기 설정 과정이 필요합니다. 다음 단계를 따라 설정을 완료하세요:

1. 웹 브라우저에서 `http://localhost:8080`으로 접속합니다.
2. 초기 관리자 비밀번호를 입력해야 합니다. 이 비밀번호는 다음 명령어로 확인할 수 있습니다:
   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. 화면의 지시에 따라 추천 플러그인을 설치하고 관리자 계정을 생성합니다.

## 주의사항 및 추가 고려사항

1. **보안**: 위의 설정은 기본적인 것이며, 프로덕션 환경에서는 추가적인 보안 설정이 필요합니다. 예를 들어, Jenkins에 대한 접근을 제한하거나, HTTPS를 설정하는 것이 좋습니다.

2. **버전 관리**: Jenkins 버전을 업데이트할 때는 `docker-compose.yml`의 이미지 태그를 변경해야 할 수 있습니다. 정기적으로 버전을 확인하고 업데이트하는 것이 좋습니다.

3. **리소스 관리**: Jenkins는 많은 시스템 리소스를 사용할 수 있습니다. 필요에 따라 컨테이너의 리소스 제한을 설정하는 것이 좋습니다.

4. **백업**: `jenkins_home` 디렉토리를 정기적으로 백업하여 데이터 손실에 대비하세요.

5. **플러그인 관리**: 필요한 플러그인만 설치하고 관리하세요. 불필요한 플러그인은 시스템 성능에 영향을 줄 수 있습니다.

6. **네트워크 설정**: 다른 서비스와 연동해야 하는 경우, Docker 네트워크를 적절히 구성하세요.

Jenkins를 Docker Compose로 설정하면 환경 관리가 훨씬 쉬워지고, 개발 팀 전체가 일관된 환경에서 작업할 수 있습니다. 이 가이드를 따라 설정하고, 필요에 따라 추가적인 커스터마이징을 진행하시기 바랍니다. Jenkins를 통한 효율적인 CI/CD 파이프라인 구축으로 개발 프로세스를 한층 개선할 수 있을 것입니다.