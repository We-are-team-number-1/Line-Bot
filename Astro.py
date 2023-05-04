import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

all_astros = {"牡羊座": 0, "金牛座": 1, "雙子座": 2, "巨蟹座": 3, "獅子座": 4, "處女座": 5, "天秤座": 6, "天蠍座": 7, "射手座": 8, "魔羯座": 9, "水瓶座": 10, "雙魚座": 11
              }


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
            # 子標題
            overall = soup.find("span", {"class": "txt_green"}).text.strip()
            love = soup.find("span", {"class": "txt_pink"}).text.strip()
            career = soup.find("span", {"class": "txt_blue"}).text.strip()
            finance = soup.find("span", {"class": "txt_orange"}).text.strip()
            # 子標題內容
            all_content = soup.find(
                "div", {"class": "TODAY_CONTENT"})
            all_p = all_content.find_all('p')

            overall_content = all_p[1].text
            love_content = all_p[3].text
            career_content = all_p[-3].text
            finance_content = all_p[-1].text

        # 明日
        elif time_selection == "明日":
            tomorrow = (datetime.now() + timedelta(days=1)
                        ).strftime("%Y-%m-%d")
            url = f"https://astro.click108.com.tw/daily_{astro_id}.php?iAcDay={tomorrow}&iAstro={astro_id}&iType=4"

            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            overall = soup.find("span", {"class": "txt_green"}).text.strip()
            love = soup.find("span", {"class": "txt_pink"}).text.strip()
            career = soup.find("span", {"class": "txt_blue"}).text.strip()
            finance = soup.find("span", {"class": "txt_orange"}).text.strip()
            # 子標題內容
            all_content = soup.find(
                "div", {"class": "TODAY_CONTENT"})
            all_p = all_content.find_all('p')

            overall_content = all_p[1].text
            love_content = all_p[3].text
            career_content = all_p[-3].text
            finance_content = all_p[-1].text

        # 本周
        elif time_selection == "本周":
            url = f"https://astro.click108.com.tw/weekly_{astro_id}.php?iAcDay={today}&iAstro={astro_id}&iType=1"

            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            overall = soup.find("span", {"class": "txt_green"}).text.strip()
            love = soup.find("span", {"class": "txt_pink"}).text.strip()
            career = soup.find("span", {"class": "txt_blue"}).text.strip()
            finance = soup.find("span", {"class": "txt_orange"}).text.strip()
            # 子標題內容
            all_content = soup.find(
                "div", {"class": "TODAY_CONTENT"})
            all_p = all_content.find_all('p')

            overall_content = all_p[1].text
            love_content = all_p[3].text
            career_content = all_p[-3].text
            finance_content = all_p[-1].text

        # 本月
        elif time_selection == "本月":
            url = f"https://astro.click108.com.tw/monthly_{astro_id}.php?iAcDay={today}&iAstro={astro_id}&iType=2"

            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            overall = soup.find("span", {"class": "txt_green"}).text.strip()
            love = soup.find("span", {"class": "txt_pink"}).text.strip()
            career = soup.find("span", {"class": "txt_blue"}).text.strip()
            finance = soup.find("span", {"class": "txt_orange"}).text.strip()
            # 子標題內容
            all_content = soup.find(
                "div", {"class": "TODAY_CONTENT"})
            all_p = all_content.find_all('p')
            overall_content = all_p[1].text
            love_tmp = all_p[4:6]
            love_content = ''
            for p in love_tmp:
                print(p.text)
                love_content += p.text + '\n'
            career_tmp = all_p[-4:-2]
            career_content = ''
            for i in career_tmp:
                print(i.text)
                career_content += i.text + '\n'
            finance_content = all_p[-1].text

    # reply_message += f"{reply_content}"

    # message = {
    #     "type": "text",
    #     "text": reply_message
    # }

    message = {
        "type": "flex",
        "altText": "星座運勢結果",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": reply_message,
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": overall,
                                "size": "md",
                                "color": "#CC7DE6",
                                "weight": "bold",
                                "margin": "md",
                                "flex": 0,
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": overall_content,
                                "size": "sm",
                                "color": "#3B3B3B",
                                "margin": "md",
                                "flex": 0,
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": love,
                                "size": "md",
                                "color": "#CC7DE6",
                                "weight": "bold",
                                "margin": "md",
                                "flex": 0,
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": love_content.rstrip('\n'),
                                "size": "sm",
                                "color": "#3B3B3B",
                                "margin": "md",
                                "flex": 0,
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": career,
                                "size": "md",
                                "color": "#CC7DE6",
                                "weight": "bold",
                                "margin": "md",
                                "flex": 0,
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": career_content.rstrip('\n'),
                                "size": "sm",
                                "color": "#262626",
                                "margin": "md",
                                "flex": 0,
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": finance,
                                "size": "md",
                                "color": "#CC7DE6",
                                "weight": "bold",
                                "margin": "md",
                                "flex": 0,
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": finance_content,
                                "size": "sm",
                                "color": "#262626",
                                "margin": "md",
                                "flex": 0,
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "資料來源：科技紫微網",
                                "size": "sm",
                                "color": "#999999",
                                "margin": "md",
                                "flex": 0,
                                "wrap": True
                            }
                        ]
                    },

                ]
            }
        }
    }
    return message
