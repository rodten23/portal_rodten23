import hmac
import hashlib
from flask import jsonify, request, abort

token_hmac = b'hmac_clicksign'

dados_globais = {
    'link_arquivo': None
}

def checar_status():
    if dados_globais['link_arquivo']:
        return jsonify({'disponivel': True, 'url': dados_globais['link_arquivo']}), 200
    return jsonify({'disponivel': False}), 200

def webhook():
    assinatura_recebida = request.headers.get('X-Hub-Signature-256')
    if not assinatura_recebida:
        abort(401)

    corpo_bruto = request.data
    assinatura_calculada = hmac.new(token_hmac, msg=corpo_bruto, digestmod=hashlib.sha256).hexdigest()
    assinatura_esperada = f"sha256={assinatura_calculada}"

    if not hmac.compare_digest(assinatura_esperada, assinatura_recebida):
        abort(403)

    # Webhook validado com sucesso!
    dados = request.json
    
    # Supondo que o JSON recebido seja: {"download_url": "https://exemplo.com"}
    if dados and "download_url" in dados:
        dados_globais["link_arquivo"] = dados["download_url"]
        print(f"Link de download recebido e salvo: {dados_globais['link_arquivo']}")

    return jsonify({"status": "processado"}), 200
