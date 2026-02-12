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
themes/hago/
├── layouts/
│   ├── _default/
│   │   ├── baseof.html      # Base template with two-column grid layout
│   │   ├── single.html       # Single post page
│   │   ├── list.html        # List pages (tags, categories)
│   │   └── summary.html     # Post summary cards
│   ├── partials/
│   │   ├── head.html        # HTML head, Open Graph, CSS
│   │   ├── header.html      # Navigation with animated search
│   │   ├── footer.html      # Scripts, code copying, TOC, Vanta.js
│   │   ├── title_bar.html   # Dynamic title bar with video background
│   │   ├── post.html        # Full post with metadata, nav, comments
│   │   ├── side_*.html      # Sidebar: recent, toc, categories, tags
│   │   └── pagination.html  # Pagination controls
│   ├── categories/taxonomy.html
│   ├── tags/taxonomy.html
│   └── index.html
├── scss/
│   ├── _variables.scss      # Font definitions (Noto Sans KR, Ubuntu)
│   ├── _theme_color.scss    # Color palette and gradients
│   ├── _mixin.scss          # Reusable CSS mixins
│   ├── _responsive.scss     # Breakpoint definitions
│   └── style.scss           # Main stylesheet
└── static/
    ├── js/
    │   └── active.js        # Sticky header/sidebar, scrollUp
    ├── css/                 # Compiled CSS output
    ├── img/                 # Logo, favicon
    └── videos/              # Background video (mp4, webp)
```

### Layout Pattern

The `baseof.html` establishes a two-column layout:
- **Main content** (col-12 col-lg-8): Uses `{{ block "main" . }}` for page-specific content
- **Sidebar** (col-12 col-md-8 col-lg-4): Uses `{{ block "side" . }}` for sidebar widgets

Page templates override these blocks to provide their specific content.

### Theme Styling (SCSS)

The theme uses SCSS with a modular structure:
- **Two-font system**: Noto Sans KR for body text, Ubuntu for code
- **Color variables** (`_theme_color.scss`): Dark theme with blue accents (#3fa4ff)
- **Responsive**: Bootstrap grid with custom breakpoints in `_responsive.scss`
- **Mixins**: Vendor prefixing utilities in `_mixin.scss`

To customize colors or fonts, modify `_theme_color.scss` or `_variables.scss`.

### JavaScript Features

Located in `active.js` and `footer.html`:

1. **Sticky navigation** (`active.js`): Header becomes sticky after 20px scroll
2. **Sticky sidebar** (`active.js`): TOC becomes sticky after 157px scroll (only on single posts)
3. **Code copying** (`footer.html`): Adds copy buttons to code blocks via clipboard API
4. **Auto-scroll TOC** (`footer.html`): Highlights current section on scroll
5. **Vanta.js background** (`footer.html`): Three.js particle animation on title bar
6. **ScrollUp**: Back-to-top button with easing animation

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

## Working with the Hago Theme

Since you're currently in the `themes/hago` directory (a submodule of the main blog), here are key considerations:

### Theme Development Workflow

1. **Edit in place**: Changes made here directly affect the blog at `/Users/gyuha/workspace/blog`
2. **Test changes**: Run `task dev` from the blog root to see changes live
3. **Deploy theme changes**: The theme is a separate git submodule - commit and push to `https://github.com/gyuha/hago.git`

### Adding New Features

- **New page type**: Add to `layouts/` following Hugo's lookup order
- **New partial**: Create in `layouts/partials/`, include with `{{ partial "name.html" . }}`
- **New component style**: Add to appropriate SCSS file in `scss/`
- **New JavaScript**: Add to `static/js/` or include in `layouts/partials/footer.html`

### Code Block Styling

The theme uses highlight.js for syntax highlighting. The copy button functionality is injected via JavaScript in `footer.html` - look for the clipboard-related code when modifying code block behavior.
