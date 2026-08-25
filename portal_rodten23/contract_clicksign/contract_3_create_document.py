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
template_id = os.getenv('TEMPLATE_ID')

base_url_response_json = './portal_rodten23/contract_clicksign/'

headers = {
    'Authorization': access_token,
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/json',
}


def create_document(
    envelope_id,
    person_name,
    person_document,
    enterprise_name,
):
    create_document_url = f'{base_url}/envelopes/{envelope_id}/documents'

    if person_name == '':
        person_name = 'Cliente Testador do Brasil'

    if person_document == '':
        person_document = '868.872.680-94'

    if enterprise_name == '':
        enterprise_name = 'Melhor Opção Ltda'

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
                        'enterprise': enterprise_name,
                        'signer_name': person_name,
                        'signer_document': person_document,
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

    id_document = response_document.json()['data']['id']

    return id_document
