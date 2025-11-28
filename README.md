# 企业微信机器人API服务

## 项目简介

企业微信机器人API服务是一个基于Flask框架开发的Web服务，用于接收外部请求并将消息转发到企业微信机器人。

## 功能特性

- 支持JSON和Form-Data两种请求格式
- 提供健康检查接口
- 完善的日志记录
- 支持中文响应
- 简单易用的API接口
- 支持从环境变量读取多个webhook地址
- 向所有配置的机器人发送消息
- 返回详细的发送结果

## 快速开始

### 环境要求

- Python 3.8+
- pip
- 虚拟环境（推荐）

### 安装依赖

1. 创建虚拟环境（推荐）
   ```bash
   python3 -m venv venv
   ```

2. 激活虚拟环境
   ```bash
   source venv/bin/activate
   ```

3. 安装依赖
   ```bash
   pip install flask requests
   ```

### 配置

通过环境变量配置企业微信机器人Webhook地址，支持多个地址用逗号分隔：

```bash
# Linux/macOS - 单个地址
export WECHAT_ROBOT_URLS="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-webhook-key"

# Linux/macOS - 多个地址
export WECHAT_ROBOT_URLS="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key1,https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key2"

# Windows (cmd) - 单个地址
set WECHAT_ROBOT_URLS="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-webhook-key"

# Windows (cmd) - 多个地址
set WECHAT_ROBOT_URLS="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key1,https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key2"

# Windows (PowerShell) - 单个地址
$env:WECHAT_ROBOT_URLS="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-webhook-key"

# Windows (PowerShell) - 多个地址
$env:WECHAT_ROBOT_URLS="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key1,https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key2"
```

或者，您也可以直接编辑 `config.py` 文件，设置默认值：

```python
# 从环境变量读取企业微信机器人Webhook地址，支持多个地址用逗号分隔
WECHAT_ROBOT_URLS = [url.strip() for url in os.environ.get("WECHAT_ROBOT_URLS", "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-webhook-key").split(",") if url.strip()]
```

### 运行项目

#### 方法一：直接运行

1. 从项目根目录的父目录运行：
   ```bash
   cd ..
   python3 -m wechat_rebot_api.app
   ```

2. 或者使用项目根目录下的命令：
   ```bash
   source venv/bin/activate && python -m wechat_rebot_api.app
   ```

#### 方法二：使用Docker

1. 构建Docker镜像：
   ```bash
   docker build -t wechat-robot-api .
   ```

2. 运行Docker容器：
   ```bash
   docker run -d -p 5000:5000 --name wechat-robot-api -e WECHAT_ROBOT_URLS="your-webhook-urls" wechat-robot-api
   ```

#### 方法三：使用docker-compose

1. 创建.env文件（可选）：
   ```bash
   echo "WECHAT_ROBOT_URLS=your-webhook-urls" > .env
   ```

2. 启动服务：
   ```bash
   docker-compose up -d
   ```

3. 停止服务：
   ```bash
   docker-compose down
   ```

#### 方法四：使用Kubernetes

1. 应用Deployment和Service配置：
   ```bash
   kubectl apply -f k8s-deployment.yaml
   ```

2. 查看部署状态：
   ```bash
   kubectl get deployments
   kubectl get pods
   kubectl get services
   ```

3. 查看日志：
   ```bash
   kubectl logs -f deployment/wechat-robot-api
   ```

4. 删除部署：
   ```bash
   kubectl delete -f k8s-deployment.yaml
   ```

#### 服务访问地址

- 直接运行/Docker/docker-compose：http://127.0.0.1:5000
- Kubernetes：通过Service IP或Ingress访问


## 前端页面

### 访问地址

服务启动后，可以通过以下地址访问前端页面：
- http://127.0.0.1:5000/static/index.html

### 功能说明

