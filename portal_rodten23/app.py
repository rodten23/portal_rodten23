from flask import Flask, render_template, redirect, request, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import date
from portal_rodten23.calculo_idade import calcular_idade
import os
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

@app.route('/')
def index():
    data_atual =  date.today()
    ano_nasc = os.getenv('ANO_NASCIMENTO')
    mes_nasc = os.getenv('MES_NASCIMENTO')
    dia_nasc = os.getenv('DIA_NASCIMENTO')
    ano_inicio_empresa = os.getenv('ANO_INICIO_EMPRESA')

    idade = calcular_idade(data_atual, ano_nasc, mes_nasc, dia_nasc)
    experiencia = data_atual.year - int(ano_inicio_empresa)
    return render_template('index.html', idade = idade, experiencia = experiencia)

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


if __name__ == '__main__':
    app.run(debug=True)