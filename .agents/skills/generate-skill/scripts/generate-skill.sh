#!/usr/bin/env bash
# Generate a new skill scaffold with proper format and structure
# Usage: generate-skill.sh <skill-name> [target-directory]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
if [ $# -lt 1 ]; then
    echo -e "${RED}Error: Skill name required${NC}"
    echo "Usage: $0 <skill-name> [target-directory]"
    echo ""
    echo "Examples:"
    echo "  $0 my-skill"
    echo "  $0 my-skill /path/to/skills"
    exit 1
fi

SKILL_NAME="$1"
TARGET_DIR="${2:-.opencode/skills}"

# Validate skill name (kebab-case)
if ! [[ "$SKILL_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo -e "${RED}Error: Skill name must be kebab-case (lowercase letters, numbers, hyphens)${NC}"
    echo "Examples: my-skill, pdf-processor, api-helper"
    exit 1
fi

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

SKILL_PATH="$TARGET_DIR/$SKILL_NAME"

# Check if skill already exists
if [ -d "$SKILL_PATH" ]; then
    echo -e "${RED}Error: Skill '$SKILL_NAME' already exists at $SKILL_PATH${NC}"
    exit 1
fi

echo -e "${GREEN}Creating skill: $SKILL_NAME${NC}"
echo -e "Location: $SKILL_PATH"
echo ""

# Create skill directory structure
mkdir -p "$SKILL_PATH"/{scripts,references,assets}

# Generate SKILL.md with frontmatter and placeholders
cat > "$SKILL_PATH/SKILL.md" << 'EOF'
---
name: SKILL_NAME_PLACEHOLDER
description: TODO - Describe what this skill does AND when to use it. Include specific triggering scenarios.
---

# SKILL_NAME_TITLE_PLACEHOLDER

TODO - Brief overview of what this skill provides.

## Quick Start

TODO - Minimal example to get started.

```bash
# Example usage
```

## Core Instructions

TODO - Main workflow and procedures.

1. First step
2. Second step
3. Final step

## Bundled Resources

### Scripts

TODO - List scripts and their purposes, or remove this section if none.

- `scripts/example-script.sh` - TODO - Describe what this does

### References

TODO - List reference files and when to read them, or remove this section if none.

- `references/example-reference.md` - TODO - When to read this

## Examples

TODO - Provide concrete usage examples, or remove this section if not needed.

### Example: Typical Use Case

**User request:** "TODO - Example user request"

**Process:**
1. TODO - First step
2. TODO - Second step
3. TODO - Final step

---

Remember to:
- Keep SKILL.md under 500 lines
- Use imperative form ("Read the file" not "You should read")
- Move detailed content to references/
- Test all scripts before finalizing
- Run validation: `bun scripts/validate-skill.ts SKILL_PATH_PLACEHOLDER`
EOF

# Replace placeholders
SKILL_NAME_TITLE=$(echo "$SKILL_NAME" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')
sed -i "s/SKILL_NAME_PLACEHOLDER/$SKILL_NAME/g" "$SKILL_PATH/SKILL.md"
sed -i "s/SKILL_NAME_TITLE_PLACEHOLDER/$SKILL_NAME_TITLE/g" "$SKILL_PATH/SKILL.md"
sed -i "s|SKILL_PATH_PLACEHOLDER|$SKILL_PATH|g" "$SKILL_PATH/SKILL.md"

# Generate example script
cat > "$SKILL_PATH/scripts/example-script.sh" << 'EOF'
#!/usr/bin/env bash
# Example script for SKILL_NAME_PLACEHOLDER
# TODO - Describe what this script does

set -euo pipefail

echo "TODO - Implement script functionality"
EOF

sed -i "s/SKILL_NAME_PLACEHOLDER/$SKILL_NAME/g" "$SKILL_PATH/scripts/example-script.sh"
chmod +x "$SKILL_PATH/scripts/example-script.sh"

# Generate example reference
cat > "$SKILL_PATH/references/example-reference.md" << 'EOF'
# Example Reference

TODO - Replace with actual reference content.

This file should contain:
- Detailed documentation
- API specifications
- Database schemas
- Advanced workflows
- Domain knowledge

Keep reference files focused on one topic. For files >100 lines, include a table of contents.

## Section 1

TODO - Content

## Section 2

TODO - Content
EOF

# Generate example asset file
cat > "$SKILL_PATH/assets/example-template.txt" << 'EOF'
# Example Template

TODO - Replace with actual template or remove assets/ directory if not needed.

This directory is for files used in output:
- Templates
- Images/icons
- Boilerplate code
- Sample documents
EOF

# Summary
echo -e "${GREEN}✓ Skill scaffold created successfully${NC}"
echo ""
echo "Directory structure:"
echo "  $SKILL_PATH/"
echo "  ├── SKILL.md"
echo "  ├── scripts/"
echo "  │   └── example-script.sh"
echo "  ├── references/"
echo "  │   └── example-reference.md"
echo "  └── assets/"
echo "      └── example-template.txt"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Edit $SKILL_PATH/SKILL.md and fill in TODOs"
echo "  2. Update or remove example files in scripts/, references/, assets/"
echo "  3. Make scripts executable and test them"
echo "  4. Remove directories you don't need"
echo "  5. Validate: bun scripts/validate-skill.ts $SKILL_PATH"
echo ""
echo -e "${GREEN}Done!${NC}"
