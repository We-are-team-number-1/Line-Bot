from __future__ import unicode_literals
from urllib import parse
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from datetime import datetime
import requests
import json
import configparser
import os
import logging
import time

# import 所有功能
import THSR
import Restaurant
import Weather
import Astro

# 1.setup log path and create log directory
logName = 'MyProgram.log'
logDir = 'log'
logPath = logDir + '/' + logName

# create log directory
os.makedirs(logDir, exist_ok=True)

# 2.create logger, then setLevel
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

# 3.create file handler, then setLevel
# create file handler
fileHandler = logging.FileHandler(logPath, mode='w')
fileHandler.setLevel(logging.DEBUG)

# 4.create stram handler, then setLevel
# create stream handler
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.INFO)

# 5.create formatter, then handler setFormatter
AllFormatter = logging.Formatter(
    '[%(levelname)s][%(asctime)s][LINE:%(lineno)s][%(module)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fileHandler.setFormatter(AllFormatter)
streamHandler.setFormatter(AllFormatter)

# 6.logger addHandler
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
my_line_id = config.get('line-bot', 'my_line_id')
end_point = config.get('line-bot', 'end_point')
line_login_id = config.get('line-bot', 'line_login_id')
line_login_secret = config.get('line-bot', 'line_login_secret')
my_phone = config.get('line-bot', 'my_phone')
HEADER = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {config.get("line-bot", "channel_access_token")}'
}

