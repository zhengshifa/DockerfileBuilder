# 设置相关密钥
项目 --> Settings --> secrets and variables --> Actions --> secrets --> new Repository secrets 
## 要推送到的仓库配置
secrets.ALIYUN_REGISTRY
secrets.ALIYUN_NAME_SPACE
secrets.ALIYUN_REGISTRY_USER
secrets.ALIYUN_REGISTRY_PASSWORD
## 远程主机配置
secrets.DEPLOY_HOST
secrets.DEPLOY_USER
secrets.PASS
![image](https://github.com/user-attachments/assets/e8794d15-2edc-492d-888c-4339cab3207d)


# 可以自动构建多平面镜像并推送到私有仓库
vi dockerfile_build/platforms
linux/amd64
linux/arm64


# 可进行远程服务器拉取到镜像,并进行相关的部署工作
vi deploy.sh


# 工作流引用下列uses
## ssh scp ssh pipelines
[cross-the-world/ssh-scp-ssh-pipelines@latest](https://github.com/cross-the-world/ssh-scp-ssh-pipelines)
