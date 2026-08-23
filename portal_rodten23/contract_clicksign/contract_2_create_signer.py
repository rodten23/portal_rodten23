import json
import os
#from pathlib import Path

import httpx
from dotenv import load_dotenv
from flask import Flask

# from portal_rodten23.contract_clicksign.contract_1_create_envelope import (
#     create_envelope,
#     read_envelope,
# )

signer = Flask(__name__)

load_dotenv()

base_url = os.getenv('BASE_URL')
access_token = os.getenv('ACCESS_TOKEN')

base_url_response_json = './portal_rodten23/contract_clicksign/'

headers = {
    'Authorization': access_token,
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/json',
}


# @signer.post('/create_signer')
def create_signer(envelope_id, person_name, emailInput, person_document):
    # response_envelope = Path(f'{base_url_response_json}response_envelope.json')
    # id_envelope = ''

    # if response_envelope.is_file():
    #     id_envelope = read_envelope()

    # else:
    #     id_envelope = create_envelope()

    create_signer_url = f'{base_url}/envelopes/{envelope_id}/signers'

    body_signer = json.dumps({
        'data': {
            'type': 'signers',
            'attributes': {
                'name': f'{person_name}',
                'email': f'{emailInput}',
                'birthday': '2000-01-01',
                #'phone_number': '11976198003',
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
    documentation_signer = response_signer.json()['data']['attributes']['documentation']

    return {
        'id_signer': id_signer,
        'name_signer': name_signer,
        'documentation_signer': documentation_signer,
     }



#     with open(
#         f'{base_url_response_json}response_signer.json',
#         'w',
#         encoding='utf-8',
#     ) as response_file:
#         json.dump(
#             response_signer.json(),
#             response_file,
#             ensure_ascii=False,
#             indent=4,
#         )

#     return read_signer()


# def read_signer():
#     with open(
#         f'{base_url_response_json}response_signer.json',
#         'r',
#         encoding='utf-8',
#     ) as open_file:
#         data_signer = json.load(open_file)

#     id_signer = data_signer['data']['id']
#     name_signer = data_signer['data']['attributes']['name']
#     documentation_signer = data_signer['data']['attributes']['documentation']

#     return {
#         'id_signer': id_signer,
#         'name_signer': name_signer,
#         'documentation_signer': documentation_signer,
#     }
