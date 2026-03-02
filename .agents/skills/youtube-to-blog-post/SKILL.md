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
4. Build structured notes per key claim: `claim`, `transcript quote/time marker`, `video url (timestamped)`, `confidence`.
5. (Optional) Enhance notes with background research using the `deep-research` skill:
   - Set `topic` from the main subject identified in step 4 notes.
   - Set `keywords` from entities and key terms extracted in step 4.
   - Set `topic_type` to `library`, `news`, or `general` based on video content.
   - Set `primary_claims` to assertions needing verification or expansion.
   - Merge returned research notes into your evidence set before writing.
6. Build a fixed output outline first, then write section-by-section from notes, prioritizing explanation accuracy over aggressive compression.
7. Generate exactly one post file under `content/post/YYYY/YYYY-MM-DD-slug.md` unless the user explicitly asks for multiple posts.
8. Write the post in Korean by default unless the user explicitly requests another language.
9. Run a completion audit against required section order and checklist (PASS/FAIL per item).
10. Run `task build` before handoff.

## Anti-Truncation Execution Rules

- Never draft in one long free-form pass.
- Use a staged pipeline:
  1) source collection -> 2) evidence notes -> 3) fixed outline -> 4) section-by-section writing -> 5) completion audit.
- Fixed outline must include every required section before body writing starts.
- If transcript depth is insufficient for any segment, mark uncertainty and avoid high-confidence technical assertions for that segment.
- If any required section is missing after writing, regenerate only missing sections and re-run the audit.
- Hard gate: no final handoff is allowed unless all checklist items are PASS.

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
- Write in Korean unless user explicitly requests another language.
- Add a concise intro.
- Insert `<!--more-->` after the intro/excerpt area.
- Add a `Sources` section immediately after `<!--more-->` with all input URLs in original order.
- For every evidence-backed claim, use a timestamped YouTube URL in `video url` (preferred format: `https://youtu.be/<id>?t=<seconds>`).
- Use this exact section order:
  1) Intro
  2) `<!--more-->`
  3) Sources
  4) Topic Sections (based on transcript/topic segmentation)
  5) 핵심 요약
  6) 결론
- Prioritize precise, exhaustive explanation of mechanisms, assumptions, and trade-offs. Do not compress or abbreviate technical content.
- For key technical points, explain `what`, `why`, and `how` concretely with as much detail as the transcript supports.
- Do not impose any length limit on individual sections — write until the topic is fully and faithfully explained.
- Cover every noteworthy point mentioned in the transcript; omission of covered content is a quality failure.
- Use Mermaid diagrams aggressively for flows, architecture, timelines, and comparisons.
- Add Mermaid diagrams to every major technical section where structure, flow, architecture, timeline, or comparison can be visualized — no upper or lower limit; use as many as clarity demands.
- Prefer multiple focused Mermaid diagrams over one oversized diagram.
- Never skip a Mermaid opportunity to save space; diagram coverage is a quality signal.
- Add a `핵심 요약` section and a short `결론` section.

## Synthesis Rules

- Keep claims grounded in transcript and metadata context.
- Do not dump raw transcript text.
- Prefer source-backed explicit explanations over broad paraphrased summaries.
- Resolve overlap or conflicts by prioritizing primary-source statements.
- If uncertainty exists, state uncertainty explicitly instead of inventing details.
- Ensure every non-trivial factual paragraph in the final post maps to at least one evidence-note entry.
- When citing transcript-backed claims, include a timestamped YouTube URL (`&t=` or `?t=` seconds) so readers can jump directly to the referenced moment.

## Multi-URL Rule

- If multiple YouTube URLs are given, produce one unified post by default.
- Do not split into multiple posts unless the user explicitly requests it.

## Validation Checklist

1. Confirm file path follows `content/post/YYYY/YYYY-MM-DD-slug.md`.
2. Confirm exactly one new post file was created for this request (unless user explicitly asked split output).
3. Confirm frontmatter includes `title`, `date`, `draft: false`, `categories`, `tags`, `description`.
4. Confirm section order is exactly: Intro -> `<!--more-->` -> Sources -> Topic Sections -> 실전 적용 포인트 -> 결론.
5. Confirm `Sources` includes all input URLs in original order.
6. Confirm Mermaid diagrams appear in every major technical section where a diagram is applicable (no minimum or maximum — presence is judged by whether a diagram would aid comprehension).
7. Confirm core sections explain key claims with full concrete detail, not only high-level summaries. No notable topic from the transcript should be omitted or superficially covered.
8. Confirm every non-trivial factual paragraph maps to evidence notes.
9. Confirm all `video url` values in evidence notes are timestamped YouTube links (for example `https://youtu.be/<id>?t=299`).
10. Run `task build` and verify success.

Checklist enforcement:
- Mark each item as PASS/FAIL explicitly.
- If any item is FAIL, do not hand off. Fix gaps and rerun the checklist.

`references/youtube-post-quality-checklist.md` is mandatory acceptance criteria, not optional reference.
