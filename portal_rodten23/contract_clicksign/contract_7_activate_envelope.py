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

base_url_response_json = './portal_rodten23/contract_clicksign/'

headers = {
    'Authorization': access_token,
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/json',
}


def activate_envelope(envelope_id):
    activate_envelope_url = f'{base_url}/envelopes/{envelope_id}'

    deadline = create_deadline()['deadline']

    body_activate_envelope = json.dumps({
        'data': {
            'id': envelope_id,
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

    id_activated_envelope = response_activate.json()['data']['id']
    status_activated_envelope = response_activate.json()['data']['attributes'][
        'status'
    ]

    return {
        'id_activated_envelope': id_activated_envelope,
        'status_activated_envelope': status_activated_envelope,
    }
