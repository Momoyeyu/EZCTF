# EZCTF - 网安实践 CTF 平台

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.112+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Vue.js](https://img.shields.io/badge/vue-2.x-green.svg)](https://vuejs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)

[中文文档](README_zh.md) | [English](README.md)

EZCTF 是一个前后端分离的现代化 CTF (Capture The Flag) 竞赛平台，专为网络安全实践课程设计。本项目采用了最新的 FastAPI 后端架构与 Vue.js 前端框架，实现了从题目管理、动态容器调度到实时排行的完整功能。

## ✨ 特性 (Features)

- **现代化后端**: 基于 **FastAPI** (Python 3.12+) 构建，集成 **SQLModel** (SQLAlchemy + Pydantic) 与 **PostgreSQL**。
- **响应式前端**: 使用 **Vue.js** 配合 **Element UI** 组件库，提供美观流畅的用户交互体验。
- **核心功能**:
    - **题目系统**: 支持 Web, Pwn, Reverse, Crypto, Misc 等多类型题目展示与附件下载。
    - **动态环境**: 支持动态容器实例的创建与销毁 (Web/Pwn 题型)。
    - **判题系统**: 动态 Flag 验证与积分结算。
    - **排行榜**: 实时更新的用户与战队积分排行榜。
- **用户与战队**:
    - 完整的用户注册、登录 (JWT 鉴权)、个人中心。
    - 战队系统：创建战队、加入/退出战队、队长管理（踢人、转让队长）。
- **工程化实践**:
    - **自动迁移**: 集成 **Alembic**，服务启动时自动同步数据库结构。
    - **依赖管理**: 后端使用 **uv** 进行极速包管理。
    - **单元测试**: 完善的 Pytest 测试用例覆盖核心逻辑。

## 📂 项目结构

```text
EZCTF/
├── backend/                # FastAPI 后端项目
│   ├── challenges/         # 题目附件与 Docker 环境配置
│   ├── src/                # 后端源代码
│   │   ├── common/         # 通用工具 (安全、错误处理)
│   │   ├── conf/           # 配置与数据库连接
│   │   ├── middleware/     # 中间件 (JWT 鉴权)
│   │   ├── task/           # 题目模块 (CRUD, 判题)
│   │   ├── team/           # 战队模块
│   │   ├── user/           # 用户模块
│   │   ├── main.py         # 应用入口
│   │   └── tests/          # 单元测试
│   ├── pyproject.toml      # 后端依赖配置
│   └── run.sh              # 后端独立启动脚本
├── ezctf.top/
│   └── ezctf/              # Vue.js 前端项目
│       ├── src/
│       │   ├── components/ # Vue 组件 (Element UI)
│       │   ├── views/      # 页面视图
│       │   ├── UserSystemApi/ # 前后端交互 API
│       │   └── ...
│       ├── package.json    # 前端依赖配置
│       └── run.sh          # 前端独立启动脚本
├── run.sh                  # 项目一键启动脚本
├── stop.sh                 # 项目一键停止脚本
└── README.md               # 项目说明文档
```

## 🚀 快速开始 (Getting Started)

### 前置要求

- **Python 3.12+** & **uv** (推荐)
- **Node.js** & **npm**
- **PostgreSQL** (默认配置: 数据库 `ezctf`, 用户/密码 `postgres/postgres`)

### 一键启动 (推荐)

项目根目录下提供了便捷的启动与停止脚本：

1.  **启动服务**
    ```bash
    ./run.sh
    ```
    该脚本会自动检测环境、安装依赖并启动前后端服务。
    - 后端 API: `http://localhost:8000`
    - 前端页面: `http://localhost:8080`

2.  **停止服务**
    ```bash
    ./stop.sh
    ```

### 手动启动 (Manual Startup)

如果需要单独调试前后端，可以按照以下步骤操作：

#### Backend 启动

1.  **进入后端目录**
    ```bash
    cd backend
    ```

2.  **启动服务**
    ```bash
    chmod +x run.sh
    ./run.sh
    ```
    API 文档地址: `http://localhost:8000/docs`

#### Frontend 启动

1.  **进入前端目录**
    ```bash
    cd ezctf.top/ezctf
    ```

2.  **启动服务**
    ```bash
    chmod +x run.sh
    ./run.sh
    ```
    访问地址: `http://localhost:8080`

## 🛠 开发指南

### 数据库迁移 (Backend)

本项目使用 **Alembic** 进行数据库模式迁移。

```bash
cd backend
# 生成迁移脚本 (修改 Model 后)
uv run alembic revision --autogenerate -m "description"

# 手动应用迁移 (服务启动时会自动执行)
uv run alembic upgrade head
```

### 运行测试

运行 Pytest 测试套件：

```bash
cd backend
uv run pytest
```

## 📄 原始需求 (Original Requirements)

### CTF网站开发
- 支持Web、Reverse、Pwn等常见题型
- 部署多类题目
- 战队/个人排名
- 实名制登陆

### 报告要求
- 设计文档、测试文档、展示文档
- 可编译代码、演示视频
