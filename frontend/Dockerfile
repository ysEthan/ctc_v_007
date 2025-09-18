# 前端Dockerfile
FROM node:20 AS builder

# 设置工作目录
WORKDIR /app

# 复制package文件
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制源代码
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

# 构建应用（跳过类型检查）
RUN npm run build-only

# 生产环境镜像
FROM nginx

# 安装curl用于健康检查
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 复制构建文件
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]