1. **消息发送**：在文本框中输入消息内容，点击"发送消息"按钮即可发送到企业微信机器人
2. **快捷键支持**：按住Ctrl+Enter键可以快速发送消息
3. **清空内容**：点击"清空内容"按钮可以清空文本框
4. **发送历史**：自动保存最近20条发送记录，包含发送时间和内容
5. **状态提示**：显示发送状态，包括成功、失败和发送中

### 页面特点

- 现代化的渐变背景设计
- 响应式布局，支持移动端
- 流畅的动画效果
- 清晰的状态反馈
- 简洁易用的界面

## API文档

### 接口列表

| 接口地址 | 请求方法 | 功能描述 |
|---------|---------|---------|
| / | GET | 首页，返回欢迎信息 |
| /health | GET | 健康检查接口 |
| /send-message | POST | 发送消息到企业微信机器人 |
| /static/index.html | GET | 前端页面 |

### 发送消息接口

**接口地址**：`/send-message`

**请求方法**：`POST`

**支持格式**：
- JSON
- Form-Data

**请求参数**：

| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| content | string | 是 | 要发送的消息内容 |
| webhook_urls | string | 否 | 额外的机器人地址，多个地址用逗号分隔 |

**请求示例**：

1. JSON格式 - 仅发送消息
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"content": "测试消息"}' http://127.0.0.1:5000/send-message
   ```

2. JSON格式 - 发送消息并指定额外机器人地址
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"content": "测试消息", "webhook_urls": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key1,https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key2"}' http://127.0.0.1:5000/send-message
   ```

3. Form-Data格式 - 仅发送消息
   ```bash
   curl -X POST -F "content=测试消息" http://127.0.0.1:5000/send-message
   ```

4. Form-Data格式 - 发送消息并指定额外机器人地址
   ```bash
   curl -X POST -F "content=测试消息" -F "webhook_urls=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key1,https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key2" http://127.0.0.1:5000/send-message
   ```

**响应示例**：

1. 全部发送成功
   ```json
   {
     "success": true,
     "message": "消息发送成功，共发送到 2 个机器人",
     "timestamp": "2025-11-27T19:22:28.536123"
   }
   ```

2. 部分发送成功
   ```json
   {
     "success": false,
     "message": "部分消息发送成功，成功 1 个，失败 1 个。错误信息: 消息发送失败到 https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key2: invalid webhook url",
     "timestamp": "2025-11-27T19:22:28.536123"
   }
   ```

3. 全部发送失败
   ```json
   {
     "success": false,
     "message": "所有消息发送失败。错误信息: 消息发送失败到 https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key1: invalid webhook url; 消息发送失败到 https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=key2: invalid webhook url",
     "timestamp": "2025-11-27T19:22:28.536123"
   }
   ```

### 健康检查接口

**接口地址**：`/health`

**请求方法**：`GET`

**响应示例**：

```json
{
  "status": "healthy",
  "timestamp": "2025-11-27T19:22:28.536123"
}
```

### 首页接口

**接口地址**：`/`

**请求方法**：`GET`

**响应示例**：

```json
{
  "message": "欢迎使用企业微信机器人接口"
}
```

## 项目结构

```
wechat_rebot_api/
├── __init__.py          # 包初始化文件
├── app.py               # 应用入口
├── api.py               # API路由定义
├── config.py            # 配置信息
├── wechat_service.py    # 企业微信机器人服务
├── wechat_robot.log     # 日志文件
├── venv/                # 虚拟环境（可选）
└── README.md            # 项目说明文档
```

## 日志说明

日志文件位于项目根目录下的 `wechat_robot.log`，包含以下信息：
- 时间戳
- 模块名
- 日志级别
- 日志消息

同时，日志也会输出到控制台。

## 注意事项

1. 请确保企业微信机器人Webhook地址配置正确
2. 建议在生产环境中使用WSGI服务器（如Gunicorn）部署
3. 生产环境中请关闭调试模式
4. 定期清理日志文件，避免占用过多磁盘空间

## 许可证

MIT License
