# OmniRoute Local Gateway Launcher
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  🚀 Launching OmniRoute AI Gateway & Token Saver" -ForegroundColor Green
Write-Host "  🛡️ Caveman & RTK Prompt Compression Active" -ForegroundColor Yellow
Write-Host "  🔗 Endpoint: http://localhost:11411/v1/chat/completions" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan

python "$PSScriptRoot\omniroute_proxy.py"