# 城市 ===================================================================================================================
key_city = ['基隆市天氣', '嘉義市天氣', '臺北市天氣', '台北市天氣', '嘉義縣天氣', '新北市天氣', '臺南市天氣', '台南市天氣', '桃園市天氣', '高雄市天氣', '新竹市天氣', '屏東縣天氣', '桃園縣天氣',
            '宜蘭市天氣', '新竹縣天氣', '臺東縣天氣', '台東縣天氣', '苗栗縣天氣', '花蓮縣天氣', '臺中市天氣', '台中市天氣', '宜蘭縣天氣', '彰化縣天氣', '澎湖縣天氣', '南投縣天氣', '金門縣天氣', '雲林縣天氣', '連江縣天氣']


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return 'ok'
    body = request.json
    events = body["events"]
    if request.method == 'POST' and len(events) == 0:
        return 'ok'
    if "replyToken" in events[0]:
        payload = dict()
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
        if events[0]["type"] == "message":

            # ============ Message type : text ============
            if events[0]["message"]["type"] == "text":
                text = events[0]["message"]["text"]

                # ================== 高鐵查詢 ==================
                if text == "高鐵查詢":
                    payload["messages"] = [
                        THSR.THSR_choose_start_station()]

                # ================== 星座運勢 ==================
                elif text == "星座運勢":
                    payload["messages"] = [Astro.reply_astros_table()]

                # ================== 天氣查詢-天氣預報 ==================
                elif text == "各縣市天氣查詢":
                    payload["messages"] = [Weather.reply_weather_table(),Weather.reply_weather_table2()]

                elif text == "天氣查詢":
                    payload["messages"] = [Weather.flx()]                
                
                # ================== 餐廳查詢-提醒開啟位置 ==================
                elif text == "請傳送你的位置資訊":
                    payload["messages"] = [
                        {
                            "type": "text",
                            "text": "請按發送定位→再按公開的所在位置",
                            "quickReply": {
                                "items": [
                                    {
                                        "action": {
                                            "type": "location",
                                            "label": "位置資訊"
                                        }
                                    }
                                ]
                            }
                        }
                    ]

                # ================== 天氣查詢-雷達 ==================
                elif text in {'雷達', '雷達回波'}:
                    line_bot_api.reply_message(
                        replyToken, ImageSendMessage(original_content_url=f'https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MSC/O-A0058-003.png?{time.time_ns()}',
                                                     preview_image_url=f'https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MSC/O-A0058-003.png?{time.time_ns()}'
                                                     ))

                # ================== 天氣查詢-地震 ==================
                elif text in {'地震', '地震查詢'}:
                    u = Weather.get_eq_pic()
                    line_bot_api.reply_message(
                        replyToken, ImageSendMessage(original_content_url=u,
                                                     preview_image_url=u
                                                     ))
                # ================== 天氣查詢-顯示天氣預報 ==================
                elif text in key_city:
                    if text[0] == '台':
                        text = text.replace('台', '臺')
                    user_city = text[:3]
                    weather = Weather.getWeather(user_city)
                    wx = Weather.wxx(weather)
                    ci = Weather.ciw(weather)
                    msg_weaterInfo = Weather.transferWeatherData(weather)
                    # msg_weaterInfo[3] = 80
                    # msg_weaterInfo[8] = 100
                    if msg_weaterInfo[3] > 42:
                        url = 'https://cdn-icons-png.flaticon.com/512/622/622085.png'
                    elif 41 > msg_weaterInfo[3] & msg_weaterInfo[3] > 20:
                        url = 'https://cdn-icons-png.flaticon.com/512/2042/2042088.png'
                    else:
                        url = 'https://cdn-icons-png.flaticon.com/512/1838/1838873.png'
                    if msg_weaterInfo[8] > 42:
                        url1 = 'https://cdn-icons-png.flaticon.com/512/622/622085.png'
                    else:
                        url1 = 'https://cdn-icons-png.flaticon.com/512/1838/1838873.png'

                    line_bot_api.reply_message(
                        replyToken, TemplateSendMessage(
                            alt_text=user_city + '未來 36 小時天氣預測',
                            template=CarouselTemplate(
                                columns=[
                                    CarouselColumn(
                                        thumbnail_image_url=url,
                                        title='{}'.format(
                                            msg_weaterInfo[0]),
                                        text='天氣狀況： \t{}\n舒適度： \t{}\n溫度： \t{}°C  至 \t{}°C \n降雨機率： {}%\n{}{}{}'.format(
                                            wx[0], ci[0], msg_weaterInfo[
                                                1], msg_weaterInfo[2], msg_weaterInfo[3], msg_weaterInfo[9], msg_weaterInfo[10], msg_weaterInfo[11]
                                        ),
                                        actions=[
                                            URIAction(
                                                label='氣象局詳細內容',
                                                uri='https://www.cwb.gov.tw/V8/C/W/County/index.html'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url=url1,
                                        title='{}'.format(
                                            msg_weaterInfo[5]),
                                        text='天氣狀況： \t{}\n舒適度： \t{}\n溫度： \t{}°C  至 \t{}°C \n降雨機率： {}%'.format(
                                            wx[2], ci[2],  msg_weaterInfo[6], msg_weaterInfo[7], msg_weaterInfo[8]),

                                        actions=[
                                            URIAction(
                                                label='氣象局詳細內容',
                                                uri='https://www.cwb.gov.tw/V8/C/W/County/index.html'
                                            )
                                        ]
                                    )

                                ]
                            )


                        ))
                

                else:
                    payload["messages"] = [
                        {
                            "type": "text",
                            "text": "請打開選單 → 點選要查詢的資訊"
                        }
                    ]

                replyMessage(payload)

            # ============ Message type : location ============
            elif events[0]["message"]["type"] == "location":

                # ================== 餐廳查詢 ==================
                latitude = events[0]["message"]["latitude"]
                longitude = events[0]["message"]["longitude"]
                payload["messages"] = [
                    Restaurant.Restaurant(latitude, longitude)]
                replyMessage(payload)
                
            

        # ============ Message type : Postback ============
        elif events[0]["type"] == "postback":
            firstData = events[0]["postback"]["data"][0:2]

            # ================== 高鐵查詢 - start station ====================
            if "data" in events[0]["postback"] and firstData == "SS":
                with open("./json/THSR_station_data.json", 'r') as f:
                    json_data = json.load(f)

                chiStation = events[0]["postback"]["data"][3:6]
                engStation = events[0]["postback"]["data"][7:]
                json_data["start_station"] = engStation
                json_data["chi_start_station"] = chiStation

                # Save station data to json
                with open("./json/THSR_station_data.json", "w") as f:
                    json.dump(json_data, f)
                payload["messages"] = [THSR.THSR_choose_end_station()]

            # ================== 高鐵查詢 - end station ====================
            elif "data" in events[0]["postback"] and firstData == "ES":
                with open("./json/THSR_station_data.json", 'r') as f:
                    json_data = json.load(f)

                chiStation = events[0]["postback"]["data"][3:6]
                engStation = events[0]["postback"]["data"][7:]
                json_data["end_station"] = engStation
                json_data["chi_end_station"] = chiStation

                if json_data["end_station"] == json_data["start_station"]:
                    logger.info("error")
                    payload["messages"] = [{
                        "type": "text",
                        "text": "出發站不能等於到達站"
                    },
                        THSR.THSR_choose_end_station()]
                else:
                    # Save station data to json
                    with open("./json/THSR_station_data.json", "w") as f:
                        json.dump(json_data, f)

                    payload["messages"] = [THSR.THSR_choose_time()]

            # ================== 高鐵查詢 - choose time ====================
            elif events[0]["postback"]["data"] == "chooseTime":
                with open("./json/THSR_station_data.json", 'r') as f:
                    json_data = json.load(f)

                searchTime = events[0]["postback"]["params"]["datetime"].replace(
                    "T", " ")
                logger.info(json_data["start_station"])
                logger.info(json_data["end_station"])

                payload["messages"] = [THSR.THSR_result(searchTime)]

            # ================== 星座運勢查詢 - choose Astro ====================
            elif "data" in events[0]["postback"] and firstData == "AS":
                with open("./json/Astro_data.json", 'r') as f:
                    json_data = json.load(f)

                userAstro = events[0]["postback"]["data"][3:6]
                json_data["selected_astro"] = userAstro

                with open("./json/Astro_data.json", "w") as f:
                    json.dump(json_data, f)

                # print('=================')
                # print(payload)
                # print(json_data)
                # print(userAstro)
                # print('=================')
                payload["messages"] = [Astro.reply_time_selecter()]

            # ================== 星座運勢查詢 - choose date ====================
            elif "data" in events[0]["postback"] and firstData == "TM":
                with open("./json/Astro_data.json", 'r') as f:
                    json_data = json.load(f)

                json_data["selected_time"] = events[0]["postback"]["data"][3:5]

                with open("./json/Astro_data.json", "w") as f:
                    json.dump(json_data, f)

                # print("+"*20)
                # print("ok")
                # print(json_data)
                # print("+"*20)
                payload["messages"] = [Astro.reply_result_message()]

            replyMessage(payload)

    return 'OK'

# 有人來call這個路徑，就執行def callback


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 若有接收到MessageEvent的話，call這裡


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


@app.route("/sendTextMessageToMe", methods=['POST'])
def sendTextMessageToMe():
    pushMessage({})
    return 'OK'


def replyMessage(payload):
    response = requests.post(
        "https://api.line.me/v2/bot/message/reply", headers=HEADER, json=payload)
    logger.info(response.text)
    print(response.text)
    print('payload =', payload)
    return 'OK'


def pushMessage(payload):
    response = requests.post(
        "https://api.line.me/v2/bot/message/push", headers=HEADER, json=payload)
    print(response.text)
    return 'OK'


if __name__ == "__main__":
    app.debug = True
    app.run()
