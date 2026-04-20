#!/usr/bin/env python
import os
import sys
import subprocess
import time

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("========================================")
print("    网络安全攻击知识库系统 - 启动脚本")
print("========================================")
print()

# 检查Python版本
print("检查Python环境...")
print(f"Python版本: {sys.version}")

# 安装依赖
print("\n安装依赖...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

# 检查并复制 .env 文件
if not os.path.exists(".env"):
    print("\n未找到 .env 文件，复制示例配置...")
    if os.path.exists(".env.example"):
        with open(".env.example", "r", encoding="utf-8") as f:
            content = f.read()
        with open(".env", "w", encoding="utf-8") as f:
            f.write(content)
        print("✓ .env 文件已创建")
    else:
        print("✗ .env.example 文件未找到")

# 初始化数据库
print("\n初始化数据库...")
from app import create_app, db
app = create_app('development')
with app.app_context():
    db.create_all()
    print("✓ 数据库初始化完成")

# 启动服务器
print("\n启动服务器...")
print("服务器将在 http://localhost:5000 启动")
print("按 Ctrl+C 停止服务器")
print()

# 运行服务器
from app import create_app
app = create_app('development')
app.run(host='0.0.0.0', port=5000, debug=True)
