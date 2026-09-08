from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_limiter import Limiter
from flask_limiter import RateLimitExceeded
from flask_limiter.util import get_remote_address
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import date
from portal_rodten23.calculate_datetime import calculate_age
import re
import os

from portal_rodten23.contract_clicksign.contract_1_create_envelope import (
    create_envelope,
)

from portal_rodten23.contract_clicksign.contract_2_create_signer import (
    create_signer,
)

from portal_rodten23.contract_clicksign.contract_3_create_document import (
    create_document,
)

from portal_rodten23.contract_clicksign.contract_4_qualify_signer import (
    qualify_signer,
)

from portal_rodten23.contract_clicksign.contract_5_define_rubric import (
    define_rubric,
)

from portal_rodten23.contract_clicksign.contract_6_define_authentication import (
    define_authentication,
)

from portal_rodten23.contract_clicksign.contract_7_activate_envelope import (
    activate_envelope,
)

from portal_rodten23.contract_clicksign.contract_8_notify_signature import (
    notify_signature,
)

from portal_rodten23.webhook_response import clicksign_webhook_validator

load_dotenv()

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=['360 per day'],
    storage_uri='memory://'
)

app.secret_key = os.getenv('TRANSACTION_ENCRYPTION_PASSWORD')

mail_settings = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USE_SSL': False,
    'MAIL_USERNAME': os.getenv('MY_EMAIL'),
    'MAIL_PASSWORD': os.getenv('MY_EMAIL_PASSWORD'),
}

app.config.update(mail_settings)

mail = Mail(app)

signed_contracts = {}

signed_file_clicksign = {'download_url': None}


class Contato:
    def __init__(self, nome, email, message):
        self.nome = nome
        self.email = email
        self.message = message


class Contract:
    def __init__(
        self,
        emailInput,
        termsCheck,
        person_name,
        person_document,
        enterprise_name,
    ):
        self.emailInput = emailInput
        self.termsCheck = termsCheck
        self.person_name = person_name
        self.person_document = person_document
        self.enterprise_name = enterprise_name


@app.route('/')
def index():
    current_date = date.today()
    year_birth = os.getenv('YEAR_BIRTH')
    month_birth = os.getenv('MONTH_BIRTH')
    day_birth = os.getenv('DAY_BIRTH')
    year_joining_company = os.getenv('YEAR_JOINING_COMPANY')

    my_age = calculate_age(
        current_date=current_date,
        year_birth=year_birth,
        month_birth=month_birth,
        day_birth=day_birth,
    )
    it_experience = current_date.year - int(year_joining_company)

    return render_template(
        'index.html',
        idade=my_age,
        experiencia=it_experience,
        ano_corrente=current_date.year,
    )


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        form_Contato = Contato(
            request.form['nome'],
            request.form['email'],
            request.form['message'],
        )

        msg = Message(
            subject=f'{form_Contato.nome} te enviou uma mensagem pelo portifólio!',
            sender=app.config.get('MAIL_USERNAME'),
            recipients=['rodten23@gmail.com', app.config.get('MAIL_USERNAME')],
            body=f"""

            {form_Contato.nome}, com o e-mail {form_Contato.email}, enviou a seguinte mensagem:

            {form_Contato.message}
            """,
        )

        mail.send(msg)

        flash('Mensagem enviada com sucesso!')

    return redirect('/')


def valida_cpf(cpf: str) -> bool:
    if cpf == '':
        return True

    else:
        cpf = re.sub(r'\D', '', cpf)

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = (soma * 10) % 11
        if resto in (10, 11):
            resto = 0
        if resto != int(cpf[9]):
            return False

        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = (soma * 10) % 11
        if resto in (10, 11):
            resto = 0
        if resto != int(cpf[10]):
            return False

        return True


@app.route('/terms_service_contract_test')
def terms_service_contract_test():
    current_date = date.today()
    return render_template('terms_service_contract_test.html', ano_corrente=current_date.year)


@app.route('/privacy_policy_contract_test')
def privacy_policy_contract_test():
    current_date = date.today()
    return render_template('privacy_policy_contract_test.html', ano_corrente=current_date.year)


