# 企业微信机器人API服务

## 项目简介

企业微信机器人API服务是一个基于Flask框架开发的Web服务，用于接收外部请求并将消息转发到企业微信机器人。

## 功能特性

- 支持JSON和Form-Data两种请求格式
- 提供健康检查接口
- 完善的日志记录
- 支持中文响应
- 简单易用的API接口

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

1. 从项目根目录的父目录运行：
   ```bash
   cd ..
   python3 -m wechat_rebot_api.app
   ```

2. 或者使用项目根目录下的命令：
   ```bash
   source venv/bin/activate && python -m wechat_rebot_api.app
   ```

3. 服务将在以下地址运行：
   - http://127.0.0.1:5000
   - http://0.0.0.0:5000

## API文档

### 接口列表

| 接口地址 | 请求方法 | 功能描述 |
|---------|---------|---------|
| / | GET | 首页，返回欢迎信息 |
| /health | GET | 健康检查接口 |
| /send-message | POST | 发送消息到企业微信机器人 |

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

**请求示例**：

1. JSON格式
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"content": "测试消息"}' http://127.0.0.1:5000/send-message
   ```

2. Form-Data格式
   ```bash
   curl -X POST -F "content=测试消息" http://127.0.0.1:5000/send-message
   ```

**响应示例**：

```json
{
  "success": true,
  "message": "消息发送成功",
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
