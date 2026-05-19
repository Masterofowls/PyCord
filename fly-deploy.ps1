# fly-deploy.ps1 — provision pycord app + set secrets + deploy
$ErrorActionPreference = 'Continue'
$env:PATH += ";C:\Program Files\Git\cmd"
Set-Location 'C:\Users\mrdan\PyCord'
Get-Location

Write-Host '== fly auth ==' -ForegroundColor Cyan
fly auth whoami

Write-Host '== ensuring app exists ==' -ForegroundColor Cyan
fly apps create pycord --org personal 2>&1 | Out-String | Write-Host

# Generate a fresh Django SECRET_KEY (URL-safe random)
$bytes = New-Object byte[] 50
[System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
$SECRET_KEY = [Convert]::ToBase64String($bytes).Replace('+','-').Replace('/','_').TrimEnd('=')

Write-Host '== setting secrets ==' -ForegroundColor Cyan
fly secrets set `
  "SECRET_KEY=$SECRET_KEY" `
  "DATABASE_URL=postgres://postgres.xocqxtakhusoshgttmuq:F%40Hfmq%241U%401RpcRJ%2Ae%23b@aws-0-eu-west-1.pooler.supabase.com:6543/postgres" `
  "ALLOWED_HOSTS=pycord.fly.dev" `
  "CSRF_TRUSTED_ORIGINS=https://pycord.fly.dev" `
  "DEBUG=False" `
  "USE_REDIS=False" `
  "SUPABASE_URL=https://xocqxtakhusoshgttmuq.supabase.co" `
  "SUPABASE_PUBLISHABLE_KEY=sb_publishable_azbMd83ZNsLxsDYPUQIgtw_W4vPdWlh" `
  "PASSKEY_RP_ID=pycord.fly.dev" `
  "PASSKEY_RP_NAME=PyCord" `
  "EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend" `
  "DEFAULT_FROM_EMAIL=PyCord <noreply@pycord.fly.dev>" `
  --app pycord --stage

Write-Host '== deploying ==' -ForegroundColor Cyan
fly deploy --remote-only --app pycord

Write-Host '== status ==' -ForegroundColor Cyan
fly status --app pycord
