# YouTube Post Quality Checklist

Use this checklist after drafting the post and before final handoff.

Hard gate:
- Report PASS/FAIL for every item.
- If any item is FAIL, do not hand off. Fix and rerun the full checklist.

## Input and Scope

- Input is YouTube URL-only, or the user explicitly asked for YouTube-to-post conversion.
- URL order is preserved and reflected in source handling.
- For multiple URLs, one unified post is produced unless the user asked for separate posts.

## Source Collection (YouTube MCP)

Per video:
- Collected metadata via `youtube_get_video`.
- Collected transcript via `youtube_get_transcript` (`chunks` or `full` preferred).
- Collected segmented topics via `youtube_segment_topics`.
- Collected entities via `youtube_extract_entities`.
- Collected comments via `youtube_get_comments` only when comments improve insight quality.

## Frontmatter Contract

Required keys are present and valid:
- `title`
- `date`
- `draft: false`
- `categories` (plural list)
- `tags` (list)
- `description`

## Content Contract

- Post language is Korean unless user requested otherwise.
- Intro is concise and clear.
- `<!--more-->` exists near the top excerpt boundary.
- `Sources` section appears immediately after `<!--more-->` and lists all URLs in original order.
- For transcript-backed claim citations, `video url` uses timestamped YouTube links (`&t=` or `?t=` seconds).
- Section order is exact: Intro -> `<!--more-->` -> Sources -> Topic Sections(>=3) -> 실전 적용 포인트 -> 결론.
- Main sections are derived from transcript segmentation and topic flow.
- Content is synthesized, not copied transcript blocks.

## Mermaid-First Enforcement

- Mermaid diagrams are used in at least 2 major technical sections.
- Diagram labels are short and readable.
- Direction is consistent (`LR` or `TD`) per diagram purpose.
- Multiple small diagrams are used instead of one overloaded diagram.

## Accuracy and Reasoning

- Claims are tied to transcript/metadata context.
- No invented numbers, quotes, or implementation details.
- Conflicts across sources are resolved with primary-source priority.
- Uncertainty is explicitly stated where evidence is weak.
- Every non-trivial factual paragraph maps to at least one evidence note (`claim`, `transcript quote/time marker`, `video url`, `confidence`).
- `video url` values in evidence notes are direct-jump links with time offset (recommended: `https://youtu.be/<id>?t=<seconds>`).

## Hugo and Repository Conventions

- File path is `content/post/YYYY/YYYY-MM-DD-slug.md`.
- Exactly one new post file is created unless the user explicitly requests split output.
- Formatting and style are consistent with nearby posts.
- Existing posts are not rewritten unless explicitly requested.

## Final Verification

- Run `task build` and confirm success.
- If visual/content behavior changed substantially, run `task dev` and review affected page on desktop/mobile.
