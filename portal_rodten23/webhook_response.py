import hashlib
import hmac
import json
from dotenv import load_dotenv
from flask import abort, request
import os

load_dotenv()

hmac_clicksign = os.getenv('HMAC_SECRET', '').encode('utf-8')


def clicksign_webhook_validator():
    content_hmac_clicksign = request.headers.get('content-hmac')
    content_length_clicksign = request.headers.get('content-length')
    print(content_hmac_clicksign)

    if not content_hmac_clicksign:
        abort(401)

    try:
        if content_length_clicksign:
            lenth = int(content_length_clicksign)
            response_clicksign_raw = request.environ['wsgi.input'].read(lenth)
        else:
            response_clicksign_raw = request.get_data(cache=True)
    except Exception as e:
        print(f'Erro ao ler stream com content-length: {e}')
        abort(400)

    if not response_clicksign_raw:
        print("Erro: Corpo da requisição vazio.")
        abort(400)

    calculated_hmac = hmac.new(
        hmac_clicksign, msg=response_clicksign_raw, digestmod=hashlib.sha256
    ).hexdigest()

    expected_hmac = f'sha256={calculated_hmac}'

    if not hmac.compare_digest(expected_hmac, content_hmac_clicksign):
        print(f"Erro: HMAC não confere.\nEsperado: {expected_hmac}\nRecebido: {content_hmac_clicksign}")
        abort(403)

    try:
        response_clicksign_json = json.loads(response_clicksign_raw.decode('utf-8'))
    except Exception:
        response_clicksign_json = None

    # Webhook validado com sucesso!
    download_url = None

    if response_clicksign_json and 'document' in response_clicksign_json:
        downloads = response_clicksign_json['document'].get('downloads', {})
        download_url = downloads.get('signed_file_url')
        print(f'Link de download recebido e salvo: {download_url}')

    return {
        'webhook_status': 'processado',
        'download_url': download_url,
    }
