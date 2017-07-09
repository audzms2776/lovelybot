from microsoftbotframework import ReplyToActivity
import requests
import json
import os
import datetime
import urllib.request


def echo_response(message):
    if message["type"] == "message":
        key_list = list(message.keys())

        if key_list.count('attachments'):
            attach_data = message['attachments'][0]

            urllib.request.urlretrieve(attach_data['contentUrl'], attach_data['name'])

            # file size check
            if os.path.getsize(attach_data['name']) >> 20 >= 2:
                os.remove('./' + attach_data['name'])
                ReplyToActivity(fill=message,
                                text='파일이 너무 큽니다. 2MB 이하만 가능합니다.').send()
                return

            # naver celebrity
            # https://developers.naver.com/docs/clova/face/reference/#celebrity-응답예시
            client_id = "a1RZIb1p59TLbq3iu_un"
            client_secret = "yzvyDMQvAL"
            url = "https://openapi.naver.com/v1/vision/celebrity"
            files = {'image': open(attach_data['name'], 'rb')}
            headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
            response = requests.post(url, files=files, headers=headers)
            rescode = response.status_code
            files.clear()

            os.remove('./' + attach_data['name'])

            temp_str = ''

            if rescode == 200:
                print(response.text)
                faces = json.loads(response.text)['faces']

                if not len(faces):
                    temp_str = '해당하는 연예인을 찾을 수 없습니다.'

                for idx, face_data in enumerate(faces):
                    temp_str += str(idx + 1) + ' 순위 : ' + face_data['celebrity']['value'] + '\n'

            else:
                temp_str = '통신 오류'

            ReplyToActivity(fill=message,
                            text=temp_str).send()

        # bit coin price
        # https://apidocs.korbit.co.kr/ko/#최종-체결-가격
        if key_list.count('text'):
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
                r = message['text'] + ' @_@'
                ReplyToActivity(fill=message,
                                text=r).send()
