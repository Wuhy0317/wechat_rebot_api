import requests
from .config import WECHAT_ROBOT_URL


def send_to_wechat_robot(content, logger=None):
    """
    发送消息到企业微信机器人
    
    Args:
        content: 要发送的消息内容
        logger: 日志记录器实例
    
    Returns:
        tuple: (是否成功, 消息)
    """
    if not content:
        if logger:
            logger.error("消息内容不能为空")
        return False, "消息内容不能为空"

    # 构造企业微信机器人消息格式
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }

    try:
        response = requests.post(
            WECHAT_ROBOT_URL,
            json=data,
            timeout=10
        )
        response.raise_for_status()  # 抛出HTTP错误

        result = response.json()
        if result.get("errcode") == 0:
            if logger:
                logger.info(f"消息发送成功: {content}")
            return True, "消息发送成功"
        else:
            error_msg = f"消息发送失败: {result.get('errmsg', '未知错误')}"
            if logger:
                logger.error(error_msg)
            return False, error_msg

    except requests.exceptions.RequestException as e:
        error_msg = f"发送请求时发生错误: {str(e)}"
        if logger:
            logger.error(error_msg)
        return False, error_msg
