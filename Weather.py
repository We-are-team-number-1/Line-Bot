import requests
import json
from linebot import LineBotApi, WebhookHandler
import configparser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, MessageTemplateAction, FlexSendMessage, BubbleContainer, ImageComponent

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

#123
def get_equake():
    msg = ['找不到地震資訊', 'https://example.com/demo.jpg']            # 預設回傳的訊息
    try:
        code = 'CWB-5903F8B2-FC6A-4703-9440-01FDFD7B64B2'
        url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={code}'
        e_data = requests.get(url)                                   # 爬取地震資訊網址
        # e_data_json = e_data.json()                                  # json 格式化訊息內容
        # eq = e_data_json['records']['Earthquake']
        eq = (json.loads(e_data.text)
              )['records']['Earthquake']
        # 取出地震資訊
        i = 0
        while (i <= (len(eq))):
            if (eq[i]["ReportType"] == '地震報告'):
                it = eq[i]
                break
            i += 1
        return it

    except IndexError:
        print('you get IndexError: list index out of range')
        return 'no data'


def eq_info(it):
    info = it["EarthquakeInfo"]

    equ = {}
    equ[0] = info
    print(equ)
    return equ


def get_earth_quake():
    msg = ['找不到地震資訊']            # 預設回傳的訊息
    try:
        code = 'CWB-5903F8B2-FC6A-4703-9440-01FDFD7B64B2'
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization=CWB-5903F8B2-FC6A-4703-9440-01FDFD7B64B2'
        e_data = requests.get(url)                                   # 爬取地震資訊網址
        eq = (json.loads(e_data.text)
              )['records']['Earthquake']

        for i in eq:
            loc = i['EarthquakeInfo']['EpiCenter']['location']       # 地震地點
            val = i['EarthquakeInfo']['Magnitude']['magnitudeValue']  # 地震規模
            dep = i['EarthquakeInfo']['Depth']['value']              # 地震深度
            eq_time = i['EarthquakeInfo']['OriginTime']              # 地震時間
            img = i['ReportImageURI']                                # 地震圖
            msg = [f'{loc}，芮氏規模 {val} 級，深度 {dep} 公里，發生時間 {eq_time}。', img]
            break     # 取出第一筆資料後就 break
        return msg    # 回傳 msg
    except:
        return msg    # 如果取資料有發生錯誤，直接回傳 msg


def flx():
    line_bot_api.push_message('U4482c45b10a321dc59e8602369c3a608', FlexSendMessage(
        alt_text='各縣市天氣查詢',
        contents={

            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "請選擇想查詢的縣市",
                                "weight": "bold",
                                "size": "md",
                                "decoration": "none",
                                "align": "center",
                                "gravity": "top"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [],
                                "spacing": "xs",
                                "margin": "md"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "text": "基隆市天氣",
                                            "label": "基隆市"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"

                                    },

                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "宜蘭縣",
                                            "text": "宜蘭縣天氣"

                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary", "position": "relative",
                                        "margin": "sm"

                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "margin": "sm",
                                        "color": "#ffffff"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "臺北市",
                                            "text": "臺北市天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "新北市",
                                            "text": "新北市天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "margin": "sm",
                                        "color": "#ffffff"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "桃園市",
                                            "text": "桃園市天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "桃園縣",
                                            "text": "桃園縣天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "margin": "sm",
                                        "color": "#ffffff"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "新竹市",
                                            "text": "新竹市天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "新竹縣",
                                            "text": "新竹縣天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "margin": "sm",
                                        "color": "#ffffff"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "苗栗縣",
                                            "text": "苗栗縣天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "臺中市",
                                            "text": "臺中市天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "margin": "sm",
                                        "color": "#ffffff"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "彰化縣",
                                            "text": "彰化縣天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "南投縣",
                                            "text": "南投縣天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "margin": "sm",
                                        "color": "#ffffff"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "雲林縣",
                                            "text": "雲林縣天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "嘉義市",
                                            "text": "嘉義市天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "margin": "sm",
                                        "color": "#ffffff"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "嘉義縣",
                                            "text": "嘉義縣天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "臺南市",
                                            "text": "臺南市天氣",

                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "margin": "sm",
                                        "color": "#ffffff"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "高雄市",
                                            "text": "高雄市天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "屏東縣",
                                            "text": "屏東縣天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    }
                                ]
                            }
                        ],

                        # "background": {
                        #     "color": "#ffedbc"

                        #     #     "type": "linearGradient",
                        #     #     "angle": "0deg",
                        #     #     "endColor": "#89cff0",
                        #     #     "startColor": "#fffeec"
                        # }
                    },
                    "footer": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "margin": "none",
                                "height": "sm",
                                "style": "link",
                                "color": "#6d6c6c",
                                "gravity": "bottom",
                                "action":  {
                                    "type": "uri",
                                    "label": "資料來源：中央氣象局",
                                    "uri": "https://www.cwb.gov.tw/V8/C/"
                                }
                            }
                        ]
                    }
                },
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "請選擇想查詢的縣市",
                                "weight": "bold",
                                "size": "md",
                                "decoration": "none",
                                "align": "center",
                                "gravity": "top"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [],
                                "spacing": "xs",
                                "margin": "md"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "text": "花蓮縣天氣",
                                            "label": "花蓮縣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"

                                    },

                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "臺東縣",
                                            "text": "臺東縣天氣"

                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary", "position": "relative",
                                        "margin": "sm"

                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "margin": "sm",
                                        "color": "#ffffff"
                                    }
                                ]
                            },

                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "澎湖縣",
                                            "text": "澎湖縣天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "金門縣",
                                            "text": "金門縣天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "margin": "sm",
                                        "color": "#ffffff"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "message",
                                            "label": "連江縣",
                                            "text": "連江縣天氣"
                                        },
                                        "color": "#d3d3d3",
                                        "style": "secondary",
                                        "position": "relative",
                                        "margin": "sm"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "margin": "sm",
                                        "color": "#ffffff"
                                    }
                                ]
                            },

                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "separator",
                                        "margin": "sm",
                                        "color": "#ffffff"
                                    }
                                ]
                            }

                        ],

                        # "background": {
                        #     "color": "#87cefa"

                        #     #     "type": "linearGradient",
                        #     #     "angle": "0deg",
                        #     #     "endColor": "#89cff0",
                        #     #     "startColor": "#fffeec"
                        # }
                    },
                    "footer": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "margin": "none",
                                "height": "sm",
                                "style": "link",
                                "color": "#6d6c6c",
                                "gravity": "bottom",
                                "action":  {
                                    "type": "uri",
                                    "label": "資料來源：中央氣象局",
                                    "uri": "https://www.cwb.gov.tw/V8/C/"
                                }
                            }
                        ]
                    }
                }
            ]
        }

    ))


