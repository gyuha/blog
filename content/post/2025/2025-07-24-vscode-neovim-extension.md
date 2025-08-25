---
title: "VSCode에서 Neovim Extension 설정하기: macOS & Windows 가이드"
date: 2025-07-24T23:17:58+09:00
draft: false
categories: [VSCode, Neovim, Vim]
tags: [vscode, neovim, vim, macos, windows, hop.nvim]
---

## Vim에서 Neovim으로 전향한 이유

VSCode에서 Vim extension을 오랫동안 사용해왔습니다. Vim의 강력한 편집 기능을 VSCode에서도 사용할 수 있다는 점은 매우 매력적이었죠. 하지만 한 가지 치명적인 문제가 있었습니다. 바로 **한글 입력 시 타이밍이 밀리는 현상**이었습니다.
<!--more-->

한글을 빠르게 타이핑하다 보면 글자가 제대로 입력되지 않거나, 입력 순서가 뒤바뀌는 등의 문제가 자주 발생했습니다. 이는 작업 효율성을 크게 떨어뜨렸고, 결국 대안을 찾게 되었습니다. 그 대안이 바로 **VSCode Neovim Extension**입니다.

Neovim Extension은 실제 Neovim 프로세스를 백그라운드에서 실행하여 VSCode와 통신하는 방식으로 작동합니다. 이로 인해 Vim extension보다 더 안정적이고, 한글 입력 문제도 해결되었습니다.

## macOS에서 Neovim 설치하기

### 1. Homebrew를 통한 설치

macOS에서는 Homebrew를 통해 쉽게 Neovim을 설치할 수 있습니다.

```bash
# Homebrew가 설치되어 있지 않다면 먼저 설치
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Neovim 설치
brew install neovim
```

### 2. 설치 확인

```bash
nvim --version
```

정상적으로 설치되었다면 Neovim 버전 정보가 출력됩니다.

## Windows에서 Neovim 설치하기

### 1. Chocolatey를 통한 설치

Windows에서는 Chocolatey 패키지 매니저를 사용하는 것이 가장 간편합니다.

```powershell
# PowerShell을 관리자 권한으로 실행 후
# Chocolatey가 설치되어 있지 않다면 먼저 설치
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Neovim 설치
choco install neovim
```

### 2. Scoop을 통한 설치 (대안)

Scoop을 선호한다면 다음과 같이 설치할 수 있습니다.

```powershell
# Scoop 설치
iwr -useb get.scoop.sh | iex

# Neovim 설치
scoop install neovim
```

### 3. 수동 설치

