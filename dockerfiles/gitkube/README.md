# 1.部署gitkube-cont和gitkubed
kubectl apply -y Deployment.yaml
kubectl apply -y remote.yaml
# kubectl --namespace kube-system expose deployment gitkubed --type=LoadBalancer --name=gitkubed
kubectl expose deployment gitkubed --type=NodePort --name=gitkubed --namespace=kube-system

# 2.在项目中添加remote.yaml
参考本项目的remote.yaml文件

# 3.创建sectet
kubectl create secret docker-registry regsecret \
--docker-server=https://index.docker.io/v1/ \
--docker-username='804410011' \
--docker-password='xxxxxxx' \
--docker-email='804410011@qq.com'
或者
cat ~/.docker/config.json | base64
apiVersion: v1
kind: Secret
metadata:
  name: zsf-regsecret-chinamobile
  namespace: default
data:
  .dockerconfigjson: ewoJImF1dGhzIjogewoJCSJjaGluYW1vYmlsZS5jb20iOiB7CgkJCSJhdXRoIjogIllXUnRhVzQ2U0dGeVltOXlNVEl6TkRVPSIKCQl9LAoJCSJoYXJib3IuZXhhbXBsZS5jb20iOiB7CgkJCSJhdXRoIjogIllXUnRhVzQ2U0dGeVltOXlNVEl6TkRVPSIKCQl9LAoJCSJoYXJib3IuanpoY3NwdC5vcmciOiB7CgkJCSJhdXRoIjogIllXUnRhVzQ2U0dGeVltOXlNVEl6TkRVPSIKCQl9Cgl9Cn0=
type: kubernetes.io/dockerconfigjson



# 4.初始化项目
git init
git add .
git commit -m "add project"
git remote add sampleremote ssh://default-sampleremote@10.248.205.8:36416/~/git/default-sampleremote
git push sampleremote master