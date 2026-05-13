#!/usr/bin/env bash
set -euo pipefail

main() {
    echo "→ Uninstalling Claude Ads..."

    # Remove main skill (orchestrator + references)
    rm -rf "${HOME}/.claude/skills/ads"

    # Remove sub-skills — v2.4.0 set PLUS legacy v2.3.x / v2.2.x skills so upgraders don't leave stale files behind.
    for skill in \
        ads-start ads-next \
        ads-audit ads-google ads-meta ads-tiktok ads-creative ads-landing ads-budget ads-plan \
        ads-competitor ads-dna ads-create ads-generate ads-photoshoot ads-math ads-test ads-update ads-publish \
        ads-apple ads-linkedin ads-microsoft ads-youtube; do
        rm -rf "${HOME}/.claude/skills/${skill}"
    done

    # Remove agents — v2.3.0 set PLUS legacy v2.2.x cross-platform audit agents so upgraders don't leave stale files behind.
    for agent in \
        audit-google audit-meta audit-tiktok creative-strategist visual-designer copy-writer format-adapter \
        audit-creative audit-tracking audit-budget audit-compliance; do
        rm -f "${HOME}/.claude/agents/${agent}.md"
    done

    echo "✓ Claude Ads uninstalled."
    echo ""
    echo "Note: your profile + audit history at ~/.claude-ads/ was NOT touched."
    echo "      If you want a clean wipe, run:  rm -rf ~/.claude-ads"
}

main "$@"
