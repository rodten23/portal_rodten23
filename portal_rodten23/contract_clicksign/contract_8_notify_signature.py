import json
import os
# from pathlib import Path

import httpx
from dotenv import load_dotenv
from flask import Flask

# from portal_rodten23.contract_clicksign.contract_1_create_envelope import (
#     create_envelope,
#     read_envelope,
# )

notify = Flask(__name__)

load_dotenv()

base_url = os.getenv('BASE_URL')
access_token = os.getenv('ACCESS_TOKEN')
# template_id = os.getenv('TEMPLATE_ID')

base_url_response_json = './portal_rodten23/contract_clicksign/'

headers = {
    'Authorization': access_token,
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/json',
}


# @notify.post('/notify_signature')
def notify_signature(envelope_id):
    # response_envelope = Path(f'{base_url_response_json}response_envelope.json')
    # id_envelope = ''

    # if response_envelope.is_file():
    #     id_envelope = read_envelope()
    # else:
    #     id_envelope = create_envelope()

    notify_signature_url = f'{base_url}/envelopes/{envelope_id}/notifications'

    body_notify_signature = json.dumps({
        'data': {
            'type': 'notifications',
            'attributes': {'message': 'Favor, revise e assine este contrato TESTE.'},
        }
    })

    response_notification = httpx.post(
        url=notify_signature_url,
        data=body_notify_signature,
        headers=headers,
        verify=False,
    )

    id_notification = response_notification.json()['data']['id']
    notification_message = response_notification.json()['data']['attributes']['message']
    
    return {'id_notification': id_notification, 'notification_message': notification_message}

    # with open(
    #     f'{base_url_response_json}response_notification.json',
    #     'w',
    #     encoding='utf-8',
    # ) as response_file:
    #     json.dump(
    #         response_notification.json(),
    #         response_file,
    #         ensure_ascii=False,
    #         indent=4,
    #     )

    # return read_notify_sign()


# def read_notify_sign():
#     with open(
#         f'{base_url_response_json}response_notification.json',
#         'r',
#         encoding='utf-8',
#     ) as open_file:
#         data_notification = json.load(open_file)

#     id_notification = data_notification['data']['id']
#     notification_message = data_notification['data']['attributes']['message']

#     return {'id': id_notification, 'message': notification_message}
