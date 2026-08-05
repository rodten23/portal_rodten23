import datetime as dt
import json
import os

import httpx
from dotenv import load_dotenv
from flask import Flask

contract = Flask(__name__)

load_dotenv()

base_url = os.getenv('BASE_URL')
access_token = os.getenv('ACCESS_TOKEN')
template_id = os.getenv('TEMPLATE_ID')

base_url_response_json = './portal_rodten23/contract_clicksign/'

headers = {
    'Authorization': access_token,
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/json',
}


@contract.post('/envelopes')
def create_envelope():
    create_envelope_url = f'{base_url}/envelopes'

    current_date = dt.date.today()
    zero_hour = dt.time(0, 0, 0, 0)
    future_date = current_date + dt.timedelta(days=30)
    deadline = f'{future_date}T{zero_hour}.000-03:00'

    body_envelope = json.dumps({
        'data': {
            'type': 'envelopes',
            'attributes': {
                'name': 'Envelope teste',
                'locale': 'pt-BR',
                'auto_close': True,
                'remind_interval': 3,
                'block_after_refusal': True,
                'deadline_at': deadline,
            },
        }
    })

    response_envelope = httpx.post(
        url=create_envelope_url,
        data=body_envelope,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}response_envelope.json', 'w', encoding='utf-8',
    ) as response_file:
        json.dump(
            response_envelope.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return read_envelope()


def read_envelope():
    with open(
        f'{base_url_response_json}response_envelope.json', 'r', encoding='utf-8',
    ) as open_file:
        data_envelope = json.load(open_file)

    id_envelope = data_envelope['data']['id']

    return id_envelope
