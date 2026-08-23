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


def create_signer(envelope_id, person_name, emailInput, person_document):
    create_signer_url = f'{base_url}/envelopes/{envelope_id}/signers'

    body_signer = json.dumps({
        'data': {
            'type': 'signers',
            'attributes': {
                'name': f'{person_name}',
                'email': f'{emailInput}',
                'birthday': '2000-01-01',
                'has_documentation': True,
                'documentation': f'{person_document}',
                'refusable': True,
                'group': 1,
                'location_required_enabled': True,
                'communicate_events': {
                    'signature_request': 'email',
                    'signature_reminder': 'email',
                    'document_signed': 'email',
                },
            },
        }
    })

    response_signer = httpx.post(
        url=create_signer_url,
        data=body_signer,
        headers=headers,
        verify=False,
    )

    if response_signer.status_code != 201:
        print(f'Erro na Clicksign (Status {response_signer.status_code}):')
        print(response_signer.text)
        raise Exception(f'Falha ao criar signatário: {response_signer.text}')

    id_signer = response_signer.json()['data']['id']
    name_signer = response_signer.json()['data']['attributes']['name']
    documentation_signer = response_signer.json()['data']['attributes'][
        'documentation'
    ]

    return {
        'id_signer': id_signer,
        'name_signer': name_signer,
        'documentation_signer': documentation_signer,
    }
