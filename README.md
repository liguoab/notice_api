
# 消息推送多平台 SDK

## About the project
整合多平台提供一个统一的消息推送入口, 该项目的主要应用场景是**告警通知**可以下发到多个平台

## Features
| 对接平台      | 接口                   | 描述                | 是否实现 |
| ------------ | ---------------------- | ------------------ | ------- |
| Email        | /email/send/message    | 邮件发送接口         | 是      |
| Slack        | /slack/send/message    | Slack 通道接口       | 是      |
| 钉钉         | /dingding/send/message  | 钉钉群消息接口       | 是      |
| 钉钉         | /dingding/call          | 钉电话（接口暂未开放）| 否      |
| 企业微信      | /wx/apps/send          | 企业微信应用消息接口   | 是      |
| SMS          | /sms/send              | 短信通知接口          | 否      |
| VMS          | /vms/send              | 语音通知接口          | 否      |

## Getting Started
#### 测试环境构建
`docker build -t myimage .`  
`docker run -d --name mycontainer -p 9091:80 -v $(pwd)/app:/app -e FLASK_APP=app/main.py -e FLASK_DEBUG=1 myimage flask run --host=0.0.0.0 --port=80`  

#### 线上环境构建 
`docker build -t myimage .`  
`docker run -d --name mycontainer -p 9091:80 myimage`  

#### 接口描述
> 通用返回码 code ：0 表示成功；1 表示失败

##### Email 下发接口 
接口地址  
/email/send/message

参数列表
| 参数    | 类型     | 必须 | 说明     |
| ------- | ------- | ---  | ------- |
| subject | string  | 是   | 邮件标题 |
| from    | string  | 是   | 发件人   |
| to      | array   | 是   | 收件人   |
| cc      | array   | 否   | 抄送人   |
| content | string  | 是   | 邮件内容 |

返回值  
成功：`{ "code": 0 }`  
失败：`{ "code": 1, "message": "xxx" }`  

##### Slack 下发接口 
接口地址  
/slack/send/message  

参数列表
| 参数    | 类型     | 必须 | 说明                    |
| ------- | ------- | ---  | ---------------------- |
| channel | string  | 是   | Channel 名称            |
| content | string  | 是   | 下发内容，markdown、text |

返回值  
成功：`{ "code": 0 }`  
失败：`{ "code": 1, "message": "xxx" }`  

##### 钉钉下发接口 
接口地址  
/dingding/send/message  

参数列表
| 参数      | 类型     | 必须 | 说明                                   |
| --------- | ------- | ---  | ------------------------------------- |
| content   | string  | 是   | 下发内容                               |
| isAtAll   | bool    | 是   | 是否群发                               |
| atMobiles | array   | 否   | 如果 isAtAll 参数是 false，该参数不能为空 |

返回值  
成功：`{ "code": 0 }`  
失败：`{ "code": 1, "message": "xxx" }`  

##### 微信下发接口 
接口地址  
/wx/apps/send  

参数列表
| 参数    | 类型     | 必须 | 说明                                           |
| ------- | ------- | ---  | --------------------------------------------- |
| touser  | string  | 是   | 指定接收人，全员：@all；指定某些人：name_a|name_b |
| agentid | string  | 是   | 发件人                                         |
| content | string  | 是   | 收件人                                         |

返回值  
成功：`{ "code": 0 }`  
失败：`{ "code": 1, "message": "{\"errcode\":81013,\"errmsg\":\"user & party & tag all invalid, hint: [1589355369_79_14baebabcb4723b8ddb56d226fc7babe],\"invaliduser\":\"test\"}" }`  
