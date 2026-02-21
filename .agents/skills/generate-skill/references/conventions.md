# Skill Format Conventions

Complete specification for skill structure and format.

## Directory Structure

```
skill-name/
├── SKILL.md                    (required)
├── LICENSE.txt                 (optional)
├── scripts/                    (optional)
│   ├── example-script.sh
│   └── helper-tool.py
├── references/                 (optional)
│   ├── api-docs.md
│   └── detailed-guide.md
└── assets/                     (optional)
    ├── template.html
    └── logo.png
```

## SKILL.md Format

### Structure

Every SKILL.md consists of two parts:

1. **Frontmatter** (YAML) - Required metadata
2. **Body** (Markdown) - Instructions and guidance

### Frontmatter Fields

```yaml
---
name: skill-name
description: Comprehensive description including what it does and when to use it
---
```

**Required fields:**
- `name` (string) - Skill identifier, must match directory name
- `description` (string) - What the skill does AND when to use it

**Do NOT include:**
- `tags` (deprecated)
- `tools` (deprecated)
- `license` (use LICENSE.txt file instead)
- Any custom fields

### Description Field Guidelines

The description is the primary triggering mechanism. Include:

1. **What it does** - Core functionality
2. **When to use it** - Specific triggering scenarios
3. **What contexts** - File types, task types, domains

**Good example:**
```yaml
description: Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when working with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks.
```

**Bad examples:**
```yaml
description: A useful skill  # Too vague
description: Does stuff with files  # Not actionable
description: PDF processor  # Missing when-to-use info
```

### Body Structure

No strict requirements, but effective skills typically include:

- **Overview** - Brief summary of what skill provides
- **Quick Start** - Minimal example to get started
- **Core Instructions** - Main workflow and procedures
- **Reference** - Links to bundled resources
- **Examples** (optional) - Concrete usage examples

Keep the body under 500 lines. Move detailed content to references/.

## Bundled Resources

### scripts/

**Purpose:** Executable code for deterministic tasks

**When to include:**
- Same code rewritten repeatedly
- Deterministic reliability needed
- Token efficiency matters

**File types:** bash, python, javascript, etc.

**Best practices:**
- Make scripts executable (`chmod +x`)
- Test all scripts before committing
- Include clear usage comments
- Keep scripts focused (one task per script)

**Example structure:**
```
scripts/
├── analyze-form.py
├── validate-fields.sh
└── generate-report.js
```

### references/

**Purpose:** Documentation loaded on-demand into context

**When to include:**
- Database schemas
- API documentation
- Detailed workflow guides
- Domain-specific knowledge
- Long explanations

**Best practices:**
- Keep files focused on one topic
- Include table of contents for files >100 lines
- Link from SKILL.md with clear "when to read" guidance
- Avoid duplication with SKILL.md content
- One level deep (don't nest references)

**Example structure:**
```
references/
├── api-reference.md
├── database-schema.md
└── advanced-workflows.md
```

### assets/

**Purpose:** Files used in output (not loaded to context)

**When to include:**
- Templates
- Images/icons
- Boilerplate code
- Fonts
- Sample documents

**Best practices:**
- Only include files that will be copied/modified in output
- Don't include large binaries unless necessary
- Organize by type or purpose

**Example structure:**
```
assets/
├── templates/
│   ├── report.html
│   └── dashboard.html
├── images/
│   └── logo.png
└── boilerplate/
    └── frontend-app/
```

## Progressive Disclosure Pattern

Skills use three-level loading:

**Level 1: Metadata (always loaded)**
- name + description fields
- ~100 words
- Determines if skill triggers

**Level 2: SKILL.md body (when triggered)**
- Loaded after skill triggers
- <5k words target
- Core instructions only

**Level 3: Bundled resources (on-demand)**
- Loaded only when agent determines it's needed
- Unlimited size (scripts can execute without loading)
- Detailed documentation and tools

### Splitting Large Skills

When SKILL.md approaches 500 lines, split content:

**Pattern 1: Domain-specific organization**
```
skill-name/
├── SKILL.md (overview + navigation)
└── references/
    ├── domain-a.md
    ├── domain-b.md
    └── domain-c.md
```

**Pattern 2: Feature-based organization**
```
skill-name/
├── SKILL.md (core workflow)
└── references/
    ├── basic-features.md
    ├── advanced-features.md
    └── troubleshooting.md
```

**Pattern 3: Framework variants**
```
skill-name/
├── SKILL.md (selection guide)
└── references/
    ├── framework-a.md
    ├── framework-b.md
    └── framework-c.md
```

## Writing Guidelines

### Use Imperative/Infinitive Form

**Good:**
- "Read the configuration file first"
- "Check for existing patterns"
- "Validate output before completing"

**Bad:**
- "You should read the file"
- "Consider checking patterns"
- "It's recommended to validate"

### Keep Content Concise

Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Does this justify its token cost?"

Prefer concise examples over verbose explanations.

### Match Freedom to Task Fragility

**High freedom (text instructions):**
- Multiple approaches valid
- Decisions depend on context
- Heuristics guide approach

**Medium freedom (pseudocode/parameterized scripts):**
- Preferred pattern exists
- Some variation acceptable
- Configuration affects behavior

**Low freedom (specific scripts, few parameters):**
- Operations fragile/error-prone
- Consistency critical
- Specific sequence required

## Validation Checklist

Before finalizing a skill:

- [ ] Frontmatter includes required fields (name, description)
- [ ] Name matches directory name
- [ ] Description includes what AND when-to-use
- [ ] No TODO placeholders in SKILL.md
- [ ] SKILL.md body under 500 lines
- [ ] All scripts are executable and tested
- [ ] References linked from SKILL.md with usage guidance
- [ ] No extraneous files (README.md, CHANGELOG.md, etc)
- [ ] Example files removed or customized
- [ ] Runs: `bun scripts/validate-skill.ts path/to/skill`

## Common Mistakes

### Including deprecated fields

**Wrong:**
```yaml
---
name: my-skill
description: Does things
tags:
  - deprecated
tools:
  - also-deprecated
---
```

**Right:**
```yaml
---
name: my-skill
description: Does things. Use when working on X.
---
```

### Vague descriptions

**Wrong:**
```yaml
description: Helpful skill for files
```

**Right:**
```yaml
description: PDF manipulation tool. Use when rotating, merging, or extracting pages from PDF files.
```

### Creating auxiliary documentation

**Wrong:**
```
skill-name/
├── SKILL.md
├── README.md          # Don't include
├── QUICK_START.md     # Don't include
└── CHANGELOG.md       # Don't include
```

**Right:**
```
skill-name/
└── SKILL.md           # Just the skill
```

### Duplicating content

**Wrong:**
```
SKILL.md contains full API reference
references/api.md contains same API reference
```

**Right:**
```
SKILL.md references the API docs
references/api.md contains the API reference
```

### Not testing scripts

Always test scripts before committing. If a script doesn't work when the agent tries to use it, the skill fails.

## Naming Conventions

- **Skill directories:** kebab-case (`my-skill-name`)
- **SKILL.md:** Exactly `SKILL.md` (case-sensitive)
- **Scripts:** kebab-case with extension (`analyze-form.py`)
- **References:** kebab-case markdown (`api-reference.md`)
- **Assets:** kebab-case or original format (`logo.png`, `template.html`)

## Version Control

Include in git:
- SKILL.md
- All scripts
- All references
- Small assets (<1MB)

Exclude from git:
- Large binaries (>1MB) unless essential
- Generated files
- User-specific configuration
- Temporary files
