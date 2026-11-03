# =====================================================
# 前端 Vue + Nginx 镜像（多阶段构建）
# 阶段 1：用 node 构建静态资源
# 阶段 2：nginx 提供服务
# =====================================================

# -------- 阶段 1: 构建 --------
FROM node:20-alpine AS builder

WORKDIR /app

# 接收构建参数
ARG VITE_API_BASE=/api
ENV VITE_API_BASE=$VITE_API_BASE

# 利用缓存：先复制 package.json
COPY package*.json ./
RUN npm config set registry https://registry.npmmirror.com \
    && npm install --no-audit --no-fund

# 复制源码并构建
COPY . .
RUN npm run build

# -------- 阶段 2: 运行（nginx）--------
FROM nginx:1.25-alpine

# 复制自定义 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 复制构建产物到 nginx 静态目录
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
