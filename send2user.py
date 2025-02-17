import requests
import json

# 获取 access_token
def get_access_token(corp_id, corp_secret):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}"
    response = requests.get(url)
    data = response.json()
    return data.get('access_token')

# 发送消息
def send_message(access_token, user_id, message):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    
    # 构建发送的消息体
    payload = {
        "touser": user_id,  # 指定用户的 user_id
        "msgtype": "text",   # 消息类型：文本
        "agentid": 1000002,  # 应用的 agentid，需根据实际应用填写
        "text": {
            "content": message  # 消息内容
        }
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    # 打印返回的响应
    return response.json()

# 主程序
if __name__ == "__main__":
    corp_id = "wwd4bee266f7e0cb51"  # 替换为你的企业微信 CorpID
    corp_secret = "taJa37JRM8EyhTCuSafQwr9Mnn69bWPvsa1KeUglUUs"  # 替换为你的企业微信 CorpSecret
    user_id = "USER_ID"  # 替换为指定用户的 user_id
    message = "你好，这是来自企业微信的测试消息！"  # 你要发送的消息内容

    # 获取 access_token
    access_token = get_access_token(corp_id, corp_secret)
    
    if access_token:
        # 发送消息
        result = send_message(access_token, user_id, message)
        print(result)  # 打印响应结果
    else:
        print("获取 access_token 失败！")