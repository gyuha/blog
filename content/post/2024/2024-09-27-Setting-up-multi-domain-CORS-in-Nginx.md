---
title: "Nginx에서 다중 도메인 CORS 설정하기"
date: 2024-09-27T08:18:16+09:00
categories: [os]
draft: true
---

Nginx 서버에서 여러 도메인에 대해 CORS(Cross-Origin Resource Sharing)를 설정하는 방법에 대해 알아보겠습니다.
<!--more-->



`example.co.kr` 도메인과 그 서브도메인들에 대한 CORS 설정을 예로 들어 설명하겠습니다.

## CORS란?

CORS는 웹 브라우저에서 실행되는 스크립트가 다른 출처(도메인, 프로토콜, 포트)의 리소스에 접근할 수 있도록 허용하는 메커니즘입니다. 보안상의 이유로 브라우저는 기본적으로 이를 제한하지만, 서버에서 적절한 CORS 헤더를 설정하면 이 제한을 완화할 수 있습니다.

## Nginx 설정 살펴보기

다음은 Nginx에서 CORS를 설정하는 예시 설정입니다:

```nginx
# CORS 허용 도메인 설정
map $http_origin $cors_origin {
    default "";
    "~^https?://([a-z0-9.-]+\\.)?example\\.co\\.kr(:[0-9]+)?$" $http_origin;
    "~^https?://([a-z0-9.-]+\\.)?sample\\.co\\.kr(:[0-9]+)?$" $http_origin;
}

server {
    listen 443 ssl;
    server_name api.example.co.kr;

    # SSL 설정 (생략)

    location / {
        add_header 'Access-Control-Allow-Origin' '$cors_origin' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, DELETE, PATCH, PUT, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization, X-Requested-With, Accept, Access';
        add_header 'Access-Control-Allow-Credentials' 'true';

        if ($request_method = 'OPTIONS') {
            return 204;
        }

        # 프록시 설정 (생략)
    }
}
```

## 주요 설정 설명

1. **CORS 허용 도메인 설정**:
   ```nginx
   map $http_origin $cors_origin {
       default "";
       "~^https?://([a-z0-9.-]+\\.)?example\\.co\\.kr(:[0-9]+)?$" $http_origin;
   }
   ```
   이 설정은 `example.co.kr` 도메인과 그 서브도메인들에 대해 CORS를 허용합니다. 정규표현식을 사용하여 유연하게 도메인을 매칭합니다.

2. **CORS 헤더 설정**:
   ```nginx
   add_header 'Access-Control-Allow-Origin' '$cors_origin' always;
   ```
   `$cors_origin` 변수를 사용하여 동적으로 허용된 오리진을 설정합니다.

3. **허용된 메서드와 헤더**:
   ```nginx
   add_header 'Access-Control-Allow-Methods' 'GET, POST, DELETE, PATCH, PUT, OPTIONS';
   add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization, X-Requested-With, Accept, Access';
   ```
   허용된 HTTP 메서드와 요청 헤더를 지정합니다.

4. **Credentials 허용**:
   ```nginx
   add_header 'Access-Control-Allow-Credentials' 'true';
   ```
   인증 정보(쿠키, HTTP 인증 등)를 포함한 요청을 허용합니다.

5. **Preflight 요청 처리**:
   ```nginx
   if ($request_method = 'OPTIONS') {
       return 204;
   }
   ```
   OPTIONS 메서드로 오는 preflight 요청에 대해 204 No Content 응답을 반환합니다.

## 결론

이 설정을 통해 `example.co.kr` 도메인과 그 서브도메인들에서 오는 CORS 요청을 안전하게 처리할 수 있습니다. 필요에 따라 정규표현식을 수정하여 다른 도메인도 추가할 수 있습니다.

CORS 설정은 보안과 밀접한 관련이 있으므로, 항상 필요한 도메인만 허용하고 정기적으로 설정을 검토하는 것이 좋습니다.


