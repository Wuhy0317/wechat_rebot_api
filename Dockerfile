# 使用官方Python镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制requirements.txt文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建包目录
RUN mkdir -p wechat_rebot_api

# 复制项目代码到包目录
COPY *.py wechat_rebot_api/

# 暴露端口
EXPOSE 5000

# 运行应用
CMD ["python", "-m", "wechat_rebot_api.app"]
