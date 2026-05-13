#!/usr/bin/env bash
set -euo pipefail

# Claude Ads Installer
# Wraps everything in main() to prevent partial execution on network failure

main() {
    SKILL_DIR="${HOME}/.claude/skills/ads"
    AGENT_DIR="${HOME}/.claude/agents"
    REPO_URL="https://github.com/Hainrixz/claude-ads"

    echo "════════════════════════════════════════"
    echo "║   Claude Ads - Installer             ║"
    echo "║   Claude Code Paid Ads Skill         ║"
    echo "════════════════════════════════════════"
    echo ""

    # Check prerequisites
    command -v git >/dev/null 2>&1 || { echo "✗ Git is required but not installed."; exit 1; }
    echo "✓ Git detected"

    # Create directories
    mkdir -p "${SKILL_DIR}/references"
    mkdir -p "${AGENT_DIR}"

    # Clone or update
    TEMP_DIR=$(mktemp -d)
    trap 'rm -rf "${TEMP_DIR}"' EXIT

    echo "↓ Downloading Claude Ads..."
    git clone --depth 1 "${REPO_URL}" "${TEMP_DIR}/claude-ads" 2>/dev/null

    # Copy main skill + references
    echo "→ Installing skill files..."
    cp "${TEMP_DIR}/claude-ads/ads/SKILL.md" "${SKILL_DIR}/SKILL.md"
    cp "${TEMP_DIR}/claude-ads/ads/references/"*.md "${SKILL_DIR}/references/"

    # Copy sub-skills
    echo "→ Installing sub-skills..."
    for skill_dir in "${TEMP_DIR}/claude-ads/skills"/*/; do
        skill_name=$(basename "${skill_dir}")
        target="${HOME}/.claude/skills/${skill_name}"
        mkdir -p "${target}"
        cp "${skill_dir}SKILL.md" "${target}/SKILL.md"

        # Copy assets (industry templates) if they exist
        if [ -d "${skill_dir}assets" ]; then
            mkdir -p "${target}/assets"
            cp "${skill_dir}assets/"*.md "${target}/assets/"
        fi
    done

    # Copy agents
    echo "→ Installing subagents..."
    cp "${TEMP_DIR}/claude-ads/agents/"*.md "${AGENT_DIR}/" 2>/dev/null || true

    # Copy scripts (optional Python tools)
    SCRIPTS_DIR="${HOME}/.claude/skills/ads/scripts"
    if [ -d "${TEMP_DIR}/claude-ads/scripts" ]; then
        echo "→ Installing Python scripts..."
        mkdir -p "${SCRIPTS_DIR}"
        # Recursive copy so scripts/lib/ (vendored research pipeline) is included
        cp -R "${TEMP_DIR}/claude-ads/scripts/." "${SCRIPTS_DIR}/"
        cp "${TEMP_DIR}/claude-ads/requirements.txt" "${SKILL_DIR}/requirements.txt"
    fi

    # Install Python dependencies (landing page analysis, image validation)
    echo ""
    echo "→ Installing Python dependencies..."
    if command -v pip3 >/dev/null 2>&1 || command -v pip >/dev/null 2>&1; then
        PIP_CMD="pip3"
        command -v pip3 >/dev/null 2>&1 || PIP_CMD="pip"
        ${PIP_CMD} install -q -r "${SKILL_DIR}/requirements.txt" 2>/dev/null \
            || { echo "  ⚠ Standard pip install failed, trying --break-system-packages..." >&2; \
                 ${PIP_CMD} install --break-system-packages -q -r "${SKILL_DIR}/requirements.txt" 2>/dev/null; } \
            && echo "  ✓ Python dependencies installed" \
            || echo "  ⚠ pip install failed. Run manually: pip3 install -r ${SKILL_DIR}/requirements.txt"
    else
        echo "  ⚠ pip not found. Install deps manually: pip3 install -r ${SKILL_DIR}/requirements.txt"
    fi

    # Check for banana-claude (image generation provider)
    echo ""
    if [ -d "${HOME}/.claude/skills/banana" ] || [ -f "${HOME}/.claude/skills/banana/SKILL.md" ]; then
        echo "  ✓ banana-claude detected (image generation ready)"
    else
        echo "  ⚠ banana-claude not installed. Image generation (/ads generate, /ads photoshoot) requires it."
        echo "    Install banana-claude (third-party skill), then run: /banana setup (to configure API key)"
    fi

    echo ""
    echo "✓ Claude Ads installed successfully!"
    echo ""
    # Count installed assets dynamically so the output never drifts from reality.
    SKILLS_COUNT=$(find "$HOME/.claude/skills" -maxdepth 2 -name SKILL.md -path "*/ads-*/SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
    REFS_COUNT=$(find "$SKILL_DIR/references" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    AGENTS_COUNT=$(find "$AGENT_DIR" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    TEMPLATES_COUNT=$(find "$HOME/.claude/skills/ads-plan/assets" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

    echo "  Installed:"
    echo "    • 1 main skill (ads orchestrator)"
    echo "    • ${SKILLS_COUNT:-?} sub-skills (platform + functional + creative)"
    echo "    • ${AGENTS_COUNT:-?} agents (3 audit + 4 creative)"
    echo "    • ${REFS_COUNT:-?} reference files"
    echo "    • ${TEMPLATES_COUNT:-?} industry templates"
    echo ""
    echo "Usage:"
    echo "  1. Start Claude Code:        claude"
    echo "  2. Run the first-time wizard: /ads start"
    echo "     (or skip to audit:          /ads audit)"
    echo "  3. After audits:              /ads next"
    echo ""
    echo "To uninstall: curl -fsSL ${REPO_URL}/raw/main/uninstall.sh | bash"
}

main "$@"
