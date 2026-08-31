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


def define_rubric(envelope_id, id_document, id_signer):
    define_rubric_url = f'{base_url}/envelopes/{envelope_id}/requirements'

    body_define_rubric = json.dumps({
        'data': {
            'type': 'requirements',
            'attributes': {
                'action': 'rubricate',
                'pages': 'all',
                'kind': 'manuscript',
                'rubric_field': 'position_sign_signer',
            },
            'relationships': {
                'document': {'data': {'type': 'documents', 'id': id_document}},
                'signer': {'data': {'type': 'signers', 'id': id_signer}},
            },
        }
    })

    response_define_rubric = httpx.post(
        url=define_rubric_url,
        data=body_define_rubric,
        headers=headers,
        verify=False,
    )

    id_define_rubric = response_define_rubric.json()['data']['id']

    return id_define_rubric
