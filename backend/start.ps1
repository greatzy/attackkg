Write-Host "============================================" -ForegroundColor Green
Write-Host "        网络安全攻击知识库系统 - 启动脚本" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

# 检查Python环境
Write-Host "检查Python环境..." -ForegroundColor Green
$pythonCmd = $null

if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "未找到 Python，请先安装 Python 3.9 或更高版本" -ForegroundColor Red
    Read-Host "按 Enter 键退出..."
    exit 1
}

$pythonVersion = & $pythonCmd --version 2>&1
Write-Host "Python 版本: $pythonVersion" -ForegroundColor Green

# 检查Python版本
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $majorVersion = [int]$matches[1]
    $minorVersion = [int]$matches[2]
    
    if ($majorVersion -lt 3) {
        Write-Host "需要 Python 3.9 或更高版本" -ForegroundColor Red
        Read-Host "按 Enter 键退出..."
        exit 1
    }
    if ($majorVersion -eq 3 -and $minorVersion -lt 9) {
        Write-Host "需要 Python 3.9 或更高版本" -ForegroundColor Red
        Read-Host "按 Enter 键退出..."
        exit 1
    }
}

# 创建虚拟环境
if (-not (Test-Path "venv")) {
    Write-Host "创建虚拟环境..." -ForegroundColor Green
    & $pythonCmd -m venv venv
}

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Green
if (Test-Path "venv\Scripts\Activate.ps1") {
    . venv\Scripts\Activate.ps1
} else {
    Write-Host "虚拟环境未找到" -ForegroundColor Red
    Read-Host "按 Enter 键退出..."
    exit 1
}

# 安装依赖
Write-Host "安装依赖..." -ForegroundColor Green
pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "依赖安装失败" -ForegroundColor Red
    Read-Host "按 Enter 键退出..."
    exit 1
}

# 检查并复制 .env 文件
if (-not (Test-Path ".env")) {
    Write-Host "未找到 .env 文件，复制示例配置..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
}

# 初始化数据库
Write-Host "初始化数据库..." -ForegroundColor Green
if (-not (Test-Path "migrations")) {
    Write-Host "初始化数据库迁移..."
    flask db init
}

Write-Host "生成数据库迁移脚本..."
flask db migrate -m "Initial migration"

Write-Host "执行数据库迁移..."
flask db upgrade

# 检查端口 5000
Write-Host "检查端口 5000..." -ForegroundColor Green
$portInUse = netstat -ano | Select-String ":5000"
if ($portInUse) {
    $pid = $portInUse -split "\s+" | Select-Object -Last 1
    Write-Host "端口 5000 已被占用 (PID: $pid)，将强制终止..." -ForegroundColor Yellow
    taskkill /F /PID $pid 2>$null
    Start-Sleep -Seconds 2
}

# 设置环境变量
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "True"

Write-Host "服务器将在 http://localhost:5000 启动" -ForegroundColor Green
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Green
Write-Host ""

# 启动服务器
flask run --host=0.0.0.0 --port=5000
if ($LASTEXITCODE -ne 0) {
    Write-Host "服务器启动失败" -ForegroundColor Red
    Read-Host "按 Enter 键退出..."
    exit 1
}
