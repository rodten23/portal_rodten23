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
from portal_rodten23.contract_clicksign.contract_4_qualify_signer import (
    qualify_signer,
    read_qualify_signer,
)
from portal_rodten23.contract_clicksign.contract_5_define_rubric import (
    define_rubric,
    read_define_rubric,
)

authentication = Flask(__name__)

load_dotenv()

base_url = os.getenv('BASE_URL')
access_token = os.getenv('ACCESS_TOKEN')

base_url_response_json = './portal_rodten23/contract_clicksign/'

headers = {
    'Authorization': access_token,
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/json',
}


@authentication.post('/define_authentication')
def define_authentication():
    response_envelope = Path(f'{base_url_response_json}response_envelope.json')
    response_signer = Path(f'{base_url_response_json}response_signer.json')
    response_document = Path(f'{base_url_response_json}response_document.json')
    response_qualify_signer = Path(
        f'{base_url_response_json}response_qualify_signer.json'
    )
    response_define_rubric = Path(
        f'{base_url_response_json}response_rubric.json'
    )
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

    if response_qualify_signer.is_file():
        read_qualify_signer()
    else:
        qualify_signer()

    if response_define_rubric.is_file():
        read_define_rubric()
    else:
        define_rubric()

    define_authentication_url = (
        f'{base_url}/envelopes/{id_envelope}/requirements'
    )

    body_define_authentication = json.dumps({
        'data': {
            'type': 'requirements',
            'attributes': {'action': 'provide_evidence', 'auth': 'email'},
            'relationships': {
                'document': {'data': {'type': 'documents', 'id': id_document}},
                'signer': {'data': {'type': 'signers', 'id': id_signer}},
            },
        }
    })

    response_define_authentication = httpx.post(
        url=define_authentication_url,
        data=body_define_authentication,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}response_authentication.json',
        'w',
        encoding='utf-8',
    ) as response_file:
        json.dump(
            response_define_authentication.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return read_define_authentication()


def read_define_authentication():
    with open(
        f'{base_url_response_json}response_authentication.json',
        'r',
        encoding='utf-8',
    ) as open_file:
        data_authentication = json.load(open_file)

    id_data_authentication = data_authentication['data']['id']

    return id_data_authentication
