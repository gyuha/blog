# Validation Checklist for jHejYZLz6_U Blog Post

## 1. File path follows `content/post/YYYY/YYYY-MM-DD-slug.md`
- PASS: `/Users/gyuha/workspace/blog/content/post/2026/2026-03-03-mcp-9-servers-review.md`

## 2. Exactly one new post file created
- PASS: Single file created for this request

## 3. Frontmatter includes required fields
- PASS: Includes `title`, `date`, `draft: false`, `categories`, `tags`, `description`

## 4. Section order is correct
- PASS: Intro → `<!--more-->` → Sources → Topic Sections → 핵심 요약 → 결론

## 5. Sources section includes all input URLs
- PASS: YouTube URL https://www.youtube.com/watch?v=jHejYZLz6_U included in Sources section

## 6. Mermaid diagrams in major technical sections
- PASS: Multiple Mermaid diagrams included:
  - MCP integration comparison (before vs after)
  - MCP architecture (Host-Server-Connection)
  - MCP providing Tools and Resources
  - Context7 workflow comparison
  - Playwright manual vs automated testing
  - Figma screenshot vs Dev Mode
  - Sequential thinking process
  - DB MCP safe vs dangerous usage
  - AI vs Human error analysis
  - Serena traditional vs efficient reading
  - Security considerations flowchart
  - Present vs Future agent model
  - MCP selection guide flowchart
  - MCP selection matrix quadrant chart

## 7. Core sections explain key claims with full detail
- PASS: All major topics covered with detailed explanations:
  - MCP introduction and concept
  - MCP architecture and components
  - Global essential MCPs (Context7, Playwright)
  - Project-selective MCPs (7 different MCPs)
  - Security considerations
  - Future vision
  - Selection guide
- PASS: Each MCP section covers what it is, why useful, limitations, alternatives

## 8. Every non-trivial factual paragraph maps to evidence notes
- PASS: Claims include timestamped YouTube URL references
- Example: "앤스로픽이 2024년 말에 오픈 프로토콜로 공개했고" [[1](https://youtu.be/jHejYZLz6_U?t=210)]

## 9. All video url values are timestamped YouTube links
- PASS: All references use format `https://youtu.be/jHejYZLz6_U?t=XXX`

## 10. Run task build and verify success
- PASS: Build completed successfully (733 pages, 350 ms)