def getWeather(city):
    token = 'CWB-5903F8B2-FC6A-4703-9440-01FDFD7B64B2'
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-5903F8B2-FC6A-4703-9440-01FDFD7B64B2'
    Data = requests.get(url)
    locations = (json.loads(Data.text)
                 )['records']['location']
    # FIND CITY
    try:
        i = 0
        while (i <= (len(locations))):
            if (locations[i]["locationName"] == city):
                item = locations[i]
                break
            i += 1
        return item

    except IndexError:
        print('you get IndexError: list index out of range')
        return 'no data'


def wxx(item):
    # 天氣現象
    cityName = item["locationName"]
    weatherElement = item["weatherElement"]
    if (weatherElement[0]["elementName"] == 'Wx'):
        timeDicts = weatherElement[0]["time"]  # 依時間區段設定早晚跟明天
        Wx_morning = timeDicts[0]["parameter"]["parameterName"]
        Wx_night = timeDicts[1]["parameter"]["parameterName"]
        Wx_tomorrow = timeDicts[2]["parameter"]["parameterName"]
    wx = {}
    wx[0] = Wx_morning
    wx[1] = Wx_night
    wx[2] = Wx_tomorrow
    return wx


def ciw(item):
    cityName = item["locationName"]
    weatherElement = item["weatherElement"]

# 舒適度
    if (weatherElement[3]["elementName"] == 'CI'):
        timeDicts = weatherElement[3]["time"]  # 依時間區段設定早晚跟明天
        CI_morning = timeDicts[0]["parameter"]["parameterName"]
        CI_night = timeDicts[1]["parameter"]["parameterName"]
        CI_tomorrow = timeDicts[2]["parameter"]["parameterName"]
    ci = {}
    ci[0] = CI_morning
    ci[1] = CI_night
    ci[2] = CI_tomorrow
    return ci


def transferWeatherData(item):
    cityName = item["locationName"]
    weatherElement = item["weatherElement"]  # 取得該縣市的天氣資料

# 降雨機率
    if (weatherElement[1]["elementName"] == 'PoP'):
        timeDicts = weatherElement[1]["time"]  # 依時間區段設定早晚跟明天
        PoP_morning = int(timeDicts[0]["parameter"]["parameterName"])
        PoP_night = int(timeDicts[1]["parameter"]["parameterName"])
        PoP_tomorrow = int(timeDicts[2]["parameter"]["parameterName"])

