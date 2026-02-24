# Deep Research Tool Routing Guide

This document defines the routing logic and budget constraints for research tools used in the `deep-research` skill.

## Section 1: Tool Routing Table

Map topic types to tool combinations to optimize research quality and budget.

| Topic Type | Tools | Max Calls |
|---|---|---|
| library/framework | `context7_resolve-library-id` + `context7_query-docs` + `grep_app_searchGitHub` | 4 |
| news/trend | `google_search` + `websearch_web_search_exa` | 3 |
| general technical | `google_search` + `websearch_web_search_exa` (+ `context7` if specific library mentioned) | 3–4 |
| mixed | Combine routes, respect total budget of 10 calls | ≤ 10 |

## Section 2: Tool Documentation

### 1. google_search
- **When to use**: News, trends, general technical queries, and finding specific URLs for analysis.
- **Parameters**:
  - `query` (required string): The search query.
  - `thinking` (boolean, default true): Enables agentic reasoning for the search.
  - `urls` (optional array): Specific URLs to analyze directly.
- **Output format**: Real-time web results with source citations, URLs, and text snippets.
- **Max calls**: 2 per session.
- **Failure handling**: If empty, skip and log `[google_search: no results for 'query']`.
- **Example**: `google_search(query="hugo mermaid integration best practices 2025", thinking=true)`

### 2. websearch_web_search_exa
- **When to use**: Deep content extraction from top search results.
- **Parameters**:
  - `query` (required): The search query.
  - `numResults` (default 8, recommend 3-5): Number of results to return.
  - `contextMaxCharacters` (default 10000, recommend 5000): Max characters for context.
  - `livecrawl` (optional, "fallback"): Use live crawling if cached content is unavailable.
- **Output format**: Clean text content from top search results.
- **Max calls**: 1-2 per session.
- **Failure handling**: If empty, skip and log `[websearch_web_search_exa: no results for 'query']`.
- **Example**: `websearch_web_search_exa(query="hugo mermaid render-codeblock-mermaid.html example", numResults=3)`

### 3. context7_resolve-library-id + context7_query-docs
- **When to use**: Specific library or framework documentation and code examples.
- **Workflow**:
  - **Step 1**: Call `context7_resolve-library-id` with `libraryName` and `query` to get a `libraryId`.
  - **Step 2**: Call `context7_query-docs` with the returned `libraryId` and `query`.
- **Output format**: Structured documentation and verified code snippets.
- **Max calls**: 2 total (1 resolve + 1 query).
- **Failure handling**: If resolve returns no matches, skip the docs call.
- **Example**:
  - `context7_resolve-library-id(libraryName="hugo", query="how to use mermaid")`
  - `context7_query-docs(libraryId="/gohugoio/hugo", query="mermaid diagram configuration")`

### 4. grep_app_searchGitHub
- **When to use**: Finding real-world code usage patterns and best practices.
- **Parameters**:
  - `query` (required): **Literal code pattern** (e.g., `'{{< mermaid >}}'`), NOT keywords.
  - `language` (array): Filter by language (e.g., `['Markdown', 'HTML']`).
  - `useRegexp` (optional): Set to true if using regex.
- **Output format**: Code examples from public GitHub repos with file paths.
- **Max calls**: 2 per session.
- **Failure handling**: If empty, try a simpler code pattern; if still empty, skip.
- **Example**: `grep_app_searchGitHub(query="{{< mermaid >}}", language=["Markdown"])`

## Section 3: Budget Summary Table

| Tool | Max Calls | Typical Output Size | Notes |
|---|---|---|---|
| google_search | 2 | ~3000 chars | Include thinking:true |
| websearch_web_search_exa | 2 | ~5000 chars | Limit numResults to 3-5 |
| context7 (both calls) | 2 | ~4000 chars | Library topics only |
| grep_app_searchGitHub | 2 | ~3000 chars | Use code patterns not keywords |
| **TOTAL** | **≤ 10** | **≤ 20000 chars** | Hard limits |

## Section 4: Result Size Limits

- **Individual result truncation**: 5000 chars max per tool result.
- **Total research output cap**: 20000 chars.
- **Budget exhaustion**: If the budget is exhausted mid-research, stop and return the collected results immediately.
