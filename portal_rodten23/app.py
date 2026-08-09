from flask import Flask, render_template, redirect, request, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import date
from portal_rodten23.calculo_idade import calcular_idade
import os

from portal_rodten23.contract_clicksign.contract_0_8 import testar_conta

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SENHA_CRIPTO_TRANSACOES")

mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": os.getenv("MEU_EMAIL"),
    "MAIL_PASSWORD": os.getenv("SENHA_MEU_EMAIL")
}

app.config.update(mail_settings)

mail = Mail(app)

class Contato:
    def __init__(self, nome, email, message):
        self.nome = nome
        self.email = email
        self.message = message

class Contract:
    def __init__(self, emailInput, person_name, cpf, enterprise_name):
        self.emailInput = emailInput
        self.person_name = person_name
        self.cpf = cpf
        self.enterprise_name = enterprise_name


@app.route('/')
def index():
    data_atual =  date.today()
    ano_nasc = os.getenv('ANO_NASCIMENTO')
    mes_nasc = os.getenv('MES_NASCIMENTO')
    dia_nasc = os.getenv('DIA_NASCIMENTO')
    ano_inicio_empresa = os.getenv('ANO_INICIO_EMPRESA')

    idade = calcular_idade(data_atual, ano_nasc, mes_nasc, dia_nasc)
    experiencia = data_atual.year - int(ano_inicio_empresa)
    return render_template('index.html', idade = idade, experiencia = experiencia, ano_corrente = data_atual.year)

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        form_Contato = Contato(
            request.form['nome'],
            request.form['email'],
            request.form['message']
        )

        msg = Message(
            subject = f'{form_Contato.nome} te enviou uma mensagem pelo portifólio!',
            sender = app.config.get("MAIL_USERNAME"),
            recipients = ['rodten23@gmail.com', app.config.get("MAIL_USERNAME")],
            body = f'''

            {form_Contato.nome}, com o e-mail {form_Contato.email}, enviou a seguinte mensagem:

            {form_Contato.message}
            '''
        )

        mail.send(msg)

        flash('Mensagem enviada com sucesso!')
    
    return redirect('/')


@app.route('/contract')
def contract():
    return render_template('/contract.html')


@app.route('/create_contract', methods=['GET', 'POST'])
def create_contract():
    if request.method == 'POST':
        form_Contract = Contract(
            request.form['emailInput'],
            request.form['person_name'],
            request.form['cpf'],
            request.form['enterprise_name']
        )
            
    return testar_conta()


if __name__ == '__main__':
    app.run(debug=True)