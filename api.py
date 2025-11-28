from flask import Blueprint, request, jsonify
import logging
from datetime import datetime
from .wechat_service import send_to_wechat_robot

# 创建蓝图
api_bp = Blueprint('api', __name__)


@api_bp.route('/send-message', methods=['POST'])
def receive_and_forward():
    """
    接收外部信息并转发到企业微信机器人
    支持两种格式: form-data和json
    """
    try:
        # 获取logger
        logger = logging.getLogger(__name__)
        
        # 尝试获取JSON数据
        json_data = request.get_json()
        if json_data and "content" in json_data:
            content = json_data["content"]
            # 从JSON获取额外的机器人地址
            extra_urls = json_data.get("webhook_urls", "")
            # 从JSON获取是否仅使用额外地址
            only_use_extra_urls = json_data.get("only_use_extra_urls", False)
        else:
            # 尝试获取表单数据
            content = request.form.get("content")
            # 从表单获取额外的机器人地址
            extra_urls = request.form.get("webhook_urls", "")
            # 从表单获取是否仅使用额外地址
            only_use_extra_urls = request.form.get("only_use_extra_urls", "false").lower() == "true"

        if not content:
            response = jsonify({
            "success": False,
            "message": "看不懂，重发！"
        })
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return response, 400

        # 转发到企业微信机器人
        success, message = send_to_wechat_robot(content, logger, extra_urls, only_use_extra_urls)

        response = jsonify({
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 200

    except Exception as e:
        error_msg = f"处理请求时发生错误: {str(e)}"
        logger = logging.getLogger(__name__)
        logger.error(error_msg)
        response = jsonify({
            "success": False,
            "message": error_msg
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    response = jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 200


@api_bp.route('/', methods=['GET'])
def index():
    """首页"""
    response = jsonify({
        "message": "欢迎使用企业微信机器人接口"
    })
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 200


def register_routes(app):
    """
    注册API路由到Flask应用
    
    Args:
        app: Flask应用实例
    """
    app.register_blueprint(api_bp)
