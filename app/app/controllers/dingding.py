from flask import Flask, jsonify, request, abort, g
from ..main import app
import requests, logging, sys
from app.config import DING_BOOT_WEBHOOK

@app.route('/dingding/send/message', methods=['POST'])
def dingdingSend():
    data = request.get_json()
    send_params = {"msgtype":"text"}
    try:
        if not isinstance(data['isAtAll'], bool):
            return jsonify(code=1, message='isAtAll 不是 bool 类型，请检查')

        send_params["text"] = {"content" : data['content']}
        send_params["at"] = {"isAtAll" : data['isAtAll']}
        
        if not data['isAtAll']:
            send_params["at"] = {"atMobiles" : data['atMobiles'], "isAtAll" : data['isAtAll']}
    except Exception as e:
        return jsonify(code=1, message=e)

    try:
        r = requests.post(DING_BOOT_WEBHOOK, json=send_params, timeout=(10,10))
        if r.status_code !=200:
            logging.info(r.text)
            return jsonify(code=1, message=r.text)
    except Exception as err:
        logging.info(err)
        return jsonify(code=1, message=err)
    return jsonify(code=0)
