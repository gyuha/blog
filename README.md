# Hugo Blog

## Project Cone

```bash
git clone https://github.com/gyuha/blog.git
cd blog
git submodule init
git submodule update
git submodule foreach git checkout master
```

## Hugo 설치 하기

- [Hugo Install and Use Themes](https://gohugo.io/themes/installing-and-using-themes/)

### Ubuntu
```bash
sudo apt install hugo
```


### 새글 쓰기

```bash
make new title=[글제목]
```

또는

```bash
hugo new post/[글제목].md
```



## 서버 실행하기

```bash
make run
```

또는

```bash
hugo server -D
```



# 서버 배포하기

```bash
make deploy
```



## 사용중인 theme

- [Beautiful Hugo - A port of Beautiful Jekyll Theme](https://github.com/halogenica/beautifulhugo)
