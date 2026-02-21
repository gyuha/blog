---
name: youtube-to-blog-post
description: Create a new Hugo blog post from YouTube video URLs using YouTube MCP data. Use when a user provides one or more YouTube links (especially URL-only prompts) and wants a Korean technical post with evidence-grounded, precise explanations and Mermaid diagrams.
---

# YouTube To Blog Post

Turn YouTube videos into publication-ready Hugo posts that match this repository's blogging conventions.

## When to Use This Skill

Use this skill when:
- The user provides only YouTube URL(s) with no extra writing instructions.
- The user asks to convert a YouTube video into a technical blog post.
- The user wants one cohesive post from multiple YouTube links.

Do not use this skill for non-YouTube-only source sets.

## Core Workflow

1. Parse input URLs and keep original order.
2. Extract each YouTube video ID from `youtube.com/watch`, `youtu.be`, or `youtube.com/shorts` format.
3. Gather source material with YouTube MCP:
   - `youtube_get_video`
   - `youtube_get_transcript` (prefer `chunks` or `full` for depth)
   - `youtube_segment_topics`
   - `youtube_extract_entities`
   - `youtube_get_comments` only when audience reactions add useful context
4. Write one cohesive post from all gathered material, prioritizing explanation accuracy over aggressive compression.
5. Create a new file under `content/post/YYYY/YYYY-MM-DD-slug.md`.
6. Write the post in Korean by default unless the user explicitly requests another language.
7. Run `task build` before handoff.

## Required Post Contract

Use YAML frontmatter with at least:

```yaml
---
title: "..."
date: 2026-02-21T17:00:00+09:00
draft: false
categories:
  - ...
tags:
  - ...
description: "..."
---
```

Body requirements:
- Add a concise intro.
- Insert `<!--more-->` after the intro/excerpt area.
- Add major sections based on transcript/topic segmentation.
- Prioritize precise explanation of mechanisms, assumptions, and trade-offs over short summary-style writing.
- For key technical points, explain `what`, `why`, and `how` concretely.
- Use Mermaid diagrams aggressively for flows, architecture, timelines, and comparisons.
- Prefer multiple small Mermaid diagrams over one oversized diagram.
- Add practical takeaways and a short conclusion.
- Place source URL(s) near the top for traceability.

## Synthesis Rules

- Keep claims grounded in transcript and metadata context.
- Do not dump raw transcript text.
- Prefer source-backed explicit explanations over broad paraphrased summaries.
- Resolve overlap or conflicts by prioritizing primary-source statements.
- If uncertainty exists, state uncertainty explicitly instead of inventing details.

## Multi-URL Rule

- If multiple YouTube URLs are given, produce one unified post by default.
- Do not split into multiple posts unless the user explicitly requests it.

## Validation Checklist

1. Confirm file path follows `content/post/YYYY/YYYY-MM-DD-slug.md`.
2. Confirm frontmatter includes `title`, `date`, `draft: false`, `categories`, `tags`, `description`.
3. Confirm `<!--more-->` exists.
4. Confirm Mermaid diagrams are present in major technical sections.
5. Confirm source URL(s) are listed near the top.
6. Confirm core sections explain key claims with concrete detail, not only high-level summaries.
7. Run `task build` and verify success.

For detailed quality criteria and section-by-section checks, read `references/youtube-post-quality-checklist.md`.
