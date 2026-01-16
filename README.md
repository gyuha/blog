# Hugo Blog

## Project Clone

```bash
git clone --recurse-submodules https://github.com/gyuha/blog.git
cd blog
```

> 이미 clone 한 경우 submodule 초기화:
> ```bash
> git submodule update --init --recursive
> ```

## Hugo 설치 하기

- [Hugo install](https://gohugo.io/installation/)


### Ubuntu
```bash
sudo apt install hugo
```

## Task 설치 하기

- [Task - A task runner / simpler Make alternative](https://taskfile.dev/)

### macOS
```bash
brew install go-task
```

### Ubuntu/Debian
```bash
sudo snap install task --classic
```

## 사용 가능한 명령어

```bash
task --list
```

| 명령어 | 설명 |
|--------|------|
| `task run` | Hugo 서버 실행 (drafts 포함) |
| `task dev` | Hugo 서버 실행 (drafts 포함, fast render 비활성화) |
| `task clone` | GitHub Pages 저장소를 public 폴더로 클론 |
| `task new -- [글제목]` | 새 포스트 생성 |
| `task deploy` | GitHub에 빌드 및 배포 |

### 새글 쓰기

```bash
task new -- my-post-title
```

또는

```bash
hugo new post/[글제목].md
```

## 서버 실행하기

```bash
task run
```

또는

```bash
hugo server -D
```

## 서버 배포하기

```bash
task deploy
```

## 사용중인 theme

- [Beautiful Hugo - A port of Beautiful Jekyll Theme](https://github.com/halogenica/beautifulhugo)
