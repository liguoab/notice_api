from flask import Flask, jsonify, request, abort, g
from ..main import app
import requests, logging, sys
import smtplib
from email.message import EmailMessage
from app.config import MAIL_HOST, MAIL_PORT, MAIL_ONSSL, MAIL_USER, MAIL_PASSWD

@app.route('/email/send/message', methods=['POST'])
def emailSend():
    data = request.get_json()
    try:
        m_subject = data['subject']
        m_from = data['from']
        m_to = data['to']
        m_content = data['content']
    except Exception as e:
        return jsonify(code=1, message='参数缺失，请检查')
    
    try:
        m_cc = data['cc']
    except Exception as e:
        m_cc = ''


    msg = EmailMessage()
    msg['Subject'] = m_subject
    msg['From'] = m_from
    msg['To'] = ','.join(str(i) for i in m_to)
    msg['Cc'] = ','.join(str(i) for i in m_cc)
    msg.set_content(m_content)
    
    if MAIL_ONSSL:
        smtp_obj = smtplib.SMTP_SSL(host=MAIL_HOST, port=MAIL_PORT)
    else:
        smtp_obj = smtplib.SMTP(host=MAIL_HOST, port=MAIL_PORT)
    smtp_obj.login(user=MAIL_USER, password=MAIL_PASSWD)
    smtp_obj.send_message(msg)
    smtp_obj.quit()
    return jsonify(code=0)
