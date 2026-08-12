from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import date
from portal_rodten23.calculate_datetime import calculate_age
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

load_dotenv()

app = Flask(__name__)
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


class Contato:
    def __init__(self, nome, email, message):
        self.nome = nome
        self.email = email
        self.message = message


class Contract:
    def __init__(
        self, emailInput, person_name, person_document, enterprise_name
    ):
        self.emailInput = emailInput
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


@app.route('/contract', methods=['GET', 'POST'])
def contract():
    if request.method == 'GET':
        return render_template('contract.html')

    if request.method == 'POST':
        form_Contract = Contract(
            request.form.get('emailInput'),
            request.form.get('person_name'),
            request.form.get('person_document'),
            request.form.get('enterprise_name'),
        )

        envelope_id = create_envelope()

        signer = create_signer(envelope_id = envelope_id, person_name = form_Contract.person_name, emailInput = form_Contract.emailInput, person_document = form_Contract.person_document)

        id_signer = signer['id_signer']

        id_document = create_document(envelope_id = envelope_id, enterprise_name = form_Contract.enterprise_name, name_signer = form_Contract.person_name, documentation_signer = form_Contract.person_document)

        id_qualify_signer = qualify_signer(envelope_id = envelope_id, id_document = id_document, id_signer = id_signer)

        id_define_rubric = define_rubric(envelope_id = envelope_id, id_document = id_document, id_signer = id_signer)

        id_define_authentication = define_authentication(envelope_id = envelope_id, id_document = id_document, id_signer = id_signer)

        activated_envelope = activate_envelope(envelope_id = envelope_id)

        print(envelope_id)

        print(id_signer)

        print(id_document)

        print(id_qualify_signer)

        print(id_define_rubric)

        print(id_define_authentication)

        print(activated_envelope['id_activated_envelope'], activated_envelope['status_activated_envelope'],)

        return jsonify({"id_signer": id_signer})

        # return render_template(
        #     'contract.html',
        #     id_signer = id_signer
        # )

        

        # print(form_Contract.emailInput, form_Contract.person_name, form_Contract.person_document, form_Contract.enterprise_name)

        # print(testar_conta())
        # return jsonify({"redirect": "/"})


# @app.route('/create_contract', methods=['POST'])
# def create_contract():
#     if request.method == 'POST':
#         form_Contract = Contract(
#             request.form['emailInput'],
#             request.form['person_name'],
#             request.form['cpf'],
#             request.form['enterprise_name']
#         )

#         return testar_conta()

#     return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
