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
from portal_rodten23.contract_clicksign.contract_datetime import (
    create_deadline,
)

document = Flask(__name__)

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


@document.post('/criar_documento')
def create_document():
    response_envelope = Path(f'{base_url_response_json}response_envelope.json')
    response_signer = Path(f'{base_url_response_json}response_signer.json')
    id_envelope = ''
    name_signer = ''
    documentation_signer = ''

    if response_envelope.is_file():
        id_envelope = read_envelope()

    else:
        id_envelope = create_envelope()

    if response_signer.is_file():
        name_signer = read_signer()['name_signer']
        documentation_signer = read_signer()['documentation_signer']

    else:
        name_signer = create_signer()['name_signer']
        documentation_signer = create_signer()['documentation_signer']

    create_document_url = f'{base_url}/envelopes/{id_envelope}/documents'

    current_date = create_deadline()['current_date']

    months = [
        '',
        'janeiro',
        'fevereiro',
        'março',
        'abril',
        'maio',
        'junho',
        'julho',
        'agosto',
        'setembro',
        'outubro',
        'novembro',
        'dezembro',
    ]

    body_document = json.dumps({
        'data': {
            'type': 'documents',
            'attributes': {
                'filename': 'Contrato_Teste.docx',
                'template': {
                    'key': template_id,
                    'data': {
                        'enterprise': 'Empresa Teste Ltda',
                        'signer_name': name_signer,
                        'signer_document': documentation_signer,
                        'created_day_contract': current_date.day,
                        'created_month_contract': months[current_date.month],
                        'created_year_contract': current_date.year,
                    },
                    'metadata': {},
                },
            },
        }
    })

    response_document = httpx.post(
        url=create_document_url,
        data=body_document,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}response_document.json',
        'w',
        encoding='utf-8',
    ) as response_file:
        json.dump(
            response_document.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return read_document()


def read_document():
    with open(
        f'{base_url_response_json}response_document.json',
        'r',
        encoding='utf-8',
    ) as open_file:
        data_document = json.load(open_file)

    id_document = data_document['data']['id']

    return id_document
