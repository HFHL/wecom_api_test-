from flask import Flask, request, jsonify
import hashlib
import time
import base64
import xml.etree.ElementTree as ET
from flask_cors import CORS
from WXBizMsgCrypt import WXBizMsgCrypt  # 企业微信加解密库

# Flask 实例
app = Flask(__name__)

# 跨域
CORS(app)

# 设置企业微信的 Token 和 EncodingAESKey（需要在后台配置）
TOKEN = 'zMyNl7QcqCBxLqdqHmq'
ENCODING_AES_KEY = 'QNnZPc2uQkhE9FLvWm4VPePFSxcUM1WoFfOvI9oUH9t'
CORP_ID = 'wwd4bee266f7e0cb51'  # 可从后台获取

# 初始化 WXBizMsgCrypt 类
wxcpt = WXBizMsgCrypt(TOKEN, ENCODING_AES_KEY, CORP_ID)

@app.route('/wx', methods=['GET'])
def verify():
    signature = request.args.get('msg_signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    
    # 验证消息签名
    ret, sEchoStr = wxcpt.VerifyURL(signature, timestamp, nonce, echostr)
    if ret != 0:
        return f"Error: VerifyURL ret: {ret}", 400
    
    return sEchoStr  # 返回解密后的原文

@app.route('/wx', methods=['POST'])
def receive_message():
    signature = request.args.get('msg_signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    
    # 获取 XML 内容
    xml_data = request.data
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()

    # 获取加密的消息
    encrypted_msg = root.find('Encrypt').text

    # 解密消息
    ret, decrypted_msg = wxcpt.DecryptMsg(encrypted_msg, signature, timestamp, nonce)
    if ret != 0:
        return f"Error: DecryptMsg ret: {ret}", 400
    
    # 打印解密后的消息内容（可以根据业务逻辑处理它）
    print(f"Received message: {decrypted_msg}")

    # 假设我们收到的消息需要回复
    response_msg = f"Received and decrypted message: {decrypted_msg}"
    
    # 对响应消息进行加密
    ret, encrypted_response = wxcpt.EncryptMsg(response_msg, nonce, timestamp)
    if ret != 0:
        return f"Error: EncryptMsg ret: {ret}", 400
    
    # 构造返回的 XML
    response_xml = f'''
    <xml>
        <Encrypt><![CDATA[{encrypted_response}]]></Encrypt>
        <MsgSignature><![CDATA[{signature}]]></MsgSignature>
        <TimeStamp>{timestamp}</TimeStamp>
        <Nonce><![CDATA[{nonce}]]></Nonce>
    </xml>
    '''
    
    return response_xml

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)