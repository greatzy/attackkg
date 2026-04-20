# 简单启动脚本
Write-Host "启动后端服务器..." -ForegroundColor Green

# 设置环境变量
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"

# 启动服务器
python run.py
