#Requires -Version 5.1
<#
.SYNOPSIS
    Claude Ads Uninstaller for Windows
.DESCRIPTION
    Removes the Claude Ads skill, sub-skills, agents, and reference files
    from Claude Code on Windows systems.
#>

$ErrorActionPreference = "Stop"

function Main {
    Write-Host "Uninstalling Claude Ads..."

    $ClaudeDir = Join-Path $env:USERPROFILE ".claude"

    # Remove main skill (orchestrator + references)
    $MainSkill = Join-Path $ClaudeDir "skills\ads"
    if (Test-Path $MainSkill) {
        Remove-Item -Path $MainSkill -Recurse -Force
    }

    # Remove sub-skills — v2.4.0 set PLUS legacy v2.3.x / v2.2.x skills so upgraders don't leave stale files behind.
    $SubSkills = @(
        "ads-start", "ads-next",
        "ads-audit", "ads-google", "ads-meta", "ads-tiktok",
        "ads-creative", "ads-landing", "ads-budget", "ads-plan", "ads-competitor",
        "ads-dna", "ads-create", "ads-generate", "ads-photoshoot",
        "ads-math", "ads-test", "ads-update", "ads-publish",
        # Legacy v2.2.x skills removed in v2.3.0 — also cleaned for upgraders
        "ads-apple", "ads-linkedin", "ads-microsoft", "ads-youtube"
    )
    foreach ($skill in $SubSkills) {
        $SkillPath = Join-Path $ClaudeDir "skills\$skill"
        if (Test-Path $SkillPath) {
            Remove-Item -Path $SkillPath -Recurse -Force
        }
    }

    # Remove agents — v2.3.0 set PLUS legacy v2.2.x cross-platform audit agents so upgraders don't leave stale files behind.
    $Agents = @(
        "audit-google", "audit-meta", "audit-tiktok",
        "creative-strategist", "visual-designer", "copy-writer", "format-adapter",
        # Legacy v2.2.x cross-platform audit agents — also cleaned for upgraders
        "audit-creative", "audit-tracking", "audit-budget", "audit-compliance"
    )
    foreach ($agent in $Agents) {
        $AgentPath = Join-Path $ClaudeDir "agents\$agent.md"
        if (Test-Path $AgentPath) {
            Remove-Item -Path $AgentPath -Force
        }
    }

    Write-Host "[OK] Claude Ads uninstalled." -ForegroundColor Green
    Write-Host ""
    Write-Host "Note: your profile + audit history at ~/.claude-ads/ was NOT touched."
    Write-Host "      If you want a clean wipe, run:  Remove-Item -Recurse -Force `$env:USERPROFILE\.claude-ads"
}

Main
