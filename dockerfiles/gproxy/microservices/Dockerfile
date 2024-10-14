# 使用基础镜像
FROM alpine:latest

# 安装gost代理
RUN apk --no-cache add curl \
    && curl -L -o gost-linux-amd64-2.11.5.gz  https://github.com/ginuerzh/gost/releases/download/v2.11.5/gost-linux-amd64-2.11.5.gz \
    && gunzip gost-linux-amd64-2.11.5.gz && mv gost-linux-amd64-2.11.5 /usr/bin/gost  && chmod +x /usr/bin/gost

# 复制启动脚本到容器
COPY start.sh /start.sh
RUN chmod +x /start.sh

# 运行启动脚本
CMD ["/start.sh"]