#!/usr/bin/env python3
"""
Threads 미디어 URL을 마크다운 이미지 태그로 변환하는 헬퍼 함수

이 모듈은 Threads.net 포스트에서 추출한 미디어 정보를
마크다운 형식으로 변환하는 유틸리티 함수를 제공합니다.
"""

import re
from typing import List, Dict, Optional
from urllib.parse import urlparse


def process_image(media_url: str, alt_text: str = "이미지") -> str:
    """
    이미지 URL을 마크다운 이미지 태그로 변환

    Args:
        media_url: 이미지 URL
        alt_text: 대체 텍스트 (기본값: "이미지")

    Returns:
        마크다운 이미지 태그 문자열

    Examples:
        >>> process_image("https://example.com/image.jpg", "예제 이미지")
        '![예제 이미지](https://example.com/image.jpg)'
    """
    if not media_url:
        return ""
    return f"![{alt_text}]({media_url})"


def process_video(media_url: str, title: str = "비디오") -> str:
    """
    비디오 URL을 마크다운 링크로 변환

    Threads 비디오는 직접 임베드가 어려우므로 링크로 제공

    Args:
        media_url: 비디오 URL
        title: 링크 텍스트 (기본값: "비디오")

    Returns:
        마크다운 링크 문자열

    Examples:
        >>> process_video("https://example.com/video.mp4", "시영영상 보기")
        '[시영영상 보기](https://example.com/video.mp4)'
    """
    if not media_url:
        return ""
    return f"[{title}]({media_url})"


def process_carousel(media_urls: List[str], descriptions: Optional[List[str]] = None) -> str:
    """
    캐러셀(여러 이미지)을 마크다운 목록으로 변환

    Args:
        media_urls: 이미지 URL 리스트
        descriptions: 각 이미지의 설명 리스트 (선택사항)

    Returns:
        마크다운 형식의 이미지 갤러리 문자열

    Examples:
        >>> urls = ["img1.jpg", "img2.jpg"]
        >>> process_carousel(urls, ["첫번째", "두번째"])
        '### 이미지 갤러리\\n\\n1. ![첫번째](img1.jpg)\\n2. ![두번째](img2.jpg)'
    """
    if not media_urls:
        return ""

    lines = ["### 이미지 갤러리", ""]

    for i, url in enumerate(media_urls, 1):
        if descriptions and i - 1 < len(descriptions):
            alt_text = descriptions[i - 1]
        else:
            alt_text = f"이미지 {i}"
        lines.append(f"{i}. {process_image(url, alt_text)}")

    return "\n".join(lines)


def extract_media_urls(media_data: List[Dict]) -> List[str]:
    """
    Threads API 응답에서 미디어 URL 추출

    Args:
        media_data: Threads API의 media 데이터 리스트

    Returns:
        미디어 URL 리스트

    Examples:
        >>> data = [{"image_versions2": {"candidates": [{"url": "img.jpg"}]}}]
        >>> extract_media_urls(data)
        ['img.jpg']
    """
    urls = []

    for media in media_data:
        # 이미지 URL 추출 (Threads API 구조 기반)
        if "image_versions2" in media:
            candidates = media["image_versions2"].get("candidates", [])
            if candidates:
                # 가장 높은 해상도 선택 (보통 첫 번째)
                urls.append(candidates[0]["url"])

        # 비디오 URL 추출
        elif "video_versions" in media:
            candidates = media["video_versions"]
            if candidates:
                urls.append(candidates[0]["url"])

    return urls


def is_valid_url(url: str) -> bool:
    """
    URL 유효성 검사

    Args:
        url: 검사할 URL 문자열

    Returns:
        유효한 URL이면 True, 아니면 False
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def sanitize_alt_text(text: str, max_length: int = 100) -> str:
    """
    대체 텍스트 정제 (길이 제한 및 특수문자 제거)

    Args:
        text: 원본 텍스트
        max_length: 최대 길이 (기본값: 100)

    Returns:
        정제된 대체 텍스트
    """
    if not text:
        return "이미지"

    # 대괄호 제거 (마크다운 충돌 방지)
    text = text.replace("[", "").replace("]", "")

    # 길이 제한
    if len(text) > max_length:
        text = text[:max_length].rsplit(" ", 1)[0] + "..."

    return text.strip()


def generate_media_section(media_items: List[Dict], post_text: Optional[str] = None) -> str:
    """
    포스트의 모든 미디어를 마크다운 섹션으로 생성

    Args:
        media_items: 미디어 아이템 리스트
        post_text: 포스트 본문 (설명 추출용)

    Returns:
        마크다운 형식의 미디어 섹션 문자열

    Examples:
        >>> items = [{"image_versions2": {"candidates": [{"url": "img.jpg"}]}}]
        >>> generate_media_section(items)
        '## 미디어\\n\\n![이미지](img.jpg)'
    """
    if not media_items:
        return ""

    media_urls = extract_media_urls(media_items)

    if not media_urls:
        return ""

    # 단일 이미지
    if len(media_urls) == 1:
        return f"## 미디어\n\n{process_image(media_urls[0], sanitize_alt_text(post_text or '이미지'))}"

    # 캐러셀 (여러 이미지)
    return f"## 미디어\n\n{process_carousel(media_urls)}"


def process_thread_media(thread_data: Dict) -> str:
    """
    전체 스레드 데이터의 미디어를 처리

    Args:
        thread_data: Threads API 응답 데이터

    Returns:
        모든 포스트의 미디어를 포함한 마크다운 섹션
    """
    all_media = []

    # 각 포스트의 미디어 수집
    if "thread_items" in thread_data:
        for item in thread_data["thread_items"]:
            if "media" in item:
                all_media.extend(item["media"])

    return generate_media_section(all_media)


if __name__ == "__main__":
    # 테스트 코드
    print("=== process_media.py 테스트 ===\n")

    # 이미지 처리 테스트
    test_image_url = "https://scontent.cdninstagram.com/v/t51.2885-15/123456789_0.jpg"
    print("이미지 처리:")
    print(process_image(test_image_url, "테스트 이미지"))
    print()

    # 캐러셀 처리 테스트
    test_urls = [
        "https://example.com/img1.jpg",
        "https://example.com/img2.jpg",
        "https://example.com/img3.jpg"
    ]
    print("캐러셀 처리:")
    print(process_carousel(test_urls, ["첫 번째", "두 번째", "세 번째"]))
    print()

    # URL 유효성 검사 테스트
    print("URL 유효성 검사:")
    print(f"유효한 URL: {is_valid_url('https://example.com/image.jpg')}")
    print(f"잘못된 URL: {is_valid_url('not-a-url')}")
    print()

    # 대체 텍스트 정제 테스트
    print("대체 텍스트 정제:")
    long_text = "이것은 매우 긴 대체 텍스트입니다. 긴 텍스트는 마크다운에서 가독성을 해칠 수 있으므로 적절한 길이로 잘라야 합니다."
    print(f"원본: {long_text}")
    print(f"정제: {sanitize_alt_text(long_text, 50)}")
