from flask import Flask
from flask_cors import CORS
from .config import APP_CONFIG, setup_logging
from .api import register_routes

# 设置日志
logger = setup_logging()

# 初始化Flask应用
app = Flask(__name__)

# 应用配置
app.config.update(APP_CONFIG)

# 配置JSON提供者，确保中文正确显示
app.json.ensure_ascii = False

# 注册API路由
register_routes(app)

# 启用CORS
CORS(app)

if __name__ == '__main__':
    # 生产环境中应使用适当的WSGI服务器如Gunicorn
    # 并关闭debug模式
    # 打印所有注册的路由，用于调试
    print("\n=== 已注册的路由 ===")
    for rule in app.url_map.iter_rules():
        print(f"{rule.rule} - {rule.methods}")
    print("====================\n")
    
    # 启动应用
    logger.info("启动企业微信机器人API服务...")
    app.run(host='0.0.0.0', port=5000, debug=True)


# source venv/bin/activate && python -m wechat_rebot_api.app