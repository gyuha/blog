---
title: "Hugo를 사용한 Github 블로그.."
date: 2018-11-07T00:20:56+09:00
draft: true
categories: [utillity]
tags: [go,blog,github]
---

## hugo 설치 하기

- [Install Hugo](https://gohugo.io/getting-started/installing/)를 보고 하면 됩니다.
<!--more-->

전 ubuntu를 쓰고 있는 관계로.. 간단하게..

```bash
sudo apt install hugo
```

이렇게 하면 간단하게 설치가 되네요..



## 사이트 만들기

```bash
$ hugo new site blog
Congratulations! Your new Hugo site is created in /home/gyuha/workspace/temp/blog.

Just a few more steps and you're ready to go:

1. Download a theme into the same-named folder.
   Choose a theme from https://themes.gohugo.io/, or
   create your own with the "hugo new theme <THEMENAME>" command.
2. Perhaps you want to add some content. You can add single files
   with "hugo new <SECTIONNAME>/<FILENAME>.<FORMAT>".
3. Start the built-in live server via "hugo server".

Visit https://gohugo.io/ for quickstart guide and full documentation.
$ cd blog
```



## 사이트 실행해 보기

```bash
$ hugo server
ERROR 2018/11/07 00:33:28 port 1313 already in use, attempting to use an available port

                   | EN  
+------------------+----+
  Pages            |  3  
  Paginator pages  |  0  
  Non-page files   |  0  
  Static files     |  0  
  Processed images |  0  
  Aliases          |  0  
  Sitemaps         |  1  
  Cleaned          |  0  

Total in 10 ms
Watching for changes in /home/gyuha/workspace/temp/blog/{content,data,layouts,static}
Watching for config changes in /home/gyuha/workspace/temp/blog/config.toml
Serving pages from memory
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop

```

웹브라우저에서 http://localhost:1313 으로 실행 해 보면 아무것도 안 나온다..



## 테마 설치 하기

이 사이트에서 사용한 스킨을 설치해 보겠습니다.

먼저 `git init`으로 초기화를 해 주고 테마를 받습니다.

```bash
git init
cd themes
git submodule add https://github.com/halogenica/beautifulhugo.git beautifulhugo
cd ..
```

다시 `hugo server `를 해 보면.. 아직도 아무것도 나오지 않습니다.

설정 데이터가 없어서 그럽니다.

```bash
cp themes/beautifulhugo/exampleSite/config.toml .
hugo server -D
```

이렇게 하고 http://localhost:1313으로 실행하면 정상적으로 사이트가 나오는 것을 확인 할 수 있습니다.

그리고, `-D` 옵션을 넣어 줘야 갱신된 글이 보입니다.

`config.toml`을 내가 원하는 형태로 수정해 줍니다.



## 새글 추가 하기

```bash
hugo new post/2018-11-11-start-blog.md
```

위와 같이 추가 하면 새 글이 추가 됩니다.



## GitHub에 올리기

- [Host on GitHub](https://gohugo.io/hosting-and-deployment/hosting-on-github/)를 참고 하면 됩니다.



## Makefile

위 과정을 매번 치기 귀찮아서.. makefile로 만들어 봤음...



```makefile
HUGO = hugo
COMMIT_MESSAGE = "rebuilding site $(shell date +%Y-%m-%d)"


run:
	$(HUGO) server -D

clone:
	rm -rf public
	git clone https://github.com/<USERNAME|ORGANIZATION>/<USERNAME|ORGANIZATION>.github.io.git
	mv gyuha.github.io public

new:
	$(HUGO) new post/$(shell date +%Y-%m-%d)-$(title).md

deploy:
	echo "\033[0;32mDeploying updates to GitHub...\033[0m"

	# Build the project.
	$(HUGO) -D

	cd ./public && git add . && git commit -m $(COMMIT_MESSAGE) && git push

```



----

- 참고 소스 : https://github.com/gyuha/blog