@app.route('/contract_test', methods=['GET', 'POST'])
@limiter.limit(
    '5 per hour',
    exempt_when=lambda: request.method == 'GET',
    error_message='Limite de criação de contratos teste excedido. Tente novamente mais tarde.'
)
def contract_test():
    if request.method == 'GET':
        return render_template('contract_test.html')

    if request.method == 'POST':
        
        form_Contract = Contract(
            request.form.get('emailInput'),
            request.form.get('termsCheck'),
            request.form.get('person_name'),
            request.form.get('person_document'),
            request.form.get('enterprise_name'),
        )

        if not form_Contract.emailInput or not form_Contract.termsCheck:
            return jsonify({
                'error': 'validation_error',
                'message': 'E-mail e termos de uso são obrigatórios.',
            }), 400

        if form_Contract.person_document:
            if not valida_cpf(form_Contract.person_document):
                return jsonify({
                    'error': 'invalid_cpf',
                    'message': 'O CPF fornecido é inválido.',
                }), 400

        try:
            envelope_id = create_envelope()

            signer = create_signer(
                envelope_id=envelope_id,
                person_name=form_Contract.person_name,
                emailInput=form_Contract.emailInput,
                person_document=form_Contract.person_document,
            )

            id_signer = signer['id_signer']

            id_document = create_document(
                envelope_id=envelope_id,
                enterprise_name=form_Contract.enterprise_name,
                person_name=form_Contract.person_name,
                person_document=form_Contract.person_document,
            )

            id_qualify_signer = qualify_signer(
                envelope_id=envelope_id,
                id_document=id_document,
                id_signer=id_signer,
            )

            id_define_rubric = define_rubric(
                envelope_id=envelope_id,
                id_document=id_document,
                id_signer=id_signer,
            )

            id_define_authentication = define_authentication(
                envelope_id=envelope_id,
                id_document=id_document,
                id_signer=id_signer,
            )

            activated_envelope = activate_envelope(envelope_id=envelope_id)

            notification = notify_signature(envelope_id=envelope_id)

            print(envelope_id)

            print(id_signer)

            print(id_document)

            print(id_qualify_signer)

            print(id_define_rubric)

            print(id_define_authentication)

            print(
                activated_envelope['id_activated_envelope'],
                activated_envelope['status_activated_envelope'],
            )

            print(
                notification['id_notification'],
                notification['notification_message'],
            )

            return jsonify({
                'success': True,
                'id_signer': id_signer,
                'id_document': id_document,
                'message': 'Contrato teste criado com sucesso!',
            }), 200

        except Exception as e:
            print(f'Erro interno: {str(e)}')
            return jsonify({
                'error': 'internal_error',
                'message': 'Erro ao processar o contrato no servidor.',
            }), 500


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Muitas requisições',
        'message': str(e.description)
    }), 429


@app.route('/check_response_clicksign', methods=['GET'])
def check_clicksign_response():

    id_document_request = request.args.get('id')

    if not id_document_request:
        return jsonify({'erro': 'ID do documento ausente.'})

    link = signed_contracts.get(id_document_request)

    print(signed_contracts)

    if link:
        return jsonify({
            'signed_file_available': True,
            'url': link,
        }), 200
    return jsonify({'signed_file_available': False}), 200


    # if signed_file_clicksign['download_url']:
    #     return jsonify({
    #         'signed_file_available': True,
    #         'url': signed_file_clicksign['download_url'],
    #     }), 200
    # return jsonify({'signed_file_available': False}), 200


@app.route('/webhook', methods=['POST'])
def webhook():
    clicksign_response = clicksign_webhook_validator()

    signed_contracts[f'{clicksign_response['id_document_webhook']}'] = clicksign_response['download_url_webhook']

    print(f"ID documento do webhook: {clicksign_response['id_document_webhook']}")

    #signed_file_clicksign['download_url'] = clicksign_response['download_url']

    return jsonify(clicksign_response), 200

    
if __name__ == '__main__':
    app.run(debug=True)
