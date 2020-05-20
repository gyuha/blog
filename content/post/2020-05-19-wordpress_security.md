---
title: "워드프레스 보안 설정"
date: 2020-05-19T10:37:23+09:00
draft: true
categories: [utillity]
tags: [security,php,wordpress]
---

워드프레스로 만든 홈페이지 보안 적용 정리..

<!--more-->
![WordPress](https://kalkin7.files.wordpress.com/2013/06/wordpress-wide1440.png?w=1024)

5년 전에 워드프레스(wordpress)로 홈페이지를 제작한 적이 있는데, 어느 순간부터 홈페이지가 이상한 사이트로 이동을 하는 겁니다.  처음에는 단순하게 홈페이지를 복구 했는데, 복구해도 계속 같은 증상이 반복이 되었습니다.  그래서 워드프레스 버전이 낮아서 그런가 해서 php를 7.3으로 올리고 워드프레스를 최신으로 업데이트를 했습니다. 하지만 같은 증상이 반복 되는 겁니다. 결국은 기존에 감염된 파일을 찾아내서 삭제하고 보안을 강화하는 형식으로 홈페이지를 복구 했습니다.  이렇게 한달을 운영하면서 보안이 문제가 없어 보여서 여기에 정리해 봅니다.



아래 작업을 시작하기 전에 단계마다 사이트와 DB를 백업 하시면서 하시는걸 추천 드립니다.



## 보안 플러그인 설치

워드프레스 플러그인 추가에서 `security`라고 검색을 해 보면 백여개가 넘는 플러그인들이 검색이 됩니다.  이 중에서 평점이 높고 사용자들이 많이 설치한 플러인 위주로 설치하고 사용해 봤습니다. 그리고 3개의 플러그인을 사용하고 있습니다.

### iThemes Security
Link : [iThemes Security](https://wordpress.org/plugins/better-wp-security/)

가장 많은 도움을 받은 플러그인입니다.  관리자 메뉴에서 `Settings`를 열어 보면 다양한 설정들이 보입니다. 차근차근 하니씩 설정해 주면 됩니다.  대부분의 보안 설정을 진행 할 수 있습니다.

그리고 가장 추천하는 설정은 `File Change Detection`입니다.  사이트에서 파일이 변경된 사항을 추적해서 기록해 주며, 메일로도 알려줍니다. 초기에 세팅을 해 놓고 사이트에 문제가 없는지 확인하는데 도움을 많이 줍니다. 

### Wordfence Security
Link :  [Wordfence Security](https://wordpress.org/plugins/wordfence/)

사이트에 대한 공격을 모니터링해 줍니다. 사이트에 공격이 들어오면 알아서 막아도 주면서 해당 IP를 블럭해서 공격을 막아 줍니다.  관리자 메뉴 중에서 `Live Traffic`이라는 메뉴가 있는데, 여기서  로그인 시도나 해킹 시도에 대한 로그를 조회 해 볼 수 있습니다. 여기를 잘 파악해 보면,  "아~ 이런식으로 해킹을 시도하는구나" 알게 됩니다. 

그리고, 2차 인증(Two-Factor Authentication)기능으로 OTP를 연결해 준다면 로그인 시도에 관련된 공격으로 부터 많이 안전해 집니다.

### Sucuri Security
Link: [Sucuri Security](https://wordpress.org/plugins/sucuri-scanner/)

앞에 2개의 플러그인 기능과 많이 겹치긴 하지만 보조적인 역할로 설치해 줬습니다. 보안 활동 감시 및 멀웨어 검사등의 기능을 합니다. 



이렇게 위 3개의 플러그인에서 중복되는 기능도 있긴 하지만, 혹시나 모를 안정성을 위해서 3개를 설치 했습니다. 

개인적인 의견으로는 [iThemes Security](https://wordpress.org/plugins/better-wp-security)와 [Wordfence Security](https://wordpress.org/plugins/wordfence/)만 설치 해도 충분 할 것으로 보입니다.



## 손으로 벌레 잡기

위 플러그인을 설치하면 멀웨어나 다양한 형태의 해킹 시도를 감지 할 수 있습니다. 하지만 플러그인 만으로도 잡히지 않는 경우들 있습니다. 이럴때 하나씩 잡아야 합니다.

### 의심되는 파일 찾기

```bash
find . -type f -name '*.php' | xargs grep -l "eval *("
find . -type f -name '*.php' | xargs grep -l "base64_decode *("
find . -type f -name '*.php' | xargs grep -l "gzinflate *("
```

[eval](https://www.php.net/manual/en/function.eval.php)은 함수는 php에서 가변 변수를 사용하게 해주는 함수로 가변 변수를 이용해서 다양한 해킹 시도하는 멀웨어 파일에서 자주 사용 됩니다.  `base64_decode`와 `gzinflate`는 함수는 스트링을 난독화 시켜서 사용자가 php파일을 바로 해독하기 어렵도록 해 줍니다.

이렇게 3개의 단어를 검색해서 전혀 쓰이지 않을것 같은 파일이나 의심스러운 파일은 수정하거나 삭제해 주는 것이 좋습니다. 

```bash
find . -type f -name '*.php'  | grep -i '<iframe'
```

php파일에 iframe이 들어 있는지를 검사합니다.



```bash
find wp-content/uploads -type f -iname '*.jpg' | xargs grep -i php
```

jpg 파일이지만 안에 php가 들어있는 멀웨어 공격을 검사합니다.



### 업로드 폴더 검사

업로드 폴더에 올라간 php실행 파일을 찾아 수상한 파일들은 삭제를 해 줍니다.

```bash
find wp-content/uploads -type f -name '*.php'
```



### 최근에 변경된 파일 찾기

```bash
find . -type f -name '*.php' -mtime -7
```

최근 7일간 php 파일중에서 변경되 파일의 목록을 출력해 줍니다.



## .htaccess 편집하기

`.htaccess`를 편집하면 사이트 접근을 제한 할 수 있습니다. 보안 플러그인에서도 `.htaccess`파일을 편집해 줍니다.

하지만, 일부는 직접 수정해서 원하는 대로 설정을 할 수 있습니다.



### 디렉토리 브라우징 끄기

대부분은 빈 index.php 파일을 만들어서 빈 디렉토리의 브라우징을 못 하도록 처리를 해 두긴 하지만, `.htaccess`파일에서도 이 기능을 끌 수 있습니다.

```
Options -Indexes
```



### wp-config.php 파일을 보호해 주기

`wp-config.php`파일에는 사이트의 중요한 정보를 가지고 있습니다. 웹에서 바로 접근을 할 수 없도록 설정해 줍니다. `.htaccess`파일에 아래의 내용을 추가해 줍니다.

```xml
<files wp-config.php>
order allow,deny
deny from all
</files>
```



### XML-RPC파일 접근 끄기

xmlrpc.php 파일은 워드프레스 서드파트 앱에서 사이트를 접근하도록 해 줍니다. 만약에 서드파티 앱을 사용하지 않는다면 이 기능을 꺼 주는게 좋습니다.  `.htaccess`파일에 아래의 내용을 추가해 줍니다.

```xml
<Files xmlrpc.php>
order deny,allow
deny from all
</Files>
```

[iThemes Security](https://wordpress.org/plugins/better-wp-security/)에서도 설정이 가능 합니다.



### 스크립트 인젝션 끄기

해커가 깆존 php문서에 악성코드를 삽입하지 못 하도록 스크립트 삽입을 허용하지 않습니다. `.htaccess`파일에 mode_rewrite 부분에 아래의 내용을 추가해 줍니다.

```xml
<IfModule mod_rewrite.c>
...
Options +FollowSymLinks
RewriteEngine On
RewriteCond %{QUERY_STRING} (<|%3C).*script.*(>|%3E) [NC,OR]
RewriteCond %{QUERY_STRING} GLOBALS(=|[|%[0-9A-Z]{0,2}) [OR]
RewriteCond %{QUERY_STRING} _REQUEST(=|[|%[0-9A-Z]{0,2})
RewriteRule ^(.*)$ index.php [F,L]
</IfModule>
```



### 특정 ip에서만 wp-admin 폴더를 접근 허용

wp-admin은 관리자 폴더 입니다. 특정 ip에서만 wp-admin을 접근 할 수 있도록 제한 합니다.

wp-admin폴더에 `.htaccess`파일을 만들고 아래 내용을 추가해 줍니다.

```xml
<Limit GET POST>
order deny,allow
deny from all
allow from 1.2.3.4
allow from 1.2.3.5
</Limit>
```

기본적으로 접근을 제한하고, 그리고 관리자 메뉴에 접근해야 하는 ip만을 위와 같이 등록해 줍니다.



### 특정 워드프레스 폴더에서 php 실행 방지하기

몇몇 해커들은 워드프레스 사이트의 업로드 기능을 이용해서 백도어를 설치하는 해킹을 시도 합니다. 이렇게 설치된 파일이 직접 실행이 않도록 `/wp-include/` ,`/wp-content/uploads/` 폴더등에서는 php가 실행되지 않도록 처리해 줄 수 있습니다.

`/wp-include/` 폴더와 `/wp-content/uploads` 폴더에 `.htaccess`파일을 생성하고 아래와 같이 넣어 줍니다.

```xml
<Files *.php>
deny from all
</Files>
```



## 파일과 폴더의 접근 권한 설정하기

파일과 폴더에 좀 더 엄격한 접근 권한 설정을 해서 파일이 변경 되지 않도록 방지 합니다.

각 폴더의 권장하는 권한은 아래와 같습니다.

| 경로               | 권한 |
| ------------------ | ---- |
| /                  | 755  |
| .htaccess          | 444  |
| wp-includes        | 755  |
| wp-admin           | 755  |
| wp-admin/js        | 755  |
| wp-content         | 755  |
| wp-content/themes  | 755  |
| wp-content/plugins | 755  |
| wp-content/uploads | 755  |
| wp-config.php      | 444  |



## 그외 팁

### 바이러스 검사하기

되도록이면 유명하거나 검증된 플러그인이나 테마를 사용하는 것이 좋습니다. 하지만 꼭 사용하고 싶다면 플러그인 또는 테마를 사용하기 전에 바이러스 검사를 해 볼 수 있습니다. 해당 플러그인이나 테마를 다운로드 받고 나서  [VirusTotal](https://www.virustotal.com/#/home/upload) 사이트에서 검사를 해 보면 일차적으로 멀웨어가 있는지 체크가 가능 합니다.







## 정리

워드프레스는 정말 많은 사이트에서 사용되는 콘텐츠 관리 플랫폼입니다. 전체 웹사이트중 36%가 워드프레스로 구축 되어 있을 정도입니다.  많은 사이트에서 사용하는 만큼 취약점이 발견되면 바로 업데이트가 이루어 지고 있어서 워드프레스 자체만으로는 보안에 취약하지는 않습니다. 

하지만,  간단한 검색만으로 사이트가 워드프레스로 제작되어 있는지 확인이 가능하며, 워드프레스로 제작이 되어 있다면, 이전 버전들에서 노출된 보안의 헛점을 이용해서 공격하는 많은 방법이 공개 되어 있어서, 공격의 대상이 되기 쉽니다. 그리고, 누구나 만들 수 있는 플러그인과 테마로 인해서, 개발자가 본의 아니게 보안에 취약한 플러그인이 만들어 질 수도 있으며, 이런 취약점이 노출이 되면 사이트 보안에 문제가 발생하게 됩니다.

워드프레스는 아래 3가지 정도면 잘 지키면 보안에 별 문제가 없어 보입니다.

1. 워드프레스, 테마, 플러그인을 항상 최신 버전으로 유지 한다.
2. 플러그인은 되도록이면 검증된 플러그인으로 설치하고 최소한으로 설치한다.
3. 보안 플러그인은 꼭 사용한다.

이렇게 3가지 정도면 보안에 문제가 발생하지 않는거 같습니다.

그리고 추가로 혹시나 모를 문제를 방지하기 위해서 정기적인 백업도 잊지 말아야 합니다.

복구 시점을 만들어 주는것 뿐만 아니라.. 변경 사항을 비교해 보면 보안의 취약점을 찾는데 도움이 됩니다.



## 참고자료

* ['만만한 타깃' 워드프레스 보안 강화 툴·방법 총정리](http://www.ciokorea.com/t/21999/%EA%B0%9C%EB%B0%9C%EC%9E%90/114510)
* [워드프레스 보안 강화를 위한 기본적인 세 가지 방법](https://www.thewordcracker.com/basic/%EC%9B%8C%EB%93%9C%ED%94%84%EB%A0%88%EC%8A%A4-%EB%B3%B4%EC%95%88-%EA%B0%95%ED%99%94%EB%A5%BC-%EC%9C%84%ED%95%9C-%EA%B8%B0%EB%B3%B8%EC%A0%81%EC%9D%B8-%EC%84%B8-%EA%B0%80%EC%A7%80-%EB%B0%A9%EB%B2%95/)
* [워드프레스 웹사이트 보안을 위한 10가지 노하우](https://m.post.naver.com/viewer/postView.nhn?volumeNo=14008515&memberNo=9711586)
* [The Ultimate WordPress Security Guide – Step by Step (2020)](https://www.wpbeginner.com/wordpress-security/)
* [12 Most Useful .htaccess Tricks for WordPress](https://www.wpbeginner.com/wp-tutorials/9-most-useful-htaccess-tricks-for-wordpress/)
* [WordPress Security – 19 Steps to Lock Down Your Site](https://kinsta.com/blog/wordpress-security/)
* [Comprehensive WordPress Malware Removal Guide](https://www.webarxsecurity.com/comprehensive-wordpress-malware-removal-guide/)
* [How to Tell if Your PHP Site has been Hacked or Compromised](https://www.gregfreeman.io/2013/how-to-tell-if-your-php-site-has-been-compromised/)