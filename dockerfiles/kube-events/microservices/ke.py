import time
import requests
from kubernetes import client, config, watch
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import socks
from requests.exceptions import ProxyError
from retrying import retry
from urllib.parse import urlparse



env_vars = os.environ
value = env_vars.get('HTTP_PROXY')

parsed_url = urlparse(value)

# 提取出账号和密码
username = parsed_url.username
password = parsed_url.password

# 提取出代理地址和端口
proxy_address = parsed_url.hostname
proxy_port = parsed_url.port


# 配置Kubernetes集群访问
#config.load_kube_config()
# 内部pod sa访问
config.load_incluster_config()

# 创建Kubernetes API客户端
v1 = client.CoreV1Api()

# OpenAI API密钥和URL
openai_api_key = os.environ.get('openai_api_key')
openai_url = "https://api.openai.com/v1/chat/completions"

# 获取当前时间
now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
previous_day = now - timedelta(days=1)

# 提示词
prompt = "根据以下Kubernetes事件告警信息,说明问题出现可能的原因,给我提供排查问题的思路和命令,解决问题的思路和命令"


# 邮件接收人
recipient_emails = ["zhengshifa@139.com"]

def send_email(content, recipient_emails):
    # 邮件配置
    sender_email = '804410011@qq.com'
    sender_password = 'iglefswwwrwqbcif'
    #smtp_server = 'smtp.qq.com'
    smtp_server = '120.232.69.34'

    

    message = MIMEText(content)
    message['Subject'] = 'k8s-dev告警事件'
    message['From'] = sender_email
    message['To'] = ', '.join(recipient_emails)

    # 设置代理服务器
    socks.set_default_proxy(socks.SOCKS5, proxy_address, proxy_port, username=username, password=password)
    socks.wrap_module(smtplib)

    # 连接到SMTP服务器并发送邮件
    try:
        server = smtplib.SMTP(smtp_server)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_emails, message.as_string())
        server.quit()
        print("邮件发送成功！")
    except Exception as e:
        print("邮件发送失败：", str(e))
    finally:
        # 关闭会话
        session.close()

# 创建会话
session = requests.Session()

@retry(stop_max_attempt_number=3)  # 最多重试3次
def make_request():
    response = session.post(openai_url, json=payload, headers=headers)
    response.raise_for_status()  # 检查是否有错误
    response_json = response.json()
    choices = response_json["choices"]
    message = choices[0]["message"]
    content = message["content"]
    # 其他代码...
    response_json = response.json()
    choices = response_json["choices"]
    message = choices[0]["message"]
    content = message["content"]
    # 打开文件并写入返回结果
    with open("output.txt", "w") as f:
        print("", file=f)
        print(f"命名空间: {namespace}", file=f)
        print(f"资源名字: {resource_name}", file=f)
        print(f"事件kind: {event_kind}", file=f)
        print(f"告警原因: {reason}", file=f)
        print(f"详细消息: {event_message}", file=f)
        print(f"首发时间: {event_first_timestamp}", file=f)
        print(f"来源组件: {event_source_component}", file=f)
        print("", file=f)
        print(content, file=f)
        print("", file=f)
    with open("output.txt", "r") as f:
        mail_content = f.read()
    send_email(mail_content, recipient_emails)
    # 输出保存成功的消息
    print("Response saved to file successfully.")

# 监听Kubernetes集群事件
w = watch.Watch()
for event in w.stream(v1.list_event_for_all_namespaces):
    namespace = event['raw_object']['metadata']['namespace']
    resource_name = event['raw_object']['involvedObject'].get('name')
    event_type = event['raw_object']['type']
    event_kind = event['raw_object']['involvedObject'].get('kind')
    reason = event['raw_object']['reason']
    event_message = event['raw_object']['message']
    event_first_timestamp = event['raw_object']['firstTimestamp']
    event_last_timestamp = event['raw_object']['lastTimestamp']
    try:
        event_source_component = event['raw_object']['source']['component']
    except KeyError:
        event_source_component = "<null>"
    
    if event_first_timestamp is not None:
        event_time = datetime.strptime(event_first_timestamp, '%Y-%m-%dT%H:%M:%SZ')
    event_info = f"namespace: {namespace},kind: {event_kind} ,resource_name: {resource_name}, reason: {reason}, event_message:{event_message}, event_source: {event_source_component}"
    
    if event_type == 'Warning' and event_first_timestamp == event_last_timestamp and event_time > previous_day:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                          {"role": "assistant", "content": prompt},
                          {"role": "user", "content": event_info }
                        ],
            "temperature": 0.7
        }

        # 发送请求给OpenAI
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }



        
        try:
            make_request()
        except ProxyError as e:
            # 处理代理错误
            print("无法连接到代理服务器:", e)
        except Exception as e:
            # 处理其他异常
            print("发生了其他错误:", e)
        finally:
            # 关闭会话
            session.close()
            socks.set_default_proxy(None)