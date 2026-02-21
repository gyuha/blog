# YouTube Post Quality Checklist

Use this checklist after drafting the post and before final handoff.

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
- Source video URL(s) appear near the top for traceability.
- Main sections are derived from transcript segmentation and topic flow.
- Content is synthesized, not copied transcript blocks.

## Mermaid-First Enforcement

- Mermaid diagrams are used in major technical sections.
- Diagram labels are short and readable.
- Direction is consistent (`LR` or `TD`) per diagram purpose.
- Multiple small diagrams are used instead of one overloaded diagram.

## Accuracy and Reasoning

- Claims are tied to transcript/metadata context.
- No invented numbers, quotes, or implementation details.
- Conflicts across sources are resolved with primary-source priority.
- Uncertainty is explicitly stated where evidence is weak.

## Hugo and Repository Conventions

- File path is `content/post/YYYY/YYYY-MM-DD-slug.md`.
- Formatting and style are consistent with nearby posts.
- Existing posts are not rewritten unless explicitly requested.

## Final Verification

- Run `task build` and confirm success.
- If visual/content behavior changed substantially, run `task dev` and review affected page on desktop/mobile.