# 低溫
    if (weatherElement[2]["elementName"] == 'MinT'):
        timeDicts = weatherElement[2]["time"]
        # 依時間區段設定早晚跟明天
        MinT_morning = timeDicts[0]["parameter"]["parameterName"]
        MinT_night = timeDicts[1]["parameter"]["parameterName"]
        MinT_tomorrow = timeDicts[2]["parameter"]["parameterName"]

# 高溫
    if (weatherElement[4]["elementName"] == 'MaxT'):
        timeDicts = weatherElement[4]["time"]  # 依時間區段設定早晚跟明天
        MaxT_morning = timeDicts[0]["parameter"]["parameterName"]
        MaxT_night = timeDicts[1]["parameter"]["parameterName"]
        MaxT_tomorrow = timeDicts[2]["parameter"]["parameterName"]

        today = timeDicts[0]["startTime"].split(
            ",")
        tomorrow = timeDicts[2]["endTime"].split(
            ",")
    if MaxT_morning > MaxT_night:
        max_t = MaxT_morning
    elif MaxT_morning < MaxT_night:
        max_t = MaxT_night
    else:
        max_t = MaxT_morning
    if MinT_morning < MinT_night:
        min_t = MinT_morning
    elif MinT_morning > MinT_night:
        min_t = MinT_night
    else:
        min_t = MinT_night

    replyMsg = {}
    replyMsg[0] = str(today[0][0:10])
    replyMsg[1] = min_t
    replyMsg[2] = max_t
    replyMsg[3] = PoP_morning
    replyMsg[4] = PoP_night
    replyMsg[5] = str(tomorrow[0][0:10])
    replyMsg[6] = MinT_tomorrow
    replyMsg[7] = MaxT_tomorrow
    replyMsg[8] = PoP_tomorrow
    replyMsg[9] = ""
    replyMsg[10] = ""
    replyMsg[11] = ""

    # replyMsg =  \
    #     str(today[0][0:10]) + min_t + max_t + PoP_morning + PoP_night + \
    #     str(tomorrow[0][0:10]) + \
    #     MinT_tomorrow + MaxT_tomorrow + PoP_tomorrow


# 低溫提醒
# notice_minT()
    minT = min([weatherElement[2]["time"][0]["parameter"]["parameterName"], weatherElement[2]["time"]
                [1]["parameter"]["parameterName"], weatherElement[2]["time"][2]["parameter"]["parameterName"]])
# 高溫提醒
    maxT = max([weatherElement[4]["time"][0]["parameter"]["parameterName"], weatherElement[4]["time"]
                [1]["parameter"]["parameterName"], weatherElement[4]["time"][2]["parameter"]["parameterName"]])
    pop = max([weatherElement[1]["time"][0]["parameter"]["parameterName"], weatherElement[1]["time"]
               [1]["parameter"]["parameterName"], weatherElement[1]["time"][2]["parameter"]["parameterName"]])

    if (int(min_t) < 13):
        replyMsg[9] = "請注意低溫\n"
        return (replyMsg)

    elif (int(max_t) > 36):
        replyMsg[10] = "請注意高溫\n"
        return (replyMsg)

    elif (int(pop) > 42):  # 降雨提醒 pop=12h/ pop6=6h
        replyMsg[11] = "請攜待雨具\n"
        return (replyMsg)

    else:
        return replyMsg


def Confirm_Template():
    message = {
        "type": "template",
        "altText": "confirm template",
        "template": {
            "type": "confirm",
            "text": "想查甚麼時候的天氣呢?",
            "actions": [
                {
                    "type": "message",
                    "label": "今日天氣",
                    "text": "今日天氣"
                },
                {
                    "type": "message",
                    "label": "明日天氣",
                    "text": "明日天氣"
                }

            ]
        }
    }

    btn = {
        "type": "template",
        "altText": "This is a buttons template",
        "template": {
            "type": "buttons",
            "thumbnailImageUrl": "https://example.com/bot/images/image.jpg",
            "imageAspectRatio": "rectangle",
            "imageSize": "cover",
            "imageBackgroundColor": "#FFFFFF",
            "title": "Menu",
            "text": "Please select",
            "defaultAction": {
                "type": "uri",
                "label": "View detail",
                "uri": "http://example.com/page/123"
            },
            "actions": [
                {
                    "type": "postback",
                    "label": "Buy",
                    "data": "action=buy&itemid=123"
                },
                {
                    "type": "postback",
                    "label": "Add to cart",
                    "data": "action=add&itemid=123"
                },
                {
                    "type": "uri",
                    "label": "View detail",
                    "uri": "http://example.com/page/123"
                }
            ]
        }
    }
    return btn
    # return message
