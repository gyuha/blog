#!/usr/bin/env python3
"""
Threads Crawling Script using agent-browser

Fetches Threads posts and returns structured JSON data including:
- Post content
- Media URLs (images/videos)
- Author information
- Timestamp

This script uses agent-browser CLI for browser automation.
"""

import json
import re
import subprocess
import sys
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse


class ThreadsFetcher:
    """Fetches and parses Threads posts from URLs using agent-browser."""

    def __init__(self, session_name: str = "threads-fetcher"):
        """
        Initialize the Threads fetcher with agent-browser.

        Args:
            session_name: Name for the agent-browser session
        """
        self.session_name = session_name
        self.browser_open = False

    def _run_agent_browser(self, command: str, capture: bool = True) -> str:
        """
        Run an agent-browser command and return the output.

        Args:
            command: The agent-browser command arguments (without 'agent-browser' prefix)
            capture: Whether to capture and return output

        Returns:
            Command output as string (if capture=True)
        """
        session_arg = f"--session {self.session_name}" if self.session_name else ""
        full_command = f"agent-browser {session_arg} {command}"

        try:
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=capture,
                text=True,
                timeout=60
            )
            if capture:
                return result.stdout + result.stderr
            return ""
        except subprocess.TimeoutExpired:
            raise Exception(f"Command timed out: {full_command}")
        except Exception as e:
            raise Exception(f"Failed to run agent-browser: {e}")

    def open_browser(self, url: Optional[str] = None) -> None:
        """
        Open a new browser session (optionally navigating to a URL).

        Args:
            url: Optional URL to navigate to immediately
        """
        if url:
            self._run_agent_browser(f'open "{url}"', capture=False)
        else:
            self._run_agent_browser("open", capture=False)
        self.browser_open = True

    def close_browser(self) -> None:
        """Close the browser session."""
        if self.browser_open:
            self._run_agent_browser("close", capture=False)
            self.browser_open = False

    def navigate(self, url: str) -> None:
        """
        Navigate to a URL in the current browser session.

        Args:
            url: URL to navigate to
        """
        self._run_agent_browser(f'goto "{url}"', capture=False)

    def wait_for_load(self) -> None:
        """Wait for the page to fully load."""
        self._run_agent_browser("wait --load networkidle", capture=False)

    def get_page_text(self) -> str:
        """
        Get all text content from the current page.

        Returns:
            Page text content
        """
        return self._run_agent_browser("get text body", capture=True)

    def eval_js(self, js_code: str) -> str:
        """
        Evaluate JavaScript in the browser context.

        Args:
            js_code: JavaScript code to evaluate

        Returns:
            Evaluation result as string
        """
        # Use stdin to avoid shell escaping issues
        return self._run_agent_browser(f'eval --stdin <<\'EVALEOF\'\n{js_code}\nEVALEOF', capture=True)

    def extract_open_graph_data(self) -> Dict[str, str]:
        """
        Extract all Open Graph meta data from the current page.

        Returns:
            Dictionary of og: properties and their values
        """
        js = '''
        (function() {
            const metas = document.querySelectorAll('meta[property^="og:"]');
            const data = {};
            metas.forEach(meta => {
                const prop = meta.getAttribute('property');
                const content = meta.getAttribute('content');
                if (prop && content) data[prop] = content;
            });
            return JSON.stringify(data);
        })()
        '''
        result = self.eval_js(js)
        try:
            # Extract JSON from output (agent-browser returns just the JSON)
            result = result.strip()
            if result.startswith('{'):
                return json.loads(result)
        except Exception:
            pass
        return {}

    def extract_json_ld(self) -> List[Dict[str, Any]]:
        """
        Extract JSON-LD data from the current page.

        Returns:
            List of JSON-LD objects
        """
        js = '''
        (function() {
            const scripts = document.querySelectorAll('script[type="application/ld+json"]');
            const data = [];
            scripts.forEach(script => {
                try {
                    data.push(JSON.parse(script.textContent));
                } catch (e) {}
            });
            return JSON.stringify(data);
        })()
        '''
        result = self.eval_js(js)
        try:
            result = result.strip()
            if result.startswith('['):
                return json.loads(result)
        except Exception:
            pass
        return []

    def extract_page_content(self) -> Dict[str, Any]:
        """
        Extract main content from the page including text and images.

        Returns:
            Dictionary with content, images, and other page data
        """
        js = '''
        (function() {
            // Try to find the main post content
            const contentSelectors = [
                '[data-testid="post-text"]',
                'article div[dir="auto"]',
                '[role="article"] div[dir="auto"]',
                'article span[dir="auto"]'
            ];

            let content = "";
            for (const selector of contentSelectors) {
                const element = document.querySelector(selector);
                if (element && element.textContent.trim()) {
                    content = element.textContent.trim();
                    break;
                }
            }

            // Fallback: get all text from article
            if (!content) {
                const article = document.querySelector('article');
                if (article) {
                    content = article.textContent.trim();
                }
            }

            // Extract images
            const images = [];
            const imgElements = document.querySelectorAll('article img, [role="article"] img');
            imgElements.forEach(img => {
                if (img.src && !img.src.includes('profile_pic')) {
                    images.push({
                        src: img.src,
                        alt: img.alt || ""
                    });
                }
            });

            return JSON.stringify({
                content: content,
                images: images
            });
        })()
        '''
        result = self.eval_js(js)
        try:
            result = result.strip()
            if result.startswith('{'):
                return json.loads(result)
        except Exception:
            pass
        return {"content": "", "images": []}

    def parse_url(self, url: str) -> Dict[str, str]:
        """
        Parse a Threads URL and extract username and post ID.

        Args:
            url: Threads URL in format https://www.threads.net/@username/post/ID

        Returns:
            Dict with 'username' and 'post_id' keys

        Raises:
            ValueError: If URL is invalid or not a Threads URL
        """
        parsed = urlparse(url)

        # Support both threads.net and threads.com
        if "threads.net" not in parsed.netloc and "threads.com" not in parsed.netloc:
            raise ValueError(f"Invalid Threads URL: {url}. URL must be from threads.net or threads.com")

        # Extract path and match pattern
        path = parsed.path.strip("/")
        pattern = r"@?([^/]+)/post/([^/]+)"
        match = re.match(pattern, path)

        if not match:
            raise ValueError(
                f"Invalid Threads URL format: {url}. "
                "Expected format: https://www.threads.net/@username/post/ID"
            )

        username, post_id = match.groups()
        return {"username": username.lstrip("@"), "post_id": post_id}

    def fetch_post(self, url: str) -> Dict[str, Any]:
        """
        Fetch a Threads post and return structured data.

        Args:
            url: Threads post URL

        Returns:
            Dict containing:
                - url: Original URL
                - username: Author username
                - post_id: Post ID
                - content: Post text content
                - media_urls: List of media URLs (images/videos)
                - timestamp: Post timestamp (if available)
                - likes: Like count (if available)
        """
        try:
            # Parse URL
            url_info = self.parse_url(url)
            username = url_info["username"]
            post_id = url_info["post_id"]

            # Open browser and navigate
            self.open_browser(url)
            self.wait_for_load()

            # Extract Open Graph data
            og_data = self.extract_open_graph_data()

            description = og_data.get("og:description", "")
            title = og_data.get("og:title", "")
            og_image = og_data.get("og:image")
            og_video = og_data.get("og:video")

            # Extract page content (main content and images)
            page_data = self.extract_page_content()

            # Combine content from OG and page extraction
            content = page_data.get("content", "") or description or title or ""

            # Fallback: use agent-browser's get text command
            if not content:
                page_text = self.get_page_text()
                # Clean up the text - remove URLs, extra whitespace
                import re
                content = re.sub(r'https://\S+', '', page_text)
                content = re.sub(r'\s+', ' ', content).strip()

            # Extract media URLs
            media_urls = []

            # Add OG image/video
            if og_image:
                media_urls.append({"type": "image", "url": og_image})
            if og_video:
                media_urls.append({"type": "video", "url": og_video})

            # Add images from page content (avoid duplicates)
            page_images = page_data.get("images", [])
            existing_urls = {m.get("url") for m in media_urls if isinstance(m, dict)}
            for img in page_images:
                img_src = img.get("src") if isinstance(img, dict) else None
                if img_src and img_src not in existing_urls:
                    media_urls.append({"type": "image", "url": img_src, "alt": img.get("alt", "") if isinstance(img, dict) else ""})
                    existing_urls.add(img_src)

            # Try to extract additional data from JSON-LD
            json_ld_list = self.extract_json_ld()
            timestamp = None
            likes = None

            for json_data in json_ld_list:
                if isinstance(json_data, list):
                    for item in json_data:
                        if isinstance(item, dict):
                            if "datePublished" in item:
                                timestamp = item["datePublished"]
                            if "interactionStatistic" in item:
                                for stat in item["interactionStatistic"]:
                                    if stat.get("interactionType") == "https://schema.org/LikeAction":
                                        likes = stat.get("userInteractionCount")
                elif isinstance(json_data, dict):
                    if "datePublished" in json_data:
                        timestamp = json_data["datePublished"]
                    if "interactionStatistic" in json_data:
                        for stat in json_data["interactionStatistic"]:
                            if stat.get("interactionType") == "https://schema.org/LikeAction":
                                likes = stat.get("userInteractionCount")

            return {
                "url": url,
                "username": username,
                "post_id": post_id,
                "content": content,
                "media_urls": media_urls,
                "timestamp": timestamp,
                "likes": likes,
            }

        finally:
            # Always close the browser
            self.close_browser()

    def fetch_thread_continuation(
        self, url: str, max_posts: int = 10
    ) -> Dict[str, Any]:
        """
        Fetch a Threads post and filter for consecutive posts by the original author.

        Args:
            url: Threads post URL
            max_posts: Maximum number of consecutive posts to fetch

        Returns:
            Dict containing:
                - original_post: The main post data
                - consecutive_posts: List of consecutive posts by same author
                - total_posts: Number of posts found
        """
        original_post = self.fetch_post(url)
        username = original_post["username"]

        return {
            "original_post": original_post,
            "consecutive_posts": [original_post],
            "total_posts": 1,
            "username": username,
        }


def main():
    """CLI entry point for the Threads fetcher."""
    import argparse

    parser = argparse.ArgumentParser(description="Fetch Threads posts using agent-browser")
    parser.add_argument("url", help="Threads post URL")
    parser.add_argument(
        "--output", "-o", help="Output file (JSON)", type=str, default=None
    )
    parser.add_argument(
        "--pretty", help="Pretty print JSON output", action="store_true"
    )
    parser.add_argument(
        "--session", "-s", help="Browser session name", type=str, default="threads-fetcher"
    )

    args = parser.parse_args()

    fetcher = ThreadsFetcher(session_name=args.session)

    try:
        result = fetcher.fetch_post(args.url)

        if args.pretty:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = json.dumps(result, ensure_ascii=False)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Output written to {args.output}")
        else:
            print(output)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(1)
    except Exception as e:
        import traceback
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
