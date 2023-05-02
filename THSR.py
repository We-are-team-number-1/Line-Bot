import json
from datetime import datetime
import logging
import os
import requests

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


def THSR_choose_start_station():
    with open("./json/THSR_choose_start_station.json", 'r', encoding='utf-8') as f:
        message = json.load(f)
    return message


def THSR_choose_end_station():
    with open("./json/THSR_choose_end_station.json", 'r', encoding='utf-8') as f:
        message = json.load(f)
    return message


def THSR_choose_time():
    with open("./json/THSR_choose_time.json", 'r', encoding='utf-8') as f:
        message = json.load(f)
    now_time = datetime.now().strftime("%Y-%m-%dt%H:%M")
    message["contents"]["body"]["contents"][0]["contents"][0]["action"]["initial"] = now_time
    return message


def THSR_result(searchTime):
    # Read station data
    closest_start_time = 0
    closest_end_time = 0
    trains_list = []
    trains_duration = []
    with open("./json/THSR_station_data.json") as f:
        json_data = json.load(f)
    logger.info(json_data["start_station"])
    logger.info(json_data["end_station"])
    target_date = searchTime[:10].replace("-", "/")
    target_time = searchTime[11:]
    logger.info('Search date : ' + target_date)
    logger.info('Search time : ' + target_time)
    form_data = {
        'SearchType': 'S',
        'Lang': 'TW',
        'StartStation': json_data["start_station"],
        'EndStation': json_data["end_station"],
        'OutWardSearchDate': target_date,
        'OutWardSearchTime': target_time,
        'ReturnSearchDate': '2023/04/07',
        'ReturnSearchTime': '21:00',
        'DiscountType': ''
    }

    response = requests.post(
        'https://www.thsrc.com.tw/TimeTable/Search', data=form_data)
    response.encoding = "utf-8"
    data = json.loads(response.text)
    num_of_train = len(data['data']['DepartureTable']['TrainItem'])
    # logger.info(num_of_train)
    # logger.info(data['data']['DepartureTable']['TrainItem'])

    # Choose the time closest to the user selected departure time
    target_time = int(target_time.replace(":", ""))
    for i in range(num_of_train):
        if abs(int(data['data']['DepartureTable']['TrainItem'][i]['DepartureTime'].replace(
                ":", "")) - target_time) < abs(closest_start_time - target_time):
            closest_start_time = int(data['data']['DepartureTable']['TrainItem'][i]['DepartureTime'].replace(
                ":", ""))
            closest_end_time = int(data['data']['DepartureTable']['TrainItem'][i]['DestinationTime'].replace(
                ":", ""))
            closest_i = i

    # logger.info(closest_start_time)
    # logger.info(closest_end_time)
    # logger.info(closest_i)

    # Choose the train that matches the time and append into time_list
    # if num of train < 5, append corresponding amount of trains into time_list
    if num_of_train - closest_i < 5:
        for j in range(0, num_of_train - closest_i):
            trains_list.append([data['data']['DepartureTable']['TrainItem'][closest_i]['TrainNumber'], data['data']['DepartureTable']['TrainItem'][closest_i]['DepartureTime'].replace(
                ":", "").zfill(4)[:2] + ":" + data['data']['DepartureTable']['TrainItem'][closest_i]['DepartureTime'].replace(
                ":", "").zfill(4)[2:], data['data']['DepartureTable']['TrainItem'][closest_i]['DestinationTime'].replace(
                ":", "").zfill(4)[:2] + ":" + data['data']['DepartureTable']['TrainItem'][closest_i]['DestinationTime'].replace(
                ":", "").zfill(4)[2:], data['data']['DepartureTable']['TrainItem'][closest_i]['Duration']])

            trains_duration.append(int(
                data['data']['DepartureTable']['TrainItem'][closest_i]['Duration'].replace(":", "")))

            closest_i += 1
    # if num of train >= 5, append only five closest start time into time_list
    else:
        for j in range(0, 5):
            trains_list.append([data['data']['DepartureTable']['TrainItem'][closest_i]['TrainNumber'], data['data']['DepartureTable']['TrainItem'][closest_i]['DepartureTime'].replace(
                ":", "").zfill(4)[:2] + ":" + data['data']['DepartureTable']['TrainItem'][closest_i]['DepartureTime'].replace(
                ":", "").zfill(4)[2:], data['data']['DepartureTable']['TrainItem'][closest_i]['DestinationTime'].replace(
                ":", "").zfill(4)[:2] + ":" + data['data']['DepartureTable']['TrainItem'][closest_i]['DestinationTime'].replace(
                ":", "").zfill(4)[2:], data['data']['DepartureTable']['TrainItem'][closest_i]['Duration']])

            trains_duration.append(int(
                data['data']['DepartureTable']['TrainItem'][closest_i]['Duration'].replace(":", "")))

            closest_i += 1

    logger.info(trains_duration)
    min_duration = min(trains_duration)
    logger.info(min_duration)

    # logger.info(f"total train : {trains_list}")
    # logger.info(f"num of train : {len(trains_list)}")
    num_of_train_list = len(trains_list)
    target_time = str(target_time).zfill(4)

    # Read corresponding json carousel template according to the num of train
    with open(f"./json/THSR_result_{num_of_train_list}_data.json", 'r', encoding='utf-8') as f:
        message = json.load(f)

    message["contents"]["header"]["contents"][0]["contents"][0]["contents"][1]["text"] = target_date
    message["contents"]["header"]["contents"][0]["contents"][1]["contents"][1]["text"] = target_time[:2] + ":" + target_time[2:]
    message["contents"]["header"]["contents"][1]["contents"][0]["contents"][1]["text"] = json_data["chi_start_station"]
    message["contents"]["header"]["contents"][1]["contents"][1]["contents"][1]["text"] = json_data["chi_end_station"]

    for i in range(0, len(trains_list)):
        if min_duration == trains_duration[i]:
            message["contents"]["body"]["contents"][3*i][
                "contents"][1]["background"]["startColor"] = "#FF8000"
            message["contents"]["body"]["contents"][3*i][
                "contents"][1]["background"]["endColor"] = "#FFC78E"

        message["contents"]["body"]["contents"][3*i+1][
            "contents"][1]["contents"][1]["text"] = trains_list[i][3]
        message["contents"]["body"]["contents"][3*i][
            "contents"][0]["contents"][0]["text"] = f'車次 {trains_list[i][0]}'
        message["contents"]["body"]["contents"][3*i +
                                                1]["contents"][0]["contents"][0]["text"] = trains_list[i][1]
        message["contents"]["body"]["contents"][3*i +
                                                1]["contents"][2]["contents"][0]["text"] = trains_list[i][2]

    return message
