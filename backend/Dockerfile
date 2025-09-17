# 后端Dockerfile
FROM python:3.11

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 替换为国内源
RUN mkdir -p ~/.pip \
    && echo "[global]" > ~/.pip/pip.conf \
    && echo "index-url=https://mirrors.aliyun.com/pypi/simple" >> ~/.pip/pip.conf \
    && echo "trusted-host=mirrors.aliyun.com" >> ~/.pip/pip.conf


# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY . .

# 自动创建环境变量文件（如果不存在）
RUN if [ ! -f .env ]; then \
        if [ -f .env.example ]; then \
            cp .env.example .env; \
            echo "✅ 已自动创建 .env 文件"; \
        else \
            echo "⚠️  .env.example 文件不存在"; \
        fi; \
    else \
        echo "ℹ️  .env 文件已存在，跳过复制"; \
    fi

# 执行数据库迁移
RUN python manage.py migrate


# 创建必要的目录
RUN mkdir -p /app/logs /app/media /app/static

# 设置环境变量
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=mysite.settings

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 9001

# 添加健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:9001/api/health/ || exit 1

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:9001", "--workers", "4", "--timeout", "120", "mysite.wsgi:application"]