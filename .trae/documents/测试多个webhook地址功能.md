# 测试多个webhook地址功能

## 测试目标

验证系统是否能正确从环境变量读取多个webhook地址，并向所有地址发送消息。

## 测试步骤

### 1. 直接在命令行中设置环境变量并运行应用

**在同一个终端会话中执行以下命令**：

```bash
# Linux/macOS
# 激活虚拟环境
source venv/bin/activate

# 设置环境变量并运行应用
WECHAT_ROBOT_URLS="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d6576147-8584-4b67-92a4-dbaaa4dcd5ea,https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4372fc3e-8aa6-4bb3-bd5e-6b815563cb3b" python3 -m wechat_rebot_api.app
```

### 2. 在另一个终端窗口中测试发送消息

**打开新的终端窗口，执行以下命令**：

```bash
# 测试发送消息
curl -X POST -H "Content-Type: application/json" -d '{"content": "测试多个地址"}' http://127.0.0.1:5000/send-message
```

### 3. 查看测试结果

**在应用运行的终端窗口中**：

* 查看日志输出，确认是否向两个地址发送了消息

* 查看每个地址的发送状态

**在测试发送消息的终端窗口中**：

* 查看返回的响应消息，确认是否显示"消息发送成功，共发送到 2 个机器人"

### 4. 测试单个webhook地址

**在同一个终端会话中执行以下命令**：

```bash
# 设置单个环境变量并运行应用
WECHAT_ROBOT_URLS="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key1" python3 -m wechat_rebot_api.app
```

**在另一个终端窗口中测试发送消息**：

```bash
curl -X POST -H "Content-Type: application/json" -d '{"content": "测试单个地址"}' http://127.0.0.1:5000/send-message
```

**预期结果**：返回"消息发送成功，共发送到 1 个机器人"

## 替代测试方法：使用Python脚本测试

创建一个简单的Python脚本，直接设置环境变量并运行应用：

```python
#!/usr/bin/env python3
import os
import subprocess

# 设置环境变量
os.environ['WECHAT_ROBOT_URLS'] = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key1,https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key2'

# 运行应用
subprocess.run(['python3', '-m', 'wechat_rebot_api.app'])
```

保存为`test_env.py`，然后执行：

```bash
python3 test_env.py
```

## 预期结果

1. 单个地址测试：返回"消息发送成功，共发送到 1 个机器人"
2. 多个地址测试：返回"消息发送成功，共发送到 2 个机器人"
3. 日志中显示每个地址的发送情况

## 注意事项

* 确保在测试前停止之前运行的应用实例

* 测试完成后，不需要清理环境变量，因为它们只在当前终端会话中有效

* 如果使用Python脚本测试，环境变量只在脚本运行期间有效

