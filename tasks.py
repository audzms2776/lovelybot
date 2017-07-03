from microsoftbotframework import ReplyToActivity
import requests
import json
import datetime


# def echo_response(message):
#     # if message["type"] == "message":
#     #     ReplyToActivity(fill=message,
#     #                     text=message["text"]).send()

def echo_response(message):
    if message["type"] == "message":
        if message['text'] == '비트 코인 시세':
            url = "https://api.korbit.co.kr/v1/ticker"

            response = requests.request("GET", url)

            jj = json.loads(response.text)

            time_s = datetime.datetime.fromtimestamp(
                jj['timestamp'] // 1000
            ).strftime('%Y-%m-%d %H:%M:%S')

            result_text = '최종 시간: %s\n 최종 가격: %s \n' % (time_s, jj['last'])
            print(result_text)

            ReplyToActivity(fill=message,
                            text=result_text).send()
        else:
            ReplyToActivity(fill=message,
                            text=message).send()
