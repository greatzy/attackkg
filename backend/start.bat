@echo off
chcp 65001 >nul
echo ================================================
echo        网络安全攻击知识库系统 - 启动脚本
echo ================================================
echo.

:: 颜色定义
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "NC=[0m"

:: 项目根目录
set "PROJECT_ROOT=%~dp0"
set "FRONTEND_DIR=%PROJECT_ROOT%\..\frontend"

:: 日志函数
:log_info
    echo %GREEN%INFO: %~1%NC%
    goto :eof

:log_warning
    echo %YELLOW%WARNING: %~1%NC%
    goto :eof

:log_error
    echo %RED%ERROR: %~1%NC%
    goto :eof

:: 检查Python环境
:check_python
    set "PYTHON_CMD="
    
    where python >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python"
    ) else (
        where python3 >nul 2>&1
        if %errorlevel% equ 0 (
            set "PYTHON_CMD=python3"
        ) else (
            call :log_error "未找到 Python，请先安装 Python 3.9 或更高版本"
            pause
            exit /b 1
        )
    )
    
    for /f "tokens=*" %%i in ('%PYTHON_CMD% --version 2^>^&1') do (
        set "PYTHON_VERSION=%%i"
    )
    set "PYTHON_VERSION=%PYTHON_VERSION:~7%"
    
    echo %GREEN%Python 版本: %PYTHON_VERSION%%NC%
    
    :: 检查Python版本
    for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
        set "MAJOR_VERSION=%%a"
        set "MINOR_VERSION=%%b"
    )
    
    if %MAJOR_VERSION% lss 3 (
        call :log_error "需要 Python 3.9 或更高版本"
        pause
        exit /b 1
    )
    if %MAJOR_VERSION% equ 3 (
        if %MINOR_VERSION% lss 9 (
            call :log_error "需要 Python 3.9 或更高版本"
            pause
            exit /b 1
        )
    )
    
    goto :eof

:: 创建虚拟环境
:create_virtualenv
    if not exist "venv" (
        call :log_info "创建虚拟环境..."
        %PYTHON_CMD% -m venv venv
    )
    goto :eof

:: 激活虚拟环境
:activate_virtualenv
    call :log_info "激活虚拟环境..."
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
    ) else (
        call :log_error "虚拟环境未找到"
        pause
        exit /b 1
    )
    goto :eof

:: 安装依赖
:install_dependencies
    call :log_info "安装依赖..."
    pip install -q -r requirements.txt
    if %errorlevel% neq 0 (
        call :log_error "依赖安装失败"
        pause
        exit /b 1
    )
    goto :eof

:: 初始化数据库
:init_database
    call :log_info "初始化数据库..."
    if not exist "migrations" (
        echo 初始化数据库迁移...
        flask db init
    )
    
    echo 生成数据库迁移脚本...
    flask db migrate -m "Initial migration"
    
    echo 执行数据库迁移...
    flask db upgrade
    goto :eof

:: 检查并初始化
:check_and_init
    call :log_info "检查项目状态..."
    
    if not exist "venv" (
        call :create_virtualenv
    )
    
    call :activate_virtualenv
    call :install_dependencies
    
    if not exist ".env" (
        call :log_warning "未找到 .env 文件，复制示例配置..."
        copy .env.example .env
    )
    
    call :init_database
    goto :eof

:: 启动服务器
:start_server
    call :log_info "启动服务器..."
    
    :: 检查是否有进程在端口 5000 运行
    for /f "tokens=5" %%i in ('netstat -ano ^| findstr :5000') do (
        call :log_warning "端口 5000 已被占用 (PID: %%i)，将强制终止..."
        taskkill /F /PID %%i >nul 2>&1
        timeout /t 2 >nul
    )
    
    :: 设置Flask配置
    set FLASK_APP=run.py
    set FLASK_ENV=development
    set FLASK_DEBUG=True
    
    call :log_info "服务器将在 http://localhost:5000 启动"
    echo 按 Ctrl+C 停止服务器
    echo.
    
    flask run --host=0.0.0.0 --port=5000
    if %errorlevel% neq 0 (
        call :log_error "服务器启动失败"
        pause
        exit /b 1
    )
    goto :eof

:: 帮助信息
:show_help
    echo ================================================
    echo 网络安全攻击知识库系统 - 启动脚本
    echo ================================================
    echo Usage: start.bat [options]
    echo.
    echo Options:
    echo   -h, --help     显示帮助信息
    echo   -i, --init     初始化项目（创建虚拟环境、安装依赖、初始化数据库）
    echo   -s, --start    启动服务器（如果未初始化，会自动执行初始化）
    echo   -c, --check    检查环境（不执行任何操作，只检查依赖）
    echo.
    echo Examples:
    echo   start.bat --init       初始化项目
    echo   start.bat --start      启动服务器
    echo   start.bat --check      检查环境
    echo.
    pause
    goto :eof

:: 主函数
:main
    if "%~1" == "-h" goto :show_help
    if "%~1" == "--help" goto :show_help
    if "%~1" == "-c" goto :check_env
    if "%~1" == "--check" goto :check_env
    if "%~1" == "-i" goto :init_only
    if "%~1" == "--init" goto :init_only
    if "%~1" == "-s" goto :start_server_only
    if "%~1" == "--start" goto :start_server_only
    
    :: 默认启动
    call :check_env
    if %errorlevel% neq 0 goto :end
    
    call :check_and_init
    call :start_server
    goto :end

:: 检查环境
:check_env
    call :log_info "检查项目环境..."
    call :check_python
    goto :eof

:: 初始化项目
:init_only
    call :check_env
    if %errorlevel% neq 0 goto :end
    
    call :check_and_init
    call :log_info "项目初始化完成"
    call :log_info "接下来可以使用 start.bat --start 启动服务器"
    pause
    goto :end

:: 启动服务器
:start_server_only
    call :check_env
    if %errorlevel% neq 0 goto :end
    
    call :check_and_init
    call :start_server
    goto :end

:end
    call :log_info "程序已结束"
    pause
    exit /b 0

:: 主程序入口
call :main %*
