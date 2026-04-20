$scriptPath = $PSScriptRoot

Write-Host "=== System Diagnostic ===" -ForegroundColor Cyan
Write-Host "Script directory: $scriptPath"
Write-Host "Current directory: $(Get-Location)"
Write-Host ""

Write-Host "=== Python Installation ===" -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python version: $pythonVersion"
} catch {
    Write-Host "Error getting Python version: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Running extremely_simple.py ===" -ForegroundColor Green
try {
    $result = python "$scriptPath\extremely_simple.py" 2>&1
    if ($result) {
        Write-Host "Output:"
        Write-Host $result
    } else {
        Write-Host "No output received" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Running debug_system.py ===" -ForegroundColor Green
try {
    $result = python "$scriptPath\debug_system.py" 2>&1
    if ($result) {
        Write-Host "Output:"
        Write-Host $result
    } else {
        Write-Host "No output received" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor Red
}
