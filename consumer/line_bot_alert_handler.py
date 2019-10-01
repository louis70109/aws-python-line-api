import json
import requests

from lib.decorator import lambda_warm_up
@lambda_warm_up
def alert_handler(event, context):
    air = requests.get(
        'http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json')
    air_body = json.loads(air.text)
    air_status = ["良好",	"普通",	"對敏感族群不健康",	"對所有族群不健康",	"非常不健康",	"危害", "資料有誤"]
    total, count = 0, 0
    for fetch in air_body:
        if (fetch['County'] == "臺中市" and (fetch['SiteName'] == "西屯" or fetch['SiteName'] == "沙鹿")):
            count += 1
            if fetch['AQI'] != 0:
                total = total + int(fetch['AQI'])
    switch = 0
    pm = int(total / count)
    print(pm)
    if pm in range(0, 50):
        switch = 0
    elif pm in range(51, 100):
        switch = 1
    elif pm in range(101, 150):
        switch = 2
    elif pm in range(151, 200):
        switch = 3
    elif pm in range(201, 250):
        switch = 4
    elif pm in range(251, 300):
        switch = 5
    else:
        switch = 6
    payload = f"\n空氣品質: {air_status[switch]}"
    r = requests.post('https://1uv2o723o4.execute-api.us-east-1.amazonaws.com/dev/notify/sqs',
                      data={'message': payload})
    print(r)
