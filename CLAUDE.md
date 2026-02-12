# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo-based blog (gyuha.com) that uses a custom theme "hago" hosted as a git submodule. The site is deployed to GitHub Pages via a separate repository.

### Repository Structure

- **Source blog**: This repository (`/Users/gyuha/workspace/blog`)
- **Theme submodule**: `themes/hago` -> https://github.com/gyuha/hago.git
- **Public submodule**: `public` -> https://github.com/gyuha/gyuha.github.io.git (GitHub Pages deployment target)

### Content Organization

- Posts are organized by year: `content/post/{YEAR}/{YYYY-MM-DD}-{slug}.md`
- Post frontmatter uses YAML format (configured in `config.toml`)
- Images are stored in `static/img/{post-slug}/`
- New posts use the `archetypes/default.md` template

## Common Commands

All commands use Task (taskfile.dev) - run `task --list` to see all available tasks.

| Command | Description |
|---------|-------------|
| `task run` | Start Hugo development server with drafts (binds to 0.0.0.0) |
| `task dev` | Start Hugo server with drafts, fast render disabled |
| `task build` | Build site with drafts |
| `task new -- [title]` | Create new post (format: `content/post/YYYY/YYYY-MM-DD-title.md`) |
| `task clone` | Clone GitHub Pages repo to `public/` folder |
| `task deploy` | Build and deploy to GitHub (commits to both `public/` and source repo) |

### Creating New Posts

```bash
# Using Task (recommended)
task new -- my-post-title

# Or using Hugo directly
hugo new post/YYYY/YYYY-MM-DD-my-post-title.md
```

## Configuration

- **Config file**: `config.toml`
- **Base URL**: `https://gyuha.com/`
- **Language**: Korean (`ko-KR`)
- **Comments**: Disqus enabled (shortname: `gyuha-blog`)
- **Analytics**: Google Analytics (G-3XN21838ZJ)
- **Code highlighting**: Pygments with "fruity" style, line numbers enabled in tables

## Theme Architecture (hago)

The theme follows Hugo's standard layout structure:

```
themes/hago/layouts/
├── _default/
│   ├── baseof.html      # Base template (includes header, sidebar, footer)
│   ├── single.html       # Single post page
│   ├── list.html        # List pages (tags, categories)
│   └── summary.html     # Post summary cards
├── partials/
│   ├── head.html        # HTML head (meta, CSS links)
│   ├── header.html      # Site header/navigation
│   ├── footer.html      # Footer content
│   ├── title_bar.html   # Title bar section
│   ├── post.html        # Full post content
│   ├── side_*.html      # Sidebar components (recent, tags, categories, toc)
│   └── pagination.html  # Pagination controls
├── categories/taxonomy.html
├── tags/taxonomy.html
└── index.html
```

### Layout Pattern

The `baseof.html` establishes a two-column layout:
- **Main content** (col-12 col-lg-8): Uses `{{ block "main" . }}` for page-specific content
- **Sidebar** (col-12 col-md-8 col-lg-4): Uses `{{ block "side" . }}` for sidebar widgets

Page templates override these blocks to provide their specific content.

## Deployment Process

The `task deploy` command:
1. Builds the site with `hugo -D`
2. Commits changes to `public/` submodule (GitHub Pages)
3. Pushes to `gyuha.github.io` repository
4. Commits and pushes source repo changes

**Note**: The `public/` folder is a git submodule and must be initialized with `git submodule update --init --recursive` after cloning.

## Frontmatter Format

Posts use YAML frontmatter:

```yaml
---
title: "Post Title"
date: YYYY-MM-DDTHH:MM:SS+09:00
draft: true
categories: [CategoryName]
tags: [tag1, tag2, tag3]
---
```

The `<!--more-->` tag is used to specify the summary/excerpt for post listings.
