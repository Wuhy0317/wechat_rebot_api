import logging
import os

# 从环境变量读取企业微信机器人Webhook地址，支持多个地址用逗号分隔
WECHAT_ROBOT_URLS = [url.strip() for url in os.environ.get("WECHAT_ROBOT_URLS", "").split(",") if url.strip()]

# Flask应用配置
APP_CONFIG = {
    'JSON_AS_ASCII': False
}

# 日志配置
def setup_logging():
    """
    配置应用日志
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("wechat_robot.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
