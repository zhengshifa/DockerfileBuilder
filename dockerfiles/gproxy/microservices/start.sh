#!/bin/sh

# 设置gost代理的参数
GOST_ARGS="/usr/bin/gost  -L=tcp://:7890/106.55.28.116:7890 -F=http://10.248.68.185:8118"
# 启动多个gost代理实例
$GOST_ARGS
# 等待所有gost代理实例退出
wait