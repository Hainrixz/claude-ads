#Requires -Version 5.1
<#
.SYNOPSIS
    Claude Ads Installer for Windows
.DESCRIPTION
    Installs the Claude Ads skill, sub-skills, agents, and reference files
    for Claude Code on Windows systems.
#>

$ErrorActionPreference = "Stop"

function Main {
    $SkillDir = Join-Path $env:USERPROFILE ".claude\skills\ads"
    $AgentDir = Join-Path $env:USERPROFILE ".claude\agents"
    $RepoUrl = "https://github.com/Hainrixz/claude-ads"

    Write-Host "=================================="
    Write-Host "   Claude Ads - Installer"
    Write-Host "   Claude Code Paid Ads Skill"
    Write-Host "=================================="
    Write-Host ""

    # Check prerequisites
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "X Git is required but not installed." -ForegroundColor Red
        exit 1
    }
    Write-Host "OK Git detected" -ForegroundColor Green

    # Create directories
    New-Item -ItemType Directory -Path (Join-Path $SkillDir "references") -Force | Out-Null
    New-Item -ItemType Directory -Path $AgentDir -Force | Out-Null

    # Clone to temp directory
    $TempDir = Join-Path $env:TEMP "claude-ads-install-$(Get-Random)"
    Write-Host "Downloading Claude Ads..."

    try {
        # Temporarily allow stderr (git writes progress to stderr — treated as error in PS 5.1)
        $ErrorActionPreference = "Continue"
        git clone --depth 1 $RepoUrl "$TempDir\claude-ads" 2>&1 | Out-Null
        $ErrorActionPreference = "Stop"
        if ($LASTEXITCODE -ne 0) { throw "Git clone failed" }

        # Copy main skill + references
        Write-Host "Installing skill files..."
        Copy-Item "$TempDir\claude-ads\ads\SKILL.md" -Destination "$SkillDir\SKILL.md" -Force
        Copy-Item "$TempDir\claude-ads\ads\references\*.md" -Destination "$SkillDir\references\" -Force

        # Copy sub-skills
        Write-Host "Installing sub-skills..."
        Get-ChildItem "$TempDir\claude-ads\skills" -Directory | ForEach-Object {
            $TargetDir = Join-Path $env:USERPROFILE ".claude\skills\$($_.Name)"
            New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
            Copy-Item (Join-Path $_.FullName "SKILL.md") -Destination "$TargetDir\SKILL.md" -Force

            # Copy assets (industry templates) if they exist
            $AssetsDir = Join-Path $_.FullName "assets"
            if (Test-Path $AssetsDir) {
                $TargetAssets = Join-Path $TargetDir "assets"
                New-Item -ItemType Directory -Path $TargetAssets -Force | Out-Null
                Copy-Item "$AssetsDir\*.md" -Destination "$TargetAssets\" -Force
            }
        }

        # Copy agents
        Write-Host "Installing subagents..."
        Copy-Item "$TempDir\claude-ads\agents\*.md" -Destination "$AgentDir\" -Force

        # Copy scripts (optional Python tools)
        $ScriptsSource = "$TempDir\claude-ads\scripts"
        if (Test-Path $ScriptsSource) {
            Write-Host "Installing Python scripts..."
            $ScriptsDir = Join-Path $SkillDir "scripts"
            New-Item -ItemType Directory -Path $ScriptsDir -Force | Out-Null
            Copy-Item "$ScriptsSource\*.py" -Destination "$ScriptsDir\" -Force
            Copy-Item "$TempDir\claude-ads\requirements.txt" -Destination "$SkillDir\requirements.txt" -Force
        }

        # Install Python dependencies (landing page analysis, image validation)
        Write-Host ""
        Write-Host "Installing Python dependencies..."
        $ErrorActionPreference = "Continue"
        pip install -q -r "$SkillDir\requirements.txt" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  OK Python dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "  Warning: pip install failed. Run manually: pip install -r $SkillDir\requirements.txt" -ForegroundColor Yellow
        }
        $ErrorActionPreference = "Stop"

        # Check for banana-claude (image generation provider)
        Write-Host ""
        $BananaPath = Join-Path $env:USERPROFILE ".claude\skills\banana\SKILL.md"
        if (Test-Path $BananaPath) {
            Write-Host "  OK banana-claude detected (image generation ready)" -ForegroundColor Green
        } else {
            Write-Host "  Warning: banana-claude not installed. Image generation requires it." -ForegroundColor Yellow
            Write-Host "    Install banana-claude (third-party skill), then run: /banana setup (to configure API key)"
        }

        Write-Host ""
        Write-Host "Claude Ads installed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "  Installed:"
        Write-Host "    - 1 main skill (ads orchestrator)"
        Write-Host "    - 19 sub-skills (platform + functional + creative)"
        Write-Host "    - 10 agents (6 audit + 4 creative)"
        Write-Host "    - 25 reference files"
        Write-Host "    - 12 industry templates"
        Write-Host ""
        Write-Host "Usage:"
        Write-Host "  1. Start Claude Code:  claude"
        Write-Host "  2. Run commands:       /ads audit"
        Write-Host "                         /ads plan saas"
        Write-Host "                         /ads google"
    }
    finally {
        # Cleanup temp directory
        if (Test-Path $TempDir) {
            Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}

Main
