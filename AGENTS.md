# AGENTS.md
Guide for coding agents in `/Users/gyuha/workspace/blog`.

## Repository Overview
- Project type: Hugo blog source repository.
- Theme: `themes/hago` (git submodule, separate local AGENTS rules).
- Deploy target: `public` (git submodule for GitHub Pages output).
- Main authority files:
  - `Taskfile.yml`
  - `config.toml`
  - `archetypes/default.md`
  - `README.md`
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

### Core commands (source of truth: `Taskfile.yml`)
```bash
task --list
task run
task dev
task build
task new -- my-post-title
task deploy
```

From `Taskfile.yml`:
- `task run` -> `hugo server -D --bind=0.0.0.0`
- `task dev` -> `hugo server -D --bind=0.0.0.0 --disableFastRender`
- `task build` -> `hugo -D`
- `task new -- <slug>` -> `hugo new post/YYYY/YYYY-MM-DD-<slug>.md`
- `task deploy` -> build + commit/push `public` + commit/push source repo

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
- `npm run sass:watch` compiles SCSS in watch mode

### Command caveats
- `task deploy` has side effects (commits and pushes two repos). Run only when explicitly requested.
- `task clone` removes `public` first (`rm -rf public`) and reclones.
- README examples are simplified; prefer exact behavior from `Taskfile.yml`.

## Lint / Test Reality
- No lint task in root `Taskfile.yml`.
- No test runner configured in root.
- No `npm test` script in `themes/hago/package.json`.
- No CI workflow under `.github/workflows/` in this repo.

## Single-Test Execution
There is no true single-test command because no test framework is configured.

Use this focused validation flow instead:
1. run `task dev`
2. open only affected routes/pages
3. verify desktop and mobile layout/behavior
4. if SCSS changed, run `npm run sass:build` in `themes/hago`
5. run `task build` before final handoff

## Style and Coding Conventions
Prefer local patterns over global rewrites.

### Formatting and imports
- `.prettierrc.yaml` exists (`printWidth: 500`, `bracketSpacing: false`, `proseWrap: never`).
- No enforced lint/format pipeline; match nearby files exactly.
- SCSS import order in `themes/hago/scss/style.scss` must remain: `theme_color` -> `variables` -> `mixin` -> `responsive`.

### Hugo templates (`themes/hago/layouts/**/*.html`)
- Preserve base block contract in `layouts/_default/baseof.html`:
  - `block "main"`
  - `block "side"`
- Reuse partial pattern: `{{ partial "name.html" . }}`.
- Preserve whitespace trim markers where used: `{{-` and `-}}`.
- Keep URL helper usage consistent by context:
  - static assets: `relURL`
  - absolute media/OG: `absURL`
  - content links: `.RelPermalink` or `.Permalink`
- Keep taxonomy templates in `layouts/categories/` and `layouts/tags/`.
- Some templates use mixed legacy URL composition (`.Site.BaseURL` + `urlize`). Preserve file-local style unless asked to refactor.

### SCSS (`themes/hago/scss`)
- Edit SCSS source files, not generated CSS, unless explicitly requested.
- Use existing variables/mixins before adding new ones.
- Naming conventions:
  - variables: `$kebab-case`
  - mixins: `kebab-case`
- Use breakpoint variables from `_responsive.scss` instead of hardcoded breakpoints.

### JavaScript
- Preserve file-local style split:
  - `themes/hago/static/js/active.js`: jQuery IIFE + `var`
  - `themes/hago/layouts/partials/footer.html`: DOM API + `const`/`let`
- Do not rename selectors/IDs/classes without checking SCSS/template impact.
- Keep explicit failure handling for browser APIs (example: clipboard `.catch(...)`).

### Types and naming
- This repo is mostly Hugo/SCSS/JS/Markdown; no project-wide TypeScript policy is defined.
- If touching typed code in future, prefer strict explicit types and no `any` escapes.
- Use existing naming/file conventions: partials use lowercase underscores (for example `side_recent.html`), post files use `content/post/YYYY/YYYY-MM-DD-slug.md`.

### Markdown and frontmatter (`content/post/**/*.md`)
- Frontmatter format is YAML (`metaDataFormat = "yaml"` in `config.toml`).
- Archetype baseline fields:
  - `title`
  - `date`
  - `draft`
- Preferred post metadata for new content: `categories` (plural), `tags`, optional `description`.
- For charts/diagrams in posts, use Mermaid by default.
- For line breaks in post content, use HTML `<br>` instead of `\n`.
- Use `<!--more-->` for excerpt split in longer posts.
- Legacy variance exists (`category` singular, occasional underscore filenames). Keep existing posts stable; use current dominant pattern for new posts.

## Mermaid-First Blog Writing Rule
When writing or updating blog posts, prioritize Mermaid diagrams aggressively.

Required guidance:
1. Add Mermaid charts wherever structure, flow, architecture, timelines, or comparisons appear.
2. Prefer multiple small diagrams over one oversized chart.
3. Use Mermaid in major sections by default unless the section is purely narrative.
4. Keep diagrams readable with short labels and consistent direction (`LR` or `TD`).
5. Ensure diagrams render through the existing Hugo Mermaid pipeline (`render-codeblock-mermaid.html`).
- Practical expectation: for technical posts, include Mermaid frequently; if a section can be clearer with a chart, add one.

## Error Handling and Safety
- Avoid silent failures.
- Keep changes minimal and scoped.
- Do not add dependencies unless required by task.
- Do not invent commands not defined in repository sources.

## Verification Checklist
For content/template/style changes:
1. run `task build`
2. run `task dev`
3. verify affected pages on desktop and mobile

If theme SCSS changed:
1. run `npm run sass:build` in `themes/hago`
2. re-verify affected pages with `task dev`

If deploy was requested:
1. confirm submodules are initialized
2. run `task deploy`
3. verify git state in both source repo and `public`

## Subtree Priority Rule
- This file is root guidance for the whole blog repository.
- For `themes/hago/**`, also apply `themes/hago/AGENTS.md`.
- If guidance conflicts, prefer the more local file for that subtree.
