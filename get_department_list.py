import requests
import json

# 获取 access_token
def get_access_token(corp_id, corp_secret):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}"
    response = requests.get(url)
    data = response.json()
    if data.get("errcode") != 0:
        print(f"获取 access_token 失败，错误代码: {data.get('errcode')}, 错误信息: {data.get('errmsg')}")
    return data.get('access_token')

# 获取部门列表
def get_department_list(access_token):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/department/simplelist?access_token={access_token}"
    
    response = requests.get(url)
    return response.json()

# 主程序
if __name__ == "__main__":
    corp_id = "wwd4bee266f7e0cb51"  # 替换为你的企业微信 CorpID
    corp_secret = "taJa37JRM8EyhTCuSafQwr9Mnn69bWPvsa1KeUglUUs"  # 替换为你的企业微信 CorpSecret

    # 获取 access_token
    # 获取 access_token
    access_token = get_access_token(corp_id, corp_secret)
    if access_token:
        print(f"获取的 access_token: {access_token}")
    
    if access_token:
        # 获取部门列表
        department_data = get_department_list(access_token)
        
        if department_data.get("errcode") == 0:
            print("部门信息：")
            for department in department_data.get("department", []):
                print(f"部门名称: {department['name']}, 部门ID: {department['id']}")
        else:
            print(f"获取部门信息失败，错误代码: {department_data.get('errcode')}")
    else:
        print("获取 access_token 失败！")