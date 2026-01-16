---
title: "linux mpv 자막 번역기"
date: 2026-01-16T22:04:30+09:00
draft: true
description: "mpv 플레이어에서 실시간으로 자막을 번역해주는 도구를 소개합니다. Linux 환경에서 mpv와 함께 사용하여 외국어 영상 시청 시 편리한 번역 기능을 제공합니다."
tags: ["mpv", "자막 번역", "Linux", "동영상 플레이어"]
---

mpv는 강력한 오픈소스 동영상 플레이어로, 다양한 기능을 플러그인 형태로 확장할 수 있습니다. 이번 글에서는 mpv에서 자막을 실시간으로 번역해주는 Lua 스크립트를 소개합니다. 이 스크립트는 `trans` 명령줄 도구를 사용하여 자막을 번역하며, Linux 환경에서 mpv와 함께 사용할 수 있습니다.

<!--more-->

설치 방법과 사용법은 다음과 같습니다.

## 사전 준비
1. **mpv 설치**: Linux 배포판에 따라 패키지 관리자를 사용하여 mpv를 설치합니다.
   ```bash
   sudo apt install mpv  # Ubuntu/Debian
   sudo dnf install mpv  # Fedora
   ```
2. **trans 도구 설치**: `trans`는 다양한 번역 서비스를 지원하는 명령줄 번역기입니다. 다음 명령어로 설치할 수 있습니다.
   ```bash
   sudo apt install translate-shell  # Ubuntu/Debian
   ```  
    또는 [공식 GitHub 저장소](https://github.com/soimort/translate-shell)에서 최신 버전을 확인할 수 있습니다。

## 스크립트 설치 및 설정
아래 Lua 스크립트를 `~/.config/mpv/scripts/` 디렉토리에 `auto_translate.lua`라는 이름으로 저장합니다.

```lua
local mp = require 'mp'
local enabled = false

-- OSD 오버레이 생성
local ov = mp.create_osd_overlay("ass-events")

function translation_callback(success, result, error)
    if success and result.status == 0 then
        -- [[ 스타일 설정 ]]
        -- \an2 : 하단 중앙 정렬
        -- \fs60 : 글자 크기
        -- \bord2 : 테두리 두께 (검은색)
        -- \1c&HFFFFFF& : 글자색 (흰색)
        local style = "{\\an2}{\\fs60}{\\bord2}"
        
        -- 줄바꿈을 공백으로 변경
        local clean_text = result.stdout:gsub("\n", " ")

        ov.data = style .. clean_text
        ov:update()
    end
end

function on_subtitle_change(name, text)
    if not enabled then return end

    if not text or text == "" then
        ov.data = ""
        ov:update()
        return
    end

    text = text:gsub("\n", " ")

    local cmd = {
        name = "subprocess",
        args = { "trans", "-b", "-t", "ko", text },
        capture_stdout = true
    }
    
    mp.command_native_async(cmd, translation_callback)
end

function toggle_translation()
    enabled = not enabled
    if enabled then
        mp.set_property("sub-visibility", "no")
        mp.osd_message("자동 번역 ON (Shift+t로 끄기)", 2)
        
        local current_text = mp.get_property("sub-text")
        if current_text then on_subtitle_change("sub-text", current_text) end
    else
        mp.set_property("sub-visibility", "yes")
        ov.data = ""
        ov:update()
        mp.osd_message("자동 번역 OFF", 2)
    end
end

mp.observe_property("sub-text", "string", on_subtitle_change)

-- [[ 단축키 변경됨: Shift + t (대문자 T) ]]
mp.add_key_binding("T", "toggle_auto_translation", toggle_translation)
```

## 사용법

1. mpv로 동영상을 재생합니다.
2. 자막이 표시되는 동안 `Shift + t` 키를 눌러 자동 번역 기능을 켜거나 끕니다.
3. 자막이 번역되어 화면 하단에 표시됩니다.

## 함께 보기

- [mpv 공식 문서](https://mpv.io/manual/stable/)
- [translate-shell GitHub](https://github.com/soimort/translate-shell)

