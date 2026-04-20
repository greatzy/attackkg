# 网络安全攻击知识库系统

## 项目概述

基于MITRE ATT&CK框架的智能防御平台，提供网络安全知识库管理、威胁情报分析、可视化攻击路径等功能。

## 技术架构

### 前端技术栈
- **Vue 3 + TypeScript**：现代化前端框架
- **Element Plus**：UI组件库
- **ECharts + d3 + Cytoscape**：可视化库
- **Pinia**：状态管理
- **Vue Router**：路由管理
- **Vite**：构建工具

### 后端技术栈
- **Flask**：轻量级Python Web框架
- **SQLAlchemy**：ORM数据库映射
- **PostgreSQL**：关系型数据库
- **Redis**：缓存和任务队列
- **Celery**：异步任务处理
- **mitreattack-python**：ATT&CK数据解析

## 功能模块

### 核心功能
1. **知识库管理**：战术、技术、子技术、缓解措施、软件管理
2. **威胁行为者**：威胁组织、使用技术、关联软件
3. **检测规则**：规则管理、技术关联、测试验证
4. **可视化分析**：ATT&CK矩阵、攻击路径图谱、威胁关联图谱
5. **威胁情报**：情报查询、风险评估、自动化分析
6. **安全报告**：报告生成、导出、预览
7. **系统管理**：用户管理、角色权限、操作日志

### 特色功能
- ATT&CK数据自动同步
- 交互式攻击路径分析
- 威胁情报关联分析
- 检测规则自动测试
- 安全报告一键生成

## 快速开始

### 环境要求
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+

### 后端部署

1. **创建虚拟环境**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **环境配置**
   ```bash
   cp .env.example .env
   # 编辑.env文件，配置数据库、Redis等信息
   ```

4. **数据库初始化**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **启动服务器**
   ```bash
   # 开发模式
   flask run --debug

   # 生产模式
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

### 前端部署

1. **安装依赖**
   ```bash
   cd frontend
   npm install
   ```

2. **配置环境**
   ```bash
   cp .env.example .env
   # 编辑.env文件，配置API基础地址
   ```

3. **启动开发服务器**
   ```bash
   npm run dev
   ```

4. **生产构建**
   ```bash
   npm run build
   ```

## 项目结构

### 后端结构
```
backend/
├── app/
│   ├── api/              # API接口
│   ├── models/           # 数据模型
│   ├── services/         # 业务服务
│   ├── tasks/            # 异步任务
│   ├── utils/            # 工具函数
│   └── __init__.py       # 应用初始化
├── config/               # 配置文件
├── instance/             # 实例配置
├── migrations/           # 数据库迁移
├── requirements.txt      # 依赖声明
└── run.py                # 启动入口
```

### 前端结构
```
frontend/
├── src/
│   ├── api/              # API接口
│   ├── assets/           # 静态资源
│   ├── components/       # 公共组件
│   ├── layouts/          # 布局组件
│   ├── router/           # 路由配置
│   ├── stores/           # 状态管理
│   ├── styles/           # 全局样式
│   ├── types/            # TypeScript类型
│   ├── utils/            # 工具函数
│   ├── views/            # 页面组件
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
├── public/               # 公共资源
├── vite.config.ts        # Vite配置
├── tsconfig.json         # TypeScript配置
└── package.json          # 依赖声明
```

## API文档

启动后端服务后，访问 `http://localhost:5000/api/docs` 查看Swagger API文档。

## 部署建议

### 开发环境
```bash
# 使用Docker Compose启动开发环境
cd deploy/docker
docker-compose up -d
```

### 生产环境
```bash
# 使用Docker Compose启动生产环境
cd deploy/docker
docker-compose -f docker-compose.prod.yml up -d
```

## 维护说明

### 数据同步
```bash
# 同步ATT&CK数据
flask sync:attack

# 定时同步（Celery Beat）
celery -A app.celery worker -B -l info
```

### 系统监控
```bash
# 启动Flower监控Celery任务
celery -A app.celery flower --port=5555
```

### 日志管理
```bash
# 查看应用日志
tail -f logs/attackkg.log

# 查看Celery日志
tail -f logs/celery.log
```

## 安全注意事项

1. **API访问控制**：使用JWT认证，配置CORS策略
2. **数据加密**：敏感数据加密存储
3. **输入验证**：全面验证用户输入，防止XSS和SQL注入
4. **权限管理**：基于RBAC的细粒度权限控制
5. **审计日志**：记录所有重要操作和安全事件

## 许可证

MIT License

## 联系方式

如有问题，请通过以下方式联系：
- 邮箱：support@example.com
- 技术支持：010-12345678
# attackkg
