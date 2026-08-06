import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from flask import Flask

from portal_rodten23.contract_clicksign.contract_1_create_envelope import (
    create_envelope,
    read_envelope,
)
from portal_rodten23.contract_clicksign.contract_datetime import (
    create_deadline,
)

activate = Flask(__name__)

load_dotenv()

base_url = os.getenv('BASE_URL')
access_token = os.getenv('ACCESS_TOKEN')

base_url_response_json = './portal_rodten23/contract_clicksign/'

headers = {
    'Authorization': access_token,
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/json',
}


@activate.patch('/activate_envelope')
def activate_envelope():
    response_envelope = Path(f'{base_url_response_json}response_envelope.json')
    id_envelope = ''

    if response_envelope.is_file():
        id_envelope = read_envelope()

    else:
        id_envelope = create_envelope()

    activate_envelope_url = f'{base_url}/envelopes/{id_envelope}'

    deadline = create_deadline()['deadline']

    body_activate_envelope = json.dumps({
        'data': {
            'id': id_envelope,
            'type': 'envelopes',
            'attributes': {
                'status': 'running',
                'deadline_at': deadline,
                'deadline_partial_signature_action': 'canceled',
            },
        }
    })

    response_activate = httpx.patch(
        url=activate_envelope_url,
        data=body_activate_envelope,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}response_activate.json',
        'w',
        encoding='utf-8',
    ) as response_file:
        json.dump(
            response_activate.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return read_activate_envelope()


def read_activate_envelope():
    with open(
        f'{base_url_response_json}response_activate.json',
        'r',
        encoding='utf-8',
    ) as open_file:
        data_activate = json.load(open_file)

    id_activate_envelope = data_activate['data']['id']
    status_activate_envelope = data_activate['data']['attributes']['status']

    return {'chave': id_activate_envelope, 'status': status_activate_envelope}
