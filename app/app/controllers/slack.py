import re
from ..main import app
from flask import Flask, jsonify, request, abort, g
import requests, logging, sys
from app.config import SLACK_WEBHOOK



@app.route("/slack/send/message")
def slackSend():
    data = request.get_json()
    try:
        channel_name=data['channel']
        content=data['content']
    except Exception as e:
        return jsonify(code=1, message="参数缺失，请检查")
    
    try:
        webhook_url=SLACK_WEBHOOK[channel_name]
    except Exception as e:
        return jsonify(code=1, message="channel 有误或不存在，请检查")
    
    send_params = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": content
                }
            }
        ]
    }
    try:
        r = requests.post(webhook_url, json=send_params, timeout=(10,10))
        if r.status_code !=200:
            logging.info(r.text)
            return jsonify(code=1, message=r.text)
    except Exception as err:
        logging.info(err)
        return jsonify(code=1, message=err)
    return jsonify(code=0, message=r.text)


if __name__ == '__main__':
    app.run()