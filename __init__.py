"""
企业微信机器人API包
用于处理外部请求并转发消息到企业微信机器人
"""

__version__ = "1.0.0"

# 导出主要组件，方便外部导入
from .app import app
from .wechat_service import send_to_wechat_robot

__all__ = ["app", "send_to_wechat_robot"]
