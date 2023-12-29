from flask import Flask, render_template, redirect
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

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)