import requests
from .config import WECHAT_ROBOT_URLS


def send_to_wechat_robot(content, logger=None, extra_urls="", only_use_extra_urls=False):
    """
    发送消息到企业微信机器人
    
    Args:
        content: 要发送的消息内容
        logger: 日志记录器实例
        extra_urls: 额外的机器人地址，用逗号分隔
        only_use_extra_urls: 是否仅使用额外的机器人地址，跳过环境变量中的地址
    
    Returns:
        tuple: (是否成功, 消息)
    """
    if not content:
        if logger:
            logger.error("消息内容不能为空")
        return False, "消息内容不能为空"
    
    # 解析额外的机器人地址
    parsed_extra_urls = [url.strip() for url in extra_urls.split(",") if url.strip()]
    
    # 根据only_use_extra_urls参数决定使用哪些地址
    if only_use_extra_urls:
        # 仅使用额外的机器人地址
        all_urls = parsed_extra_urls
        if not all_urls:
            if logger:
                logger.error("仅使用额外机器人地址时，必须在请求中提供webhook_urls参数")
            return False, "仅使用额外机器人地址时，必须在请求中提供webhook_urls参数"
    else:
        # 合并所有机器人地址
        all_urls = WECHAT_ROBOT_URLS + parsed_extra_urls
        if not all_urls:
            if logger:
                logger.error("企业微信机器人URL未配置，请设置WECHAT_ROBOT_URLS环境变量或在请求中提供webhook_urls参数")
            return False, "企业微信机器人URL未配置，请设置WECHAT_ROBOT_URLS环境变量或在请求中提供webhook_urls参数"

    # 构造企业微信机器人消息格式
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }

    success_count = 0
    error_messages = []

    for url in all_urls:
        try:
            response = requests.post(
                url,
                json=data,
                timeout=10
            )
            response.raise_for_status()  # 抛出HTTP错误

            result = response.json()
            if result.get("errcode") == 0:
                if logger:
                    logger.info(f"消息发送成功到 {url}: {content}")
                success_count += 1
            else:
                error_msg = f"消息发送失败到 {url}: {result.get('errmsg', '未知错误')}"
                if logger:
                    logger.error(error_msg)
                error_messages.append(error_msg)

        except requests.exceptions.RequestException as e:
            error_msg = f"发送请求到 {url} 时发生错误: {str(e)}"
            if logger:
                logger.error(error_msg)
            error_messages.append(error_msg)

    # 处理结果
    if success_count == len(all_urls):
        return True, f"消息发送成功，共发送到 {success_count} 个机器人"
    elif success_count > 0:
        return False, f"部分消息发送成功，成功 {success_count} 个，失败 {len(error_messages)} 个。错误信息: {'; '.join(error_messages)}"
    else:
        return False, f"所有消息发送失败。错误信息: {'; '.join(error_messages)}"
