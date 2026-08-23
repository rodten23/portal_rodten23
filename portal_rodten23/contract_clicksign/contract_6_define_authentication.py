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


def define_authentication(envelope_id, id_document, id_signer):
    define_authentication_url = (
        f'{base_url}/envelopes/{envelope_id}/requirements'
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

    id_define_authentication = response_define_authentication.json()['data'][
        'id'
    ]

    return id_define_authentication
