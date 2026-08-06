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
from portal_rodten23.contract_clicksign.contract_2_create_signer import (
    create_signer,
    read_signer,
)
from portal_rodten23.contract_clicksign.contract_3_create_document import (
    create_document,
    read_document,
)

qualify = Flask(__name__)

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


@qualify.post('/qualify_signer')
def qualify_signer():
    response_envelope = Path(f'{base_url_response_json}response_envelope.json')
    response_signer = Path(f'{base_url_response_json}response_signer.json')
    response_document = Path(f'{base_url_response_json}response_document.json')
    id_envelope = ''
    id_signer = ''
    id_document = ''

    if response_envelope.is_file():
        id_envelope = read_envelope()
    else:
        id_envelope = create_envelope()

    if response_signer.is_file():
        id_signer = read_signer()['id_signer']
    else:
        id_signer = create_signer()['id_signer']

    if response_document.is_file():
        id_document = read_document()
    else:
        id_document = create_document()

    qualify_signer_url = f'{base_url}/envelopes/{id_envelope}/requirements'

    body_qualify_signer = json.dumps({
        'data': {
            'type': 'requirements',
            'attributes': {'action': 'agree', 'role': 'partner'},
            'relationships': {
                'document': {'data': {'type': 'documents', 'id': id_document}},
                'signer': {'data': {'type': 'signers', 'id': id_signer}},
            },
        }
    })

    response_qualify_signer = httpx.post(
        url=qualify_signer_url,
        data=body_qualify_signer,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}response_qualify_signer.json',
        'w',
        encoding='utf-8',
    ) as response_file:
        json.dump(
            response_qualify_signer.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return read_qualify_signer()


def read_qualify_signer():
    with open(
        f'{base_url_response_json}response_qualify_signer.json',
        'r',
        encoding='utf-8',
    ) as open_file:
        data_qualify_signer = json.load(open_file)

    id_qualify_signer = data_qualify_signer['data']['id']

    return id_qualify_signer
