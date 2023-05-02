import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

all_astros = {"牡羊座": 0, "金牛座": 1, "雙子座": 2, "巨蟹座": 3, "獅子座": 4, "處女座": 5, "天秤座": 6, "天蠍座": 7, "射手座": 8, "魔羯座": 9, "水瓶座": 10, "雙魚座": 11
              }


## 測試

# 這裡是測試
# 今天5/2整合測試

# 我的測試
# test0246

def reply_astros_table():
    with open("./json/1. astros_list.json", 'r', encoding='utf-8') as f:
        message = json.load(f)

    return message


def reply_time_selecter():
    with open("./json/2. time_selector.json", 'r', encoding='utf-8') as f:
        message = json.load(f)

    return message


def reply_result_message():
    with open("./json/Astro_data.json") as f:
        json_data = json.load(f)
    iuput_data = json_data

    if iuput_data["selected_astro"] in all_astros:
        your_astro = iuput_data["selected_astro"]
        time_selection = iuput_data["selected_time"]
        astro_id = all_astros[your_astro]
        today = datetime.now().strftime("%Y-%m-%d")
        reply_content = ''
        reply_message = f"【{time_selection}{your_astro}運勢】\n"

        # 今日
        if time_selection == "今日":
            url = f"https://astro.click108.com.tw/daily_{astro_id}.php?iAcDay={today}&iAstro={astro_id}&iType=0"

            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            all_content = soup.find(
                "div", {"class": "TODAY_CONTENT"})
            for p in all_content.find_all('p'):
                reply_content += p.text.strip() + '\n'
            reply_content = reply_content.rstrip('\n')

        # 明日
        elif time_selection == "明日":
            tomorrow = (datetime.now() + timedelta(days=1)
                        ).strftime("%Y-%m-%d")
            url = f"https://astro.click108.com.tw/daily_{astro_id}.php?iAcDay={tomorrow}&iAstro={astro_id}&iType=4"

            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            all_content = soup.find(
                "div", {"class": "TODAY_CONTENT"})
            for p in all_content.find_all('p'):
                reply_content += p.text.strip() + '\n'
            reply_content = reply_content.rstrip('\n')

        # 本周
        elif time_selection == "本周":
            url = f"https://astro.click108.com.tw/weekly_{astro_id}.php?iAcDay={today}&iAstro={astro_id}&iType=1"

            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            all_content = soup.find(
                "div", {"class": "TODAY_CONTENT"})
            for p in all_content.find_all('p'):
                reply_content += p.text.strip() + '\n'
            reply_content = reply_content.rstrip('\n')

        # 本月
        elif time_selection == "本月":
            url = f"https://astro.click108.com.tw/monthly_{astro_id}.php?iAcDay={today}&iAstro={astro_id}&iType=2"

            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            all_content = soup.find(
                "div", {"class": "TODAY_CONTENT"})
            for p in all_content.find_all('p'):
                reply_content += p.text.strip() + '\n'
            reply_content = reply_content.rstrip('\n')

    reply_message += f"{reply_content}"

    message = {
        "type": "text",
        "text": reply_message
    }

    # message = {
    #     "type": "flex",
    #     "altText": "星座運勢結果",
    #     "contents": {
    #         "type": "bubble",
    #         "body": {
    #             "type": "box",
    #             "layout": "vertical",
    #             "contents": [
    #                 {
    #                     "type": "text",
    #                     "text": title,
    #                     "weight": "bold",
    #                     "size": "xl"
    #                 },
    #                 {
    #                     "type": "box",
    #                     "layout": "baseline",
    #                     "margin": "md",
    #                     "contents": [
    #                         {
    #                             "type": "text",
    #                             "text": reply_content,
    #                             "size": "sm",
    #                             "color": "#999999",
    #                             "margin": "md",
    #                             "flex": 0
    #                         }
    #                     ]
    #                 },
    #                 {
    #                     "type": "box",
    #                     "layout": "vertical",
    #                     "margin": "lg",
    #                     "spacing": "sm",
    #                     "contents": [
    #                         {
    #                             "type": "box",
    #                             "layout": "baseline",
    #                             "spacing": "sm",
    #                             "contents": [
    #                                 {
    #                                     "type": "text",
    #                                     "text": "Place",
    #                                     "color": "#aaaaaa",
    #                                     "size": "sm",
    #                                     "flex": 1
    #                                 },

    #                             ]
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     }
    # }


# message = {
#     "type": "flex",
#     "altText": "星座運勢結果",
#     "contents": {
#         "type": "bubble",
#         "body": {
#             "type": "box",
#             "layout": "baseline",
#             "contents": [
#                 {
#                     "type": "text",
#                     'text': reply_message
#                 },
#                 {
#                     "type": "box",
#                     "layout": "horizontal",
#                     "contents": [
#                         {
#                             "type": "text",
#                             "text": reply_content,
#                         }
#                     ]
#                 }
#             ]
#         }
#     }
# }
    return message
