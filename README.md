# MongoDB游戏用户管理系统

## 项目简介

MongoDB游戏用户管理系统是一个基于Flask和MongoDB开发的Web应用，用于管理游戏用户的基本信息、装备和积分。该系统充分利用了MongoDB的文档型数据库特性，支持嵌套文档操作和聚合查询，提供了直观的用户界面和丰富的功能。

## 技术栈

### 后端
- **编程语言**: Python 3.8+
- **Web框架**: Flask 2.0+
- **数据库**: MongoDB 4.4+
- **数据库驱动**: pymongo

### 前端
- **HTML5, CSS3, JavaScript (ES6+)**
- **Bootstrap 5** - 用于响应式UI设计
- **Chart.js** - 用于数据可视化

## 功能特性

### 基础功能
- **用户管理**: 添加、查询、更新、删除用户
- **装备管理**: 添加、更新、删除装备
- **积分管理**: 增减积分、查询积分历史

### MongoDB特色功能
- **嵌套文档操作**: 装备和积分数据作为嵌套文档存储在用户文档中
- **聚合查询**: 实现了等级分布、装备类型分布、积分排行榜等统计功能

## 环境要求

- **操作系统**: Windows/Linux
- **Python**: 3.8+
- **MongoDB**: 4.4+

## 安装步骤

### 1. 安装MongoDB

#### Windows
1. 从MongoDB官网下载安装包：https://www.mongodb.com/try/download/community
2. 运行安装包，按照提示完成安装
3. 启动MongoDB服务：
   - 可以通过MongoDB Compass（图形化工具）启动
   - 或通过命令行启动：`mongod`

#### Linux (Ubuntu 24.04)
```bash
# 包数据加载 && 包管理升级
sudo apt-get update && sudo apt-get upgrade -y

# 安装gnupg curl
sudo apt-get install gnupg curl

# ubuntu 24.04
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list

sudo apt-get update

# 下载最新版本
sudo apt-get install -y mongodb-org

# 查看当前mongodb状态
sudo systemctl status mongod

# 启动mongodb服务
sudo systemctl start mongod

# 可选：设置开机自启动
sudo systemctl enable mongod

# 进入mongo服务
mongosh
```

### 2. 安装Python依赖

1. 克隆或下载项目代码到本地
2. 进入项目目录
3. 创建并激活虚拟环境（可选但推荐）：
   
   ```bash
   # 创建虚拟环境
   python -m venv venv
   
   # 激活虚拟环境
   # Windows
   venv\Scripts\activate
   # Linux
   source venv/bin/activate
   ```

4. 安装项目依赖：
   ```bash
   pip install flask pymongo
   ```

## 运行方法

### 1. 确保MongoDB服务正在运行

- Windows: 检查任务管理器中是否有mongod进程
- Linux: 运行 `sudo systemctl status mongod` 查看服务状态

### 2. 启动应用

在项目目录下运行：
```bash
python app.py
```

应用将在 `http://localhost:5000` 启动

### 3. 访问应用

在浏览器中输入以下URL访问应用：
- 主页面：http://localhost:5000
- 统计页面：http://localhost:5000/stats

## API接口说明

### 用户管理

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/users` | GET | 获取所有用户列表 |
| `/api/users` | POST | 添加新用户 |
| `/api/users/<user_id>` | GET | 获取单个用户详情 |
| `/api/users/<user_id>` | PUT | 更新用户信息 |
| `/api/users/<user_id>` | DELETE | 删除用户 |

### 装备管理

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/users/<user_id>/equipment` | POST | 添加装备 |
| `/api/users/<user_id>/equipment/<equipment_id>` | PUT | 更新装备 |
| `/api/users/<user_id>/equipment/<equipment_id>` | DELETE | 删除装备 |

### 积分管理

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/users/<user_id>/points` | POST | 更新积分 |

### 统计分析

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/stats/level-distribution` | GET | 获取等级分布 |
| `/api/stats/equipment-type-distribution` | GET | 获取装备类型分布 |
| `/api/stats/points-ranking` | GET | 获取积分排行榜 |

## 项目结构

```
game_user_management/
├── app.py              # 主应用入口
├── config.py           # 配置文件
├── models/             # 数据模型目录
├── routes/             # 路由目录
│   ├── user_routes.py  # 用户相关路由
│   ├── equipment_routes.py  # 装备相关路由
│   ├── points_routes.py     # 积分相关路由
│   └── stats_routes.py      # 统计相关路由
├── services/           # 服务层
│   └── mongo_service.py     # MongoDB服务
├── static/             # 静态资源目录
│   ├── css/            # CSS文件目录
│   ├── js/             # JavaScript文件目录
│   │   └── main.js     # 前端交互逻辑
│   └── images/         # 图片资源目录
├── templates/          # HTML模板目录
│   ├── index.html      # 主页面
│   ├── user_detail.html # 用户详情页面
│   └── stats.html      # 统计页面
└── README.md           # 项目说明文档
```

## 使用说明

### 1. 添加用户

1. 在主页面点击"添加用户"按钮
2. 填写用户名、昵称和等级
3. 点击"保存"按钮

### 2. 查看用户详情

1. 在主页面点击用户列表中的"详情"按钮
2. 查看用户的基本信息、装备列表和积分历史

### 3. 添加装备

1. 进入用户详情页面
2. 在装备列表部分点击"添加装备"按钮
3. 填写装备名称、类型、等级、攻击力和防御力
4. 点击"保存"按钮

### 4. 更新积分

1. 进入用户详情页面
2. 在积分信息部分点击"更新积分"按钮
3. 填写积分变动值（正数表示增加，负数表示扣除）和变动原因
4. 点击"保存"按钮

### 5. 查看统计数据

1. 在主页面点击"统计分析"按钮
2. 查看等级分布图表、装备类型分布图表和积分排行榜

## 注意事项

1. **MongoDB连接**：确保MongoDB服务正在运行，并且连接配置正确（默认连接到localhost:27017）

2. **配置修改**：可以通过修改`config.py`文件来调整MongoDB连接信息和Flask应用配置

3. **开发模式**：当前应用运行在开发模式下，生产环境部署时建议使用Gunicorn等WSGI服务器

4. **数据备份**：定期备份MongoDB数据库，以防止数据丢失

5. **安全考虑**：生产环境部署时，建议添加身份验证和授权机制，以及使用HTTPS协议

## 故障排除

### 无法连接到MongoDB

- 检查MongoDB服务是否正在运行
- 检查`config.py`中的MongoDB连接配置是否正确
- 检查防火墙设置，确保27017端口已开放

### 应用启动失败

- 检查Python版本是否符合要求（3.8+）
- 检查依赖包是否已正确安装
- 查看控制台输出的错误信息，根据错误信息进行排查

### 页面无法访问

- 检查应用是否正在运行
- 检查访问的URL是否正确
- 检查防火墙设置，确保5000端口已开放

