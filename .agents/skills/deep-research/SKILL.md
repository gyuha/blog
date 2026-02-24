---
name: deep-research
description: Perform deep background research on blog post topics using web search, official documentation, and code examples. Use when writing blog posts that need additional context beyond primary sources. Triggers on research enhancement requests or when called by youtube-to-blog-post / url-only-to-blog-post skills.
---
## When to Use This Skill
Use this skill when:
- A calling skill (e.g., `youtube-to-blog-post` or `url-only-to-blog-post`) requires additional background context or verification of primary source claims.
- The user explicitly requests deeper research on a specific technical topic, library, or news event.
- Primary sources are insufficient to explain the "why" or "how" of a technical mechanism.

Do not use this skill as a standalone blog post generator. It produces research notes, not final posts.

## Input Contract
The calling skill or user must provide:
- `topic` (string): A 1-2 sentence description of the research target.
- `keywords` (array): 3-10 specific terms or phrases to guide search queries.
- `topic_type` (enum): One of `library`, `news`, or `general`.
- `primary_claims` (array): A list of specific assertions from primary sources that require verification or expansion.

## Core Research Workflow
1. Classify the topic type and select the appropriate tool routing from `references/tool-routing-guide.md`.
2. Execute tool calls according to the routing table, respecting the total budget of ≤ 10 calls.
3. Gather broad context first using `google_search` to obtain synthesized summaries and initial source URLs.
4. Extract deep content from high-relevance URLs using `websearch_web_search_exa`, limiting `numResults` to 3-5 to manage output size.
5. Resolve official documentation for library/framework topics using the 2-step `context7` workflow (resolve ID → query docs).
6. Search for real-world code patterns using `grep_app_searchGitHub` as a supplementary step, using literal code patterns and handling potential rate-limit errors gracefully.
7. Extract relevant facts from tool results and build structured research notes.
8. Cross-reference findings against the `primary_claims` to confirm, refute, or expand upon them.
9. Output the final structured research notes.

## Output Contract
Return research notes in the following format:
`claim | evidence | url | confidence`

Confidence values:
- `high`: Multiple authoritative sources agree.
- `medium`: A single authoritative source or multiple indirect sources agree.
- `low`: Findings are inferred, indirect, or sources conflict.

Categories for organization:
- `background`: General context and definitions.
- `verification`: Evidence supporting or refuting primary claims.
- `comparison`: Trade-offs, alternatives, or version differences.
- `code_example`: Verified implementation patterns.

Maximum output size: 20,000 characters.

## Budget and Limits
- **Total Tool Calls**: ≤ 10 calls per research session.
- **Result Truncation**: 5,000 characters maximum per individual tool result.
- **Output Cap**: 20,000 characters total for the final research notes.
- **Early Stop**: If the budget is exhausted before completion, stop immediately and return all collected results.

## Failure Handling
- **Empty Results**: If a tool returns no results, skip it and log `[TOOL_NAME: no results for 'query']`.
- **Errors/Timeouts**: If a tool call fails or times out, log the error and continue with the next step in the workflow.
- **Total Failure**: If all tool calls fail, return empty research notes with a concise error summary.
- **Non-Blocking**: Never block the calling skill; return the best available data even if incomplete.

## Anti-Patterns
- Do not write blog post content; produce only structured research notes.
- Do not persist research data to the filesystem.
- Do not trigger recursive calls to this or other skills.
- Do not exceed the 10-call tool budget or 20,000-character output limit.
- Do not use YouTube MCP tools within this skill.

See `references/tool-routing-guide.md` for detailed tool parameters, routing table, and examples.
