import hmac
import hashlib
from dotenv import load_dotenv
from flask import jsonify, request, abort
import os

load_dotenv()

hmac_clicksign = os.getenv(b'HMAC_SECRET')

signed_file_clicksign = {'download_url': None}


def check_clicksign_response():
    if signed_file_clicksign['signed_file_url']:
        return jsonify({
            'signed_file_available': True,
            'url': signed_file_clicksign['download_url'],
        }), 200
    return jsonify({'signed_file_available': False}), 200


def clicksign_webhook_validator():
    content_hmac_clicksign = request.headers.get('content-hmac')
    if not content_hmac_clicksign:
        abort(401)

    response_clicksign_raw = request.data

    calculated_hmac = hmac.new(
        hmac_clicksign, msg=response_clicksign_raw, digestmod=hashlib.sha256
    ).hexdigest()

    expected_hmac = f'sha256={calculated_hmac}'

    if not hmac.compare_digest(expected_hmac, content_hmac_clicksign):
        abort(403)

    # Webhook validado com sucesso!
    response_clicksign_json = request.json

    if response_clicksign_json and 'document' in response_clicksign_json:
        signed_file_clicksign['download_url'] = response_clicksign_json[
            'document'
        ]['downloads']['signed_file_url']
        print(
            f'Link de download recebido e salvo: {signed_file_clicksign["download_url"]}'
        )

    return jsonify({'webhook_status': 'processado'}), 200