공식 GitHub 릴리즈 페이지에서 직접 다운로드할 수도 있습니다.
1. [Neovim GitHub Releases](https://github.com/neovim/neovim/releases)에서 최신 Windows 버전 다운로드
2. zip 파일 압축 해제
3. 시스템 환경 변수 PATH에 `nvim.exe`가 있는 폴더 경로 추가

## VSCode Neovim Extension 설치 및 설정

### 1. Extension 설치

VSCode Extension 마켓플레이스에서 "vscode-neovim"을 검색하여 설치합니다.

### 2. Extension 설정

`settings.json`에 다음 설정을 추가합니다:

```json
{
  // Neovim 실행 파일 경로 (필요한 경우)
  "vscode-neovim.neovimExecutablePaths.darwin": "/opt/homebrew/bin/nvim",
  "vscode-neovim.neovimExecutablePaths.win32": "C:\\tools\\neovim\\nvim-win64\\bin\\nvim.exe",
  
  // 기타 유용한 설정
  "vscode-neovim.neovimInitVimPaths.darwin": "$HOME/.config/nvim/init.lua",
  "vscode-neovim.neovimInitVimPaths.win32": "$HOME/AppData/Local/nvim/init.lua"
}
```

## Neovim 설정 파일 작성

### 1. 설정 파일 위치

- **macOS/Linux**: `~/.config/nvim/init.lua`
- **Windows**: `~/AppData/Local/nvim/init.lua`

### 2. 기본 설정 파일 생성

```bash
# macOS/Linux
mkdir -p ~/.config/nvim
touch ~/.config/nvim/init.lua

# Windows (PowerShell)
New-Item -Path "$env:LOCALAPPDATA\nvim" -ItemType Directory -Force
New-Item -Path "$env:LOCALAPPDATA\nvim\init.lua" -ItemType File -Force
```

### 3. Packer 플러그인 매니저 설치

Neovim의 플러그인을 관리하기 위해 Packer를 먼저 설치해야 합니다:

```bash
# macOS/Linux
git clone --depth 1 https://github.com/wbthomason/packer.nvim \
  ~/.local/share/nvim/site/pack/packer/start/packer.nvim

# Windows (PowerShell)
git clone --depth 1 https://github.com/wbthomason/packer.nvim `
  "$env:LOCALAPPDATA\nvim-data\site\pack\packer\start\packer.nvim"
```

### 4. init.lua 작성

다음은 제가 사용하는 `init.lua` 설정입니다:

```lua
-- Packer 설치 (플러그인 매니저)
local ensure_packer = function()
  local fn = vim.fn
  local install_path = fn.stdpath('data')..'/site/pack/packer/start/packer.nvim'
  if fn.empty(fn.glob(install_path)) > 0 then
    fn.system({'git', 'clone', '--depth', '1', 'https://github.com/wbthomason/packer.nvim', install_path})
    vim.cmd [[packadd packer.nvim]]
    return true
  end
  return false
end

local packer_bootstrap = ensure_packer()

-- 플러그인 설정
require('packer').startup(function(use)
  use 'wbthomason/packer.nvim'
  use {
    'easymotion/vim-easymotion'
  }
end)

-- OS별 클립보드 설정
if vim.fn.has('win32') == 1 then
  vim.opt.clipboard = "unnamed,unnamedplus"
elseif vim.fn.has('macunix') == 1 then
  vim.opt.clipboard = "unnamedplus"
end

vim.g.mapleader = ","        -- Leader 키 설정

-- EasyMotion 키맵 설정
local opts = { noremap = true, silent = true }

-- EasyMotion 키맵들
vim.api.nvim_set_keymap('n', '<leader><leader>f', '<Plug>(easymotion-bd-f)', {})
vim.api.nvim_set_keymap('n', '<leader><leader>w', '<Plug>(easymotion-w)', {})
vim.api.nvim_set_keymap('n', '<leader><leader>b', '<Plug>(easymotion-b)', {})
vim.api.nvim_set_keymap('n', '<leader><leader>j', '<Plug>(easymotion-j)', {})
vim.api.nvim_set_keymap('n', '<leader><leader>k', '<Plug>(easymotion-k)', {})

-- Y를 누르면 라인 yank가 되도록 설정
vim.api.nvim_set_keymap('n', 'Y', 'yy', { noremap = true })

-- Visual Block 모드를 위한 여러 키 바인딩
vim.api.nvim_set_keymap('n', '<C-q>', '<C-v>', opts)
vim.api.nvim_set_keymap('v', '<C-q>', '<C-v>', opts)

-- 추가 대안 (leader 키 사용)
vim.api.nvim_set_keymap('n', '<leader>v', '<C-v>', opts)

-- 상태라인에 모드 표시 (선택사항)
vim.opt.showmode = true

-- 완성 메뉴 메시지 숨기기
vim.opt.shortmess:append("c")

vim.opt.ignorecase = true
vim.opt.smartcase = true
```

### 5. 플러그인 설치

init.lua 파일을 작성한 후, Neovim을 실행하여 플러그인을 설치해야 합니다:

```bash
# Neovim 실행
nvim

# Neovim 내에서 다음 명령어 입력
:PackerInstall
```

처음 실행 시 Packer가 자동으로 설치되며, 이후 hop.nvim을 포함한 설정된 플러그인들이 설치됩니다. 설치가 완료되면 Neovim을 재시작하세요.

## hop.nvim 플러그인 사용법

### 왜 hop.nvim인가?

VSCode의 Vim Extension을 사용할 때는 EasyMotion이라는 훌륭한 기능이 내장되어 있었습니다. 하지만 Neovim Extension으로 전환하면서 이 기능이 없어진 것을 발견했습니다. EasyMotion은 화면에 보이는 텍스트로 빠르게 이동할 수 있게 해주는 필수적인 기능이었기에, 이를 대체할 플러그인이 필요했습니다.

hop.nvim은 EasyMotion의 Neovim 버전으로, 동일한 기능을 제공합니다. 화면의 특정 위치로 빠르게 이동할 수 있게 해주는 이 플러그인은 생산성 향상에 큰 도움이 됩니다.

### 사용법

- `,,f`: 화면의 모든 단어로 점프
- `,,w`: 커서 이후의 단어로 점프
- `,,b`: 커서 이전의 단어로 점프
- `,,j`: 아래쪽 라인으로 점프
- `,,k`: 위쪽 라인으로 점프

## 키맵 및 클립보드 설정 설명

### Leader 키
`,`를 Leader 키로 설정했습니다. 이는 사용자 정의 단축키의 prefix로 사용됩니다.

### 클립보드 통합
OS별로 시스템 클립보드와 Neovim의 클립보드를 통합했습니다. 이제 `y`로 복사한 내용을 다른 프로그램에서도 붙여넣을 수 있습니다.

### Visual Block 모드
일부 터미널에서 `Ctrl+V`가 붙여넣기로 사용되는 경우를 위해 `Ctrl+Q`를 Visual Block 모드로 매핑했습니다.

## 마무리

VSCode Neovim Extension을 사용하면 Vim의 강력한 기능을 VSCode에서 안정적으로 사용할 수 있습니다. 특히 한글 입력 문제가 해결되어 한국어로 작업하는 개발자들에게 큰 도움이 될 것입니다.

설정이 완료되면 VSCode를 재시작하고, Neovim의 모든 기능을 VSCode에서 즐기세요!
