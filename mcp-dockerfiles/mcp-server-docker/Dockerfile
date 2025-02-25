# 使用官方Python精简镜像作为基础
FROM python:3.12-slim AS builder

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

# 复制必要文件
COPY pyproject.toml README.md uv.lock ./

# 创建虚拟环境并安装依赖
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -U pip setuptools && \
    pip install --no-cache-dir . 

# 第二阶段构建：运行时镜像
FROM python:3.12-slim

# 设置工作目录和用户
WORKDIR /app
RUN useradd -m -u 1001 appuser
USER appuser

# 从builder阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制应用代码
COPY --chown=appuser:appuser src/ ./src/

# 暴露应用端口
EXPOSE 8000

# 设置启动命令
CMD ["mcp-server-docker"]