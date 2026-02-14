# AGENTS.md
Guide for coding agents in `/Users/gyuha/workspace/blog`.

## Repository Overview
- Project type: Hugo blog source repository.
- Theme: `themes/hago` (git submodule).
- Deploy target: `public` (git submodule for GitHub Pages output).
- Main authority files:
  - `Taskfile.yml`
  - `config.toml`
  - `archetypes/default.md`
  - `README.md`
  - `CLAUDE.md`
  - `themes/hago/package.json`
  - `themes/hago/AGENTS.md`

## Cursor / Copilot Rule Files
Checked in this repository:
- `.cursorrules`: not found
- `.cursor/rules/`: not found
- `.github/copilot-instructions.md`: not found
No extra Cursor/Copilot instruction file is active.

## Build / Lint / Test Commands
Run from repository root unless otherwise noted.

### Core commands (root)
```bash
task --list
task run
task dev
task build
task new -- my-post-title
```
From `Taskfile.yml`:
- `task run` -> `hugo server -D --bind=0.0.0.0`
- `task dev` -> `hugo server -D --bind=0.0.0.0 --disableFastRender`
- `task build` -> `hugo -D`
- `task new -- <slug>` -> `content/post/YYYY/YYYY-MM-DD-<slug>.md`

### Direct Hugo equivalents
```bash
hugo server -D
hugo -D
hugo new post/2026/2026-02-14-my-post.md
```

### Theme asset commands (`themes/hago`)
```bash
npm install
npm run sass:build
npm run sass:watch
npm start
```
From `themes/hago/package.json`:
- `npm start` == `npm run sass:watch`
- `npm run sass:build` compiles SCSS once
- `npm run sass:watch` compiles in watch mode

### Deploy command (side effects: commits + pushes)
```bash
task deploy
```
`task deploy` does all of the following:
1. builds site with drafts
2. commits/pushes `public` submodule
3. commits/pushes source repo
Only run when deployment is explicitly requested.

### Lint / test status
- No lint task in `Taskfile.yml`.
- No test runner in root.
- No `npm test` in `themes/hago/package.json`.
- No CI workflows in `.github/workflows/`.

## Single-Test Execution
There is no single-test command in this repository because no test framework is configured.
Closest validation flow:
1. run `task dev`
2. open and validate the affected page(s)
3. verify desktop + mobile widths
4. if SCSS changed, run `npm run sass:build` in `themes/hago`

## Style and Coding Conventions
Prefer local patterns over global rewrites.

### Global formatting signals
- `.prettierrc.yaml` exists with:
  - `printWidth: 500`
  - `bracketSpacing: false`
  - `proseWrap: "never"`
- No enforced lint/format pipeline; match nearby files.

### Hugo templates (`themes/hago/layouts/**/*.html`)
- Preserve base block contract in `layouts/_default/baseof.html`:
  - `block "main"`
  - `block "side"`
- Partial pattern: `{{ partial "name.html" . }}`
- Keep whitespace trim markers where present: `{{-` and `-}}`
- Keep URL helper usage consistent by context:
  - static asset paths: `relURL`
  - absolute media/OG paths: `absURL`
  - content links: `.RelPermalink` / `.Permalink`
- Reuse existing partial structure (`side_*.html`, `pagination.html`, etc.)
- Keep taxonomy templates under:
  - `layouts/categories/`
  - `layouts/tags/`

### SCSS (`themes/hago/scss`)
- Edit SCSS source files, not generated CSS, unless requested.
- Keep import order in `scss/style.scss`:
  1. `theme_color`
  2. `variables`
  3. `mixin`
  4. `responsive`
- Naming style:
  - variables use `$kebab-case`
  - mixins use `kebab-case`
- Use breakpoint variables from `_responsive.scss`.
- Prefer existing variables/mixins over repeated hardcoded values.

### JavaScript
- Preserve file-local style:
  - `themes/hago/static/js/active.js`: jQuery IIFE + `var`
  - `themes/hago/layouts/partials/footer.html`: DOM API + `const`/`let`
- Do not rename existing selectors/IDs/classes without full impact check.
- Keep explicit error handling for operations that may fail (clipboard copy, etc.).

### Markdown and frontmatter (`content/post/**/*.md`)
- Frontmatter format is YAML (`metaDataFormat = "yaml"` in `config.toml`).
- Archetype baseline (`archetypes/default.md`):
  - `title`
  - `date`
  - `draft`
- Typical metadata in posts:
  - `categories` (plural)
  - `tags`
- Use `<!--more-->` to define excerpt split for longer posts.
- New post filename pattern:
  - `content/post/YYYY/YYYY-MM-DD-slug.md`
Legacy variance exists (`category` singular, underscore slugs); for new work use current dominant style.

## Error Handling and Safety
- Avoid silent failures.
- Keep changes minimal and scoped.
- Do not add dependencies unless task requires them.
- Do not invent commands not defined in repository sources.

## Verification Checklist
For content/template/style changes:
1. run `task build`
2. run `task dev`
3. verify affected pages in desktop and mobile viewport
If theme SCSS changed:
1. run `npm run sass:build` in `themes/hago`
2. re-verify affected pages with `task dev`
If deploy was requested:
1. ensure submodules are initialized
2. run `task deploy`
3. verify git state in source repo and `public`

## Subtree Priority Rule
- This file is root guidance for the whole blog repo.
- For `themes/hago/**`, also apply `themes/hago/AGENTS.md`.
- If guidance conflicts, prefer the more local file for that subtree.
