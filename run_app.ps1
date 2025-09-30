#!/usr/bin/env powershell
# PowerShell version of the app launcher

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PDF Policy Processor - Streamlit" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if API key is set
if (-not $env:BREVO_API_KEY) {
    Write-Host "⚠️  Warning: BREVO_API_KEY environment variable not set" -ForegroundColor Yellow
    Write-Host "Run: .\set_api_key.bat to configure it" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Starting web application..." -ForegroundColor Green
Write-Host "Open your browser to: http://localhost:8501" -ForegroundColor Green
Write-Host ""
Write-Host "Backend email integration: ENABLED" -ForegroundColor Blue
Write-Host "Email script: send_emails_brevo.py" -ForegroundColor Blue
Write-Host ""

# Start Streamlit
python -m streamlit run pdf_processor_final_working.py --server.headless false --server.port 8501