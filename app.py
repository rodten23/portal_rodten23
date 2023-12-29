from flask import Flask, render_template, redirect, request, flash
from flask_mail import Mail, Message
from config import senha_transacoes, meu_email, senha_meu_email

app = Flask(__name__)
app.secret_key = senha_transacoes

mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": meu_email,
    "MAIL_PASSWORD": senha_meu_email
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
    return render_template('index.html')

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
            recipients = ['rodten23@gmail.com', meu_email],
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