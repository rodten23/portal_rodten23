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


def qualify_signer(envelope_id, id_document, id_signer):
    qualify_signer_url = f'{base_url}/envelopes/{envelope_id}/requirements'

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

    id_qualify_signer = response_qualify_signer.json()['data']['id']

    return id_qualify_signer
