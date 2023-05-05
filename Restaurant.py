import requests
import random
import datetime

GOOGLE_API_KEY = 'AIzaSyCh99R3Y1hnPZ-oP2dxqrnfZgGiZuRuVf0'


def Restaurant(latitude, longitude):
    # 獲取使用者的經緯度

    # 使用 Google API Start =========
    # 1. 搜尋附近餐廳
    nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=restaurant&fields=name,business_status,vicinity,opening_hours&language=zh-TW".format(
        GOOGLE_API_KEY, latitude, longitude)
    # nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=restaurant&language=zh-TW".format(
    #     GOOGLE_API_KEY, latitude, longitude)

    nearby_results = requests.get(nearby_url)
    # print(nearby_url)
    # print(f"result : {nearby_results.text}")

    # 2. 得到最近的20間餐廳
    nearby_restaurants_dict = nearby_results.json()
    top20_restaurants = nearby_restaurants_dict["results"]
    # print(f"result : {top20_restaurants}")

    # CUSTOMe choose rate >= 4
    res_num = (len(top20_restaurants))  # 20
    above4 = []
    restaurant = []
    for i in range(res_num):
        try:
            if (top20_restaurants[i]['rating'] > 3.9) and (top20_restaurants[i]['business_status'] == 'OPERATIONAL'):
                print('rate: ', top20_restaurants[i]['rating'])
                above4.append(i)
                restaurant.append(top20_restaurants[i])
        except KeyError:
            pass

    if len(above4) == 0:
        print('附近沒有4星以上餐廳')
    # print(above4)
    # print(f"restaurant :{restaurant}")
    # 3. 隨機選擇一間餐廳

    restaurant5 = random.sample(restaurant, 3)

    # print(f"restaurant5 :{restaurant5}")

    # print(len(restaurant5))
    # 4. 檢查餐廳有沒有照片，有的話會顯示
    map_url = []
    thumbnail_image_url = []
    details = []
    phone_number = []
    today = datetime.datetime.today().weekday()
    # details_restaurants = []
    for i in range(len(restaurant5)):
        if restaurant5[i]["photos"] is None:
            thumbnail_image_url[i] = None
        else:
            #     # 根據文件，最多只會有一張照片
            photo_reference = restaurant5[i]["photos"][0]["photo_reference"]
            thumbnail_image_url.append("https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth=1024".format(
                GOOGLE_API_KEY, photo_reference))
        # print(thumbnail_image_url)
        # 5. 組裝餐廳詳細資訊

        details_url = "https://maps.googleapis.com/maps/api/place/details/json?key={}&placeid={place_id}&language=zh-TW".format(
            GOOGLE_API_KEY, place_id=restaurant5[i]["place_id"])
        details_results = requests.get(details_url)
        details_dict = details_results.json()
        # details_restaurants = details_dict["result"]
        phone_number.append(details_dict["result"]["formatted_phone_number"].replace(
            " ", ""))

        # print(details_restaurants)
        # print(phone_number)

        if restaurant5[i]["rating"] is None:
            rating = "無"
        else:
            rating = restaurant5[i]["rating"]
        
        if restaurant5[i]["vicinity"] is None:
            address = "沒有資料"
        else:
            address = restaurant5[i]["vicinity"]

        if "weekday_text" in details_dict["result"]["opening_hours"]:
            today_open_hours = details_dict["result"]["opening_hours"]["weekday_text"][today]
            today_open_hours = today_open_hours.split(
                ": ")[1]
            opening_time = today_open_hours.split(" - ")[0]
            opening_hours = opening_time

        details.append("評分：{}星\n地址：{}\n營業時間:{}".format(
            rating, address,  opening_hours))

    # 6. 取得餐廳的 Google map 網址

        map_url.append("https://www.google.com/maps/search/?api=1&query={lat},{long}&query_place_id={place_id}".format(
            lat=restaurant5[i]["geometry"]["location"]["lat"],
            long=restaurant5[i]["geometry"]["location"]["lng"],
            place_id=restaurant5[i]["place_id"]
        ))
    # print(map_url)

    ############ 整理資料##########

    message = {
        "type": "template",
        "altText": "this is a carousel template",
        "template": {
            "type": "carousel",
            "imageAspectRatio": "rectangle",
            "imageSize": "cover",
            "columns": [
                {
                    "thumbnailImageUrl": thumbnail_image_url[0],
                    "imageBackgroundColor": "#FFFFFF",
                    "title": restaurant5[0]['name'][:40],
                    "text": details[0][:60],
                    "actions": [
                        {
                            "type": "uri",
                            "label": "查看地圖",
                            "uri":  map_url[0]
                        },
                        {
                            "type": "uri",
                            "label": "撥打電話",
                            "uri": "tel:{}".format(phone_number[0])
                        }

                    ]
                },
                {
                    "thumbnailImageUrl": thumbnail_image_url[1],
                    "imageBackgroundColor": "#FFFFFF",
                    "title": restaurant5[1]['name'][:40],
                    "text": details[1][:60],
                    "actions": [
                        {
                            "type": "uri",
                            "label": "查看地圖",
                            "uri":  map_url[1]
                        },
                        {
                            "type": "uri",
                            "label": "撥打電話",
                            "uri": "tel:{}".format(phone_number[1])
                        }
                    ]
                },
                {
                    "thumbnailImageUrl": thumbnail_image_url[2],
                    "imageBackgroundColor": "#FFFFFF",
                    "title": restaurant5[2]['name'][:40],
                    "text": details[2][:60],
                    "actions": [
                        {
                            "type": "uri",
                            "label": "查看地圖",
                            "uri":  map_url[2]
                        },
                        {
                            "type": "uri",
                            "label": "撥打電話",
                            "uri": "tel:{}".format(phone_number[2])
                        }
                    ]
                }

            ]

        }
    }
    return message
