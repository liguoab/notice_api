import re, requests, logging, sys, json
from ..main import app
from flask import Flask, jsonify, request, abort, g 
from app.config import WX_CORPID, WX_CORPSECRET


@app.route("/wx/apps/send", methods=['POST'])
def wxSend():
    data = request.get_json()

    try:
        touser=data['touser']
        agentid=data['agentid']
        content=data['content']
    except Exception as e:
        return jsonify(code=1, message='参数缺失，请检查')
    
    # 获取 access_token
    token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    token_params = {"corpid":WX_CORPID,"corpsecret":WX_CORPSECRET}
    try:
        r = requests.get(token_url, params=token_params)
        if r.status_code != 200:
            logging.info(r.text)
            return jsonify(code=1, message=r.text)
    except Exception as err:
        logging.info(err)
        return jsonify(code=1, message=err)
    # 得到 access_token
    access_token = r.json()["access_token"]
    # 发送文本消息
    send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={0}".format(access_token)
    send_params = {
       "touser" : touser, # 全员发送 @all、独立发送 name_a|name_b
       "msgtype" : "text",
       "agentid" : agentid,
       "text" : {
           "content" : content
       }
    }
    try:
        r = requests.post(send_url, json=send_params, timeout=(10,10))
        if (r.status_code !=200 or json.loads(r.text)['errcode']):
            logging.info(r.text)
            return jsonify(code=1, message=r.text)
    except Exception as err:
        logging.info(err)
        return jsonify(code=1, message=err)
    return jsonify(code=0, message=r.text)