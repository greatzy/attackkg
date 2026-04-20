# AttackKg - 网络安全攻击知识库系统

基于 MITRE ATT&CK 框架的知识管理和可视化平台。

## 项目简介

AttackKg 是一个用于管理和可视化 MITRE ATT&CK 框架数据的系统，帮助安全团队高效管理和分析攻击技术数据。

## 核心功能

- **知识管理**：战术、技术、子技术、缓解措施的管理和查询
- **可视化分析**：攻击矩阵、攻击路径图谱、关联分析
- **数据导入**：支持 MITRE 官方 STIX 格式数据导入
- **用户管理**：基于 RBAC 的权限控制系统

## 技术栈

### 前端
- Vue 3 + TypeScript
- Element Plus
- ECharts
- Vite

### 后端
- Flask
- SQLAlchemy
- JWT

### 数据库
- SQLite（开发环境）
- PostgreSQL（生产环境）

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 18+
- npm 或 yarn

### 安装

#### 后端

```bash
cd backend

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动服务
python run.py
```

#### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 访问

- 前端：http://localhost:5174
- 后端：http://localhost:5000

## 项目结构

```
attackKg/
├── backend/              # 后端代码
│   ├── app/
│   │   ├── api/         # API接口
│   │   ├── models/      # 数据模型
│   │   └── utils/       # 工具函数
│   ├── requirements.txt  # Python依赖
│   └── run.py           # 启动文件
├── frontend/             # 前端代码
│   ├── src/
│   │   ├── api/         # API调用
│   │   ├── views/       # 页面组件
│   │   └── ...
│   └── package.json      # Node依赖
├── docs/                 # 设计文档
└── result/              # 挑战赛成果
```

## 相关文档

- [概要设计说明书](docs/01-概要设计.md)
- [详细设计说明书](docs/02-详细设计.md)
- [使用手册](使用手册.md)
- [测试报告](测试报告.md)

## License

MIT License