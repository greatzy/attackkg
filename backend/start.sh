#!/bin/bash

# 网络安全攻击知识库系统 - 启动脚本
# 使用前请确保已安装 Python 3.9+ 和相关依赖

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 项目根目录
PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BACKEND_DIR="$PROJECT_ROOT"
FRONTEND_DIR="$PROJECT_ROOT/../frontend"

# 日志函数
log_info() {
    echo -e "${GREEN}INFO: ${1}${NC}"
}

log_warning() {
    echo -e "${YELLOW}WARNING: ${1}${NC}"
}

log_error() {
    echo -e "${RED}ERROR: ${1}${NC}"
}

# 检查命令是否存在
check_command() {
    if ! command -v "$1" > /dev/null 2>&1; then
        log_error "命令 '$1' 未找到，请先安装"
        return 1
    fi
    return 0
}

# 检查Python版本
check_python_version() {
    if check_command python3; then
        PYTHON_CMD="python3"
    elif check_command python; then
        PYTHON_CMD="python"
    else
        log_error "Python 未找到"
        return 1
    fi

    local PYTHON_VERSION
    PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    
    log_info "Python 版本: $PYTHON_VERSION"
    
    local MAJOR_VERSION
    MAJOR_VERSION=${PYTHON_VERSION%%.*}
    local MINOR_VERSION
    MINOR_VERSION=${PYTHON_VERSION#*.}
    
    if [ "$MAJOR_VERSION" -lt 3 ] || [ "$MINOR_VERSION" -lt 9 ]; then
        log_error "需要 Python 3.9 或更高版本，当前版本: $PYTHON_VERSION"
        return 1
    fi
    
    return 0
}

# 创建虚拟环境
create_virtualenv() {
    if [ ! -d "venv" ]; then
        log_info "创建虚拟环境..."
        "$PYTHON_CMD" -m venv venv
    fi
}

# 激活虚拟环境
activate_virtualenv() {
    log_info "激活虚拟环境..."
    if [ -f "venv/bin/activate" ]; then
        . venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        . venv/Scripts/activate
    else
        log_error "虚拟环境未找到"
        return 1
    fi
}

# 安装依赖
install_dependencies() {
    log_info "检查并更新依赖..."
    if ! pip install -q -r requirements.txt; then
        log_error "依赖安装失败"
        return 1
    fi
}

# 检查数据库连接
check_database() {
    log_info "检查数据库连接..."
    if ! python -c "
from app import create_app, db
from app.models import *

app = create_app('development')
with app.app_context():
    try:
        # 检查数据库连接
        db.session.execute('SELECT 1')
        print('数据库连接正常')
        
        # 检查表是否存在
        tables = db.metadata.tables.keys()
        if 'users' in tables and 'tactics' in tables:
            print('数据库表结构完整')
        else:
            print('数据库表结构不完整，需要初始化')
    except Exception as e:
        print(f'数据库连接失败: {e}')
        raise
    finally:
        db.session.remove()
" > /dev/null 2>&1; then
        log_warning "数据库连接失败或表结构不完整，将尝试初始化..."
        return 1
    fi
    return 0
}

# 初始化数据库
init_database() {
    log_info "初始化数据库..."
    if flask db init 2>/dev/null || true; then
        log_info "数据库迁移仓库已初始化"
    fi
    
    if flask db migrate -m "Initial migration" 2>/dev/null || true; then
        log_info "数据库迁移脚本已生成"
    fi
    
    if flask db upgrade 2>/dev/null || true; then
        log_info "数据库已更新"
    fi
}

# 启动服务器
start_server() {
    log_info "启动Flask开发服务器..."
    export FLASK_APP=run.py
    export FLASK_ENV=development
    export FLASK_DEBUG=True
    
    # 检查是否有其他进程正在运行
    local PID=$(lsof -ti :5000 || netstat -tuln 2>/dev/null | grep :5000 | awk '{print $7}' | cut -d/ -f1 2>/dev/null || ss -tuln 2>/dev/null | grep :5000 | awk '{print $7}' | cut -d, -f2 2>/dev/null || true)
    
    if [ -n "$PID" ]; then
        log_warning "端口 5000 已被占用 (PID: $PID)，将强制终止"
        kill -9 "$PID" 2>/dev/null || true
        sleep 2
    fi
    
    # 启动服务器
    log_info "服务器将在 http://localhost:5000 启动"
    log_info "按 Ctrl+C 停止服务器"
    
    if flask run --host=0.0.0.0 --port=5000; then
        log_info "服务器启动成功"
    else
        log_error "服务器启动失败"
        return 1
    fi
}

# 显示帮助信息
show_help() {
    echo "网络安全攻击知识库系统 - 启动脚本"
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help     显示帮助信息"
    echo "  -i, --init     初始化项目（创建虚拟环境、安装依赖、初始化数据库）"
    echo "  -s, --start    启动服务器（如果未初始化，会自动执行初始化）"
    echo "  -d, --debug    调试模式启动"
    echo "  -c, --check    检查环境（不执行任何操作，只检查依赖）"
    echo ""
    echo "Examples:"
    echo "  $0 --init       初始化项目"
    echo "  $0 --start      启动服务器"
    echo "  $0 --check      检查环境"
    echo "  $0 --debug      调试模式启动"
}

# 主函数
main() {
    local ACTION="start"
    
    while [ "$#" -gt 0 ]; do
        case $1 in
            -h|--help)
                show_help
                return 0
                ;;
            -i|--init)
                ACTION="init"
                ;;
            -s|--start)
                ACTION="start"
                ;;
            -d|--debug)
                ACTION="debug"
                ;;
            -c|--check)
                ACTION="check"
                ;;
            *)
                log_error "未知选项: $1"
                show_help
                return 1
                ;;
        esac
        shift
    done
    
    log_info "网络安全攻击知识库系统 - $ACTION"
    
    cd "$BACKEND_DIR" || exit 1
    
    # 检查Python环境
    if ! check_python_version; then
        return 1
    fi
    
    # 检查并初始化虚拟环境
    if [ "$ACTION" != "check" ]; then
        create_virtualenv
        activate_virtualenv
        install_dependencies
    fi
    
    if [ "$ACTION" = "check" ]; then
        log_info "环境检查完成"
        return 0
    fi
    
    # 配置环境变量
    if [ ! -f ".env" ]; then
        log_warning "未找到 .env 文件，将复制示例配置"
        cp .env.example .env
    fi
    
    # 初始化数据库
    if ! check_database; then
        init_database
    fi
    
    # 启动服务器
    if [ "$ACTION" = "init" ]; then
        log_info "项目初始化完成"
        log_info "接下来可以使用 $0 --start 启动服务器"
        return 0
    fi
    
    start_server
}

# 捕获Ctrl+C信号
trap 'log_info "服务器已停止"; exit 0' INT

# 执行主函数
if main "$@"; then
    exit 0
else
    exit 1
fi
