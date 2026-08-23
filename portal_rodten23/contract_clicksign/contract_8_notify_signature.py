import json
import os

import httpx
from dotenv import load_dotenv


load_dotenv()

base_url = os.getenv('BASE_URL')
access_token = os.getenv('ACCESS_TOKEN')

base_url_response_json = './portal_rodten23/contract_clicksign/'

headers = {
    'Authorization': access_token,
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/json',
}


def notify_signature(envelope_id):
    notify_signature_url = f'{base_url}/envelopes/{envelope_id}/notifications'

    body_notify_signature = json.dumps({
        'data': {
            'type': 'notifications',
            'attributes': {
                'message': 'Favor, revise e assine este contrato TESTE.'
            },
        }
    })

    response_notification = httpx.post(
        url=notify_signature_url,
        data=body_notify_signature,
        headers=headers,
        verify=False,
    )

    id_notification = response_notification.json()['data']['id']
    notification_message = response_notification.json()['data']['attributes'][
        'message'
    ]

    return {
        'id_notification': id_notification,
        'notification_message': notification_message,
    }
