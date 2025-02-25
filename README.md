# DockerfileBuilder 项目

DockerfileBuilder 是一个用于自动化构建多架构 Docker 镜像并部署到远程服务器的工具。它支持以下功能：

- 自动构建支持多种架构（如 amd64、arm64）的 Docker 镜像
- 将构建好的镜像推送到私有镜像仓库
- 自动部署镜像到远程服务器

## 项目配置

### 1. 设置相关密钥
项目 --> Settings --> secrets and variables --> Actions --> secrets --> new Repository secrets 

#### 要推送到的仓库配置
secrets.ALIYUN_REGISTRY
secrets.ALIYUN_NAME_SPACE  
secrets.ALIYUN_REGISTRY_USER
secrets.ALIYUN_REGISTRY_PASSWORD

#### 远程主机配置
secrets.DEPLOY_HOST
secrets.DEPLOY_USER
secrets.PASS

![image](https://github.com/user-attachments/assets/e8794d15-2edc-492d-888c-4339cab3207d)

### 2. 配置构建平台
编辑 platforms 文件，指定要构建的镜像架构：
```bash
vi dockerfile_build/platforms
linux/amd64
linux/arm64
```

### 3. 配置部署脚本
编辑 deploy.sh 文件，配置远程部署相关参数：
```bash
vi deploy.sh
```

## 使用方法

1. 将 Dockerfile 文件放入项目目录
2. 配置 platforms 文件指定要构建的架构
3. 提交代码到 master 分支，提交信息格式为 `xxx:xxx`
4. 项目会自动构建镜像并推送到配置的私有仓库
5. 镜像构建完成后会自动部署到配置的远程服务器

## 示例

以下是一个典型的使用流程：

1. 在项目根目录创建 Dockerfile
2. 配置 platforms 文件：
   ```
   linux/amd64
   linux/arm64
   ```
3. 提交代码：
   ```bash
   git add .
   git commit -m "filesystem:v1"
   git push origin master
   ```
4. 等待构建和部署完成

## 注意事项

1. 确保正确配置所有 secrets
2. platforms 文件中的架构名称必须正确
3. 提交信息必须符合 `xxx:xxx` 格式
4. 部署服务器必须能够访问配置的私有镜像仓库

## 工作流引用

项目使用了以下 GitHub Action：
- [cross-the-world/ssh-scp-ssh-pipelines@latest](https://github.com/cross-the-world/ssh-scp-ssh-pipelines)
