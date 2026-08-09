import datetime as dt
import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from flask import Flask, redirect

contract = Flask(__name__)

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


@contract.get('/conta')
def testar_conta():
    testar_conta_url = f'{base_url}/envelopes?access_token={access_token}'

    resposta_conta = httpx.get(url=testar_conta_url, verify=False)

    with open(
        f'{base_url_response_json}resposta_conta.json', 'w', encoding='utf-8'
    ) as response_file:
        json.dump(
            resposta_conta.json(), response_file, ensure_ascii=False, indent=4
        )

    with open(
        f'{base_url_response_json}resposta_conta.json', 'r', encoding='utf-8'
    ) as open_file:
        dados_conta = json.load(open_file)

    chave_conta = dados_conta['data'][0]['id']

    print(chave_conta)

    return redirect('/')


@contract.post('/envelopes')
def criar_envelope():
    criar_envelope_url = f'{base_url}/envelopes'

    data_atual = dt.date.today()
    hora_zerada = dt.time(0, 0, 0, 0)
    data_futura = data_atual + dt.timedelta(days=30)
    data_limite = f'{data_futura}T{hora_zerada}.000-03:00'

    body_envelope = json.dumps({
        'data': {
            'type': 'envelopes',
            'attributes': {
                'name': 'Envelope teste',
                'locale': 'pt-BR',
                'auto_close': True,
                'remind_interval': 3,
                'block_after_refusal': True,
                'deadline_at': data_limite,
            },
        }
    })

    resposta_envelope = httpx.post(
        url=criar_envelope_url,
        data=body_envelope,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}resposta_envelope.json', 'w', encoding='utf-8',
    ) as response_file:
        json.dump(
            resposta_envelope.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return ler_envelope()


def ler_envelope():
    with open(
        f'{base_url_response_json}resposta_envelope.json', 'r', encoding='utf-8',
    ) as open_file:
        dados_envelope = json.load(open_file)

    chave_envelope = dados_envelope['data']['id']

    return chave_envelope


@contract.post('/criar_signatario')
def criar_signatario():
    envelope = Path(f'{base_url_response_json}resposta_envelope.json')
    chave_envelope = ''

    if envelope.is_file():
        chave_envelope = ler_envelope()

    else:
        chave_envelope = criar_envelope()

    criar_signatario_url = f'{base_url}/envelopes/{chave_envelope}/signers'

    body_signatario = json.dumps({
        'data': {
            'type': 'signers',
            'attributes': {
                'name': 'Testador Que Assina',
                'email': 'rodten23@gmail.com',
                'birthday': '2000-01-01',
                'phone_number': '11976198003',
                'has_documentation': True,
                'documentation': '123.480.920-69',
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

    resposta_signatario = httpx.post(
        url=criar_signatario_url,
        data=body_signatario,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}resposta_signatario.json', 'w', encoding='utf-8',
    ) as response_file:
        json.dump(
            resposta_signatario.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return ler_signatario()


def ler_signatario():
    with open(
        f'{base_url_response_json}resposta_signatario.json', 'r', encoding='utf-8',
    ) as open_file:
        dados_signatario = json.load(open_file)

    chave_signatario = dados_signatario['data']['id']
    nome_signatario = dados_signatario['data']['attributes']['name']
    documento_signatario = dados_signatario['data']['attributes'][
        'documentation'
    ]

    return {
        'chave': chave_signatario,
        'nome': nome_signatario,
        'documento': documento_signatario,
    }


@contract.post('/criar_documento')
def criar_documento():
    envelope = Path(f'{base_url_response_json}resposta_envelope.json')
    signatario = Path(f'{base_url_response_json}resposta_signatario.json')
    chave_envelope = ''
    nome_signatario = ''
    documento_signatario = ''

    if envelope.is_file():
        chave_envelope = ler_envelope()

    else:
        chave_envelope = criar_envelope()

    if signatario.is_file():
        nome_signatario = ler_signatario()['nome']
        documento_signatario = ler_signatario()['documento']

    else:
        nome_signatario = criar_signatario()['nome']
        documento_signatario = criar_signatario()['documento']

    criar_documento_url = f'{base_url}/envelopes/{chave_envelope}/documents'

    data_atual = dt.date.today()

    meses = [
        '',
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro',
    ]

    body_documento = json.dumps({
        'data': {
            'type': 'documents',
            'attributes': {
                'filename': 'Contrato_Teste.docx',
                'template': {
                    'key': template_id,
                    'data': {
                        'enterprise': 'Empresa Teste Ltda',
                        'signer_name': nome_signatario,
                        'signer_document': documento_signatario,
                        'created_day_contract': data_atual.day,
                        'created_month_contract': meses[data_atual.month],
                        'created_year_contract': data_atual.year,
                    },
                    'metadata': {},
                },
            },
        }
    })

    resposta_documento = httpx.post(
        url=criar_documento_url,
        data=body_documento,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}resposta_documento.json', 'w', encoding='utf-8',
    ) as response_file:
        json.dump(
            resposta_documento.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return ler_documento()


def ler_documento():
    with open(
        f'{base_url_response_json}resposta_documento.json',
        'r',
        encoding='utf-8',
    ) as open_file:
        dados_documento = json.load(open_file)

    chave_documento = dados_documento['data']['id']

    return chave_documento


@contract.post('/qualificar_signatario_documento')
def qualificar_sig_doc():
    envelope = Path(f'{base_url_response_json}resposta_envelope.json')
    documento = Path(f'{base_url_response_json}resposta_documento.json')
    signatario = Path(f'{base_url_response_json}resposta_signatario.json')
    chave_envelope = ''
    chave_documento = ''
    chave_signatario = ''

    if envelope.is_file():
        chave_envelope = ler_envelope()
    else:
        chave_envelope = criar_envelope()

    if documento.is_file():
        chave_documento = ler_documento()
    else:
        chave_documento = criar_documento()

    if signatario.is_file():
        chave_signatario = ler_signatario()['chave']
    else:
        chave_signatario = criar_signatario()['chave']

    qualificar_sig_doc_url = (
        f'{base_url}/envelopes/{chave_envelope}/requirements'
    )

    body_qualificacao = json.dumps({
        'data': {
            'type': 'requirements',
            'attributes': {'action': 'agree', 'role': 'partner'},
            'relationships': {
                'document': {
                    'data': {'type': 'documents', 'id': chave_documento}
                },
                'signer': {
                    'data': {'type': 'signers', 'id': chave_signatario}
                },
            },
        }
    })

    resposta_qualificar_sig_doc = httpx.post(
        url=qualificar_sig_doc_url,
        data=body_qualificacao,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}resposta_qualificar_sig_doc.json', 'w', encoding='utf-8',
    ) as response_file:
        json.dump(
            resposta_qualificar_sig_doc.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return ler_qualificacao()


def ler_qualificacao():
    with open(
        f'{base_url_response_json}resposta_qualificar_sig_doc.json', 'r', encoding='utf-8',
    ) as open_file:
        dados_qualificacao = json.load(open_file)

    chave_qualificacao = dados_qualificacao['data']['id']

    return chave_qualificacao


@contract.post('/definir_rubrica')
def definir_rubrica():
    envelope = Path(f'{base_url_response_json}resposta_envelope.json')
    documento = Path(f'{base_url_response_json}resposta_documento.json')
    signatario = Path(f'{base_url_response_json}resposta_signatario.json')
    chave_envelope = ''
    chave_documento = ''
    chave_signatario = ''

    if envelope.is_file():
        chave_envelope = ler_envelope()
    else:
        chave_envelope = criar_envelope()

    if documento.is_file():
        chave_documento = ler_documento()
    else:
        chave_documento = criar_documento()

    if signatario.is_file():
        chave_signatario = ler_signatario()['chave']
    else:
        chave_signatario = criar_signatario()['chave']

    definir_rubrica_url = f'{base_url}/envelopes/{chave_envelope}/requirements'

    body_rubrica = json.dumps({
        'data': {
            'type': 'requirements',
            'attributes': {
                'action': 'rubricate',
                'pages': 'all',
                'kind': 'manuscript',
                'rubric_field': 'position_sign_signer',
            },
            'relationships': {
                'document': {
                    'data': {'type': 'documents', 'id': chave_documento}
                },
                'signer': {
                    'data': {'type': 'signers', 'id': chave_signatario}
                },
            },
        }
    })

    resposta_definir_rubrica = httpx.post(
        url=definir_rubrica_url,
        data=body_rubrica,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}resposta_definir_rubrica.json', 'w', encoding='utf-8',
    ) as response_file:
        json.dump(
            resposta_definir_rubrica.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return ler_rubrica()


def ler_rubrica():
    with open(
        f'{base_url_response_json}resposta_definir_rubrica.json', 'r', encoding='utf-8',
    ) as open_file:
        dados_rubrica = json.load(open_file)

    chave_rubrica = dados_rubrica['data']['id']

    return chave_rubrica


@contract.post('/definir_autenticacao')
def definir_autenticacao():
    envelope = Path(f'{base_url_response_json}resposta_envelope.json')
    documento = Path(f'{base_url_response_json}resposta_documento.json')
    signatario = Path(f'{base_url_response_json}resposta_signatario.json')
    chave_envelope = ''
    chave_documento = ''
    chave_signatario = ''

    if envelope.is_file():
        chave_envelope = ler_envelope()
    else:
        chave_envelope = criar_envelope()

    if documento.is_file():
        chave_documento = ler_documento()
    else:
        chave_documento = criar_documento()

    if signatario.is_file():
        chave_signatario = ler_signatario()['chave']
    else:
        chave_signatario = criar_signatario()['chave']

    definir_autenticacao_url = (
        f'{base_url}/envelopes/{chave_envelope}/requirements'
    )

    body_autenticacao = json.dumps({
        'data': {
            'type': 'requirements',
            'attributes': {'action': 'provide_evidence', 'auth': 'email'},
            'relationships': {
                'document': {
                    'data': {'type': 'documents', 'id': chave_documento}
                },
                'signer': {
                    'data': {'type': 'signers', 'id': chave_signatario}
                },
            },
        }
    })

    resposta_definir_autenticacao = httpx.post(
        url=definir_autenticacao_url,
        data=body_autenticacao,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}resposta_definir_autenticacao.json', 'w', encoding='utf-8',
    ) as response_file:
        json.dump(
            resposta_definir_autenticacao.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return ler_autenticacao()


def ler_autenticacao():
    with open(
        f'{base_url_response_json}resposta_definir_autenticacao.json', 'r', encoding='utf-8',
    ) as open_file:
        dados_autenticacao = json.load(open_file)

    chave_autenticacao = dados_autenticacao['data']['id']

    return chave_autenticacao


@contract.patch('/ativar_envelope')
def ativar_envelope():
    envelope = Path(f'{base_url_response_json}resposta_envelope.json')
    chave_envelope = ''

    if envelope.is_file():
        chave_envelope = ler_envelope()

    else:
        chave_envelope = criar_envelope()

    ativar_envelope_url = f'{base_url}/envelopes/{chave_envelope}'

    data_atual = dt.date.today()
    hora_zerada = dt.time(0, 0, 0, 0)
    data_futura = data_atual + dt.timedelta(days=30)
    data_limite = f'{data_futura}T{hora_zerada}.000-03:00'

    body_ativacao = json.dumps({
        'data': {
            'id': chave_envelope,
            'type': 'envelopes',
            'attributes': {
                'status': 'running',
                'deadline_at': data_limite,
                'deadline_partial_signature_action': 'canceled',
            },
        }
    })

    resposta_ativacao = httpx.patch(
        url=ativar_envelope_url,
        data=body_ativacao,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}resposta_ativacao.json', 'w', encoding='utf-8',
    ) as response_file:
        json.dump(
            resposta_ativacao.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return ler_ativacao()


def ler_ativacao():
    with open(
        f'{base_url_response_json}resposta_ativacao.json', 'r', encoding='utf-8',
    ) as open_file:
        dados_ativacao = json.load(open_file)

    chave_envelope = dados_ativacao['data']['id']
    status_envelope = dados_ativacao['data']['attributes']['status']

    return {'chave': chave_envelope, 'status': status_envelope}


@contract.post('/notificar_assinatura')
def notificar_assinatura():
    envelope = Path(f'{base_url_response_json}resposta_envelope.json')
    chave_envelope = ''

    if envelope.is_file():
        chave_envelope = ler_envelope()

    else:
        chave_envelope = criar_envelope()

    notificar_assinatura_url = (
        f'{base_url}/envelopes/{chave_envelope}/notifications'
    )

    body_notificacao = json.dumps({
        'data': {
            'type': 'notifications',
            'attributes': {'message': 'Favor, revise e assine este contrato.'},
        }
    })

    resposta_notificacao = httpx.post(
        url=notificar_assinatura_url,
        data=body_notificacao,
        headers=headers,
        verify=False,
    )

    with open(
        f'{base_url_response_json}resposta_notificacao.json', 'w', encoding='utf-8',
    ) as response_file:
        json.dump(
            resposta_notificacao.json(),
            response_file,
            ensure_ascii=False,
            indent=4,
        )

    return ler_notificacao()


def ler_notificacao():
    with open(
        f'{base_url_response_json}resposta_notificacao.json', 'r', encoding='utf-8',
    ) as open_file:
        dados_notificacao = json.load(open_file)

    chave_notificacao = dados_notificacao['data']['id']
    mensagem_notificacao = dados_notificacao['data']['attributes']['message']

    return {'chave': chave_notificacao, 'mensagem': mensagem_notificacao}
