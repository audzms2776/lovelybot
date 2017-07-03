from microsoftbotframework import ReplyToActivity
import requests

def echo_response(message):
  if message["type"] == "message":
    if message['text'] == '비트 코인 시세':
      url = "https://api.korbit.co.kr/v1/ticker/detailed"

      headers = {
          'cache-control': "no-cache",
          'postman-token': "3cb8f5cc-b1b2-48de-9086-389941e47ab1"
          }

      response = requests.request("GET", url, headers=headers)

      print(response.text)
      ReplyToActivity(fill=message,
                      text=response.text).send()
