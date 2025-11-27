import logging

# 企业微信机器人Webhook地址
WECHAT_ROBOT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d6576147-8584-4b67-92a4-dbaaa4dcd5ea"

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
