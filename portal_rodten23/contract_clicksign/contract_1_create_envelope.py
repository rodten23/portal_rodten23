import json
import os

import httpx
from dotenv import load_dotenv

from portal_rodten23.calculate_datetime import (
    create_deadline,
)


load_dotenv()

base_url = os.getenv('BASE_URL')
access_token = os.getenv('ACCESS_TOKEN')

base_url_response_json = './portal_rodten23/contract_clicksign/'

headers = {
    'Authorization': access_token,
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/json',
}


def create_envelope():
    create_envelope_url = f'{base_url}/envelopes'

    body_envelope = json.dumps({
        'data': {
            'type': 'envelopes',
            'attributes': {
                'name': 'Envelope teste',
                'locale': 'pt-BR',
                'auto_close': True,
                'remind_interval': 3,
                'block_after_refusal': True,
                'deadline_at': create_deadline()['deadline'],
            },
        }
    })

    response_envelope = httpx.post(
        url=create_envelope_url,
        data=body_envelope,
        headers=headers,
        verify=False,
    )

    return response_envelope.json()['data']['id']
