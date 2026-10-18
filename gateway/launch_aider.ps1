# Aider Pair Programming Launcher
param (
    [string]$Model = "ollama/qwen2.5-coder:1.5b",
    [string]$RepoPath = "."
)

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  🚀 Launching Aider Terminal Pair Programmer" -ForegroundColor Green
Write-Host "  🤖 Model: $Model" -ForegroundColor Yellow
Write-Host "  📁 Working Tree: $RepoPath" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan

# Set environment for local Ollama or OpenAI compatible gateway
$env:OLLAMA_API_BASE = "http://localhost:11434"

aider --model $Model --watch-files $RepoPath
