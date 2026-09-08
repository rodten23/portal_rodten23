// Form validation & submit
const form = document.getElementById('contractForm');
const btn = document.getElementById('submitBtn');
const btnPDF = document.getElementById('btn-pdf');
const statusDownload = document.getElementById('status');
let idContractSession = null;

form.addEventListener('submit', (e) => {
    e.preventDefault();
 
    const emailInput = document.getElementById('emailInput');
    const person_name = document.getElementById('person_name');
    const person_document = document.getElementById('person_document');
    const enterprise_name = document.getElementById('enterprise_name');
    const termsCheck = document.getElementById('termsCheck');
    let valid = true;
 
    // Email (Obrigatório)
    if (!emailInput.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value)) {
        emailInput.classList.add('is-invalid');
        emailInput.classList.remove('is-valid');
        valid = false;
    } else {
        emailInput.classList.remove('is-invalid');
        emailInput.classList.add('is-valid');
    }

    // person_name (Opcional - valida apenas se houver texto)
    const nomeTexto = person_name.value.trim();
    if (nomeTexto !== "") {
        if (nomeTexto.length > 45 || !/^[A-Za-zÀ-ÿ]{3,}\s[A-Za-zÀ-ÿ\s]*$/.test(nomeTexto)) {
            person_name.classList.add('is-invalid');
            person_name.classList.remove('is-valid');
            valid = false;
        } else {
            person_name.classList.remove('is-invalid');
            person_name.classList.add('is-valid');
        }
    } else {
        // Se estiver vazio, limpa as classes de validação e permite o envio
        person_name.classList.remove('is-invalid', 'is-valid');
    }

    // person_document (Opcional - valida apenas se houver texto)
    const cpfTexto = person_document.value.trim();
    if (cpfTexto !== "") {
        if (!validaCPF(cpfTexto)) {
            person_document.classList.add('is-invalid');
            person_document.classList.remove('is-valid');
            valid = false;
        } else {
            person_document.classList.remove('is-invalid');
            person_document.classList.add('is-valid');
        }
    } else {
        // Se estiver vazio, limpa as classes de validação e permite o envio
        person_document.classList.remove('is-invalid', 'is-valid');
    }

    // Terms (Obrigatório)
    if (!termsCheck.checked) {
        termsCheck.classList.add('is-invalid');
        termsCheck.classList.remove('is-valid');
        valid = false;
    } else {
        termsCheck.classList.remove('is-invalid');
        termsCheck.classList.add('is-valid');
    }
 
    if (!valid) {
        console.warn("Envio bloqueado: Existem campos inválidos no formulário.");
        return;
    }
 
    // Enviar formulário via API
    enviarFormulario(form, emailInput, termsCheck, person_name, person_document, enterprise_name);
});

// Máscara em tempo real para o CPF
document.getElementById('person_document').addEventListener('input', function (e) {
    let pdValue = e.target.value.replace(/\D/g, ''); 
    
    if (pdValue.length > 3 && pdValue.length <= 6) {
        pdValue = pdValue.replace(/^(\d{3})(\d+)/, '$1.$2');
    } else if (pdValue.length > 6 && pdValue.length <= 9) {
        pdValue = pdValue.replace(/^(\d{3})(\d{3})(\d+)/, '$1.$2.$3');
    } else if (pdValue.length > 9) {
        pdValue = pdValue.replace(/^(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
    }
    
    e.target.value = pdValue.substring(0, 14); 
});

// Função de cálculo matemático do CPF
function validaCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, ''); 
    
    if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;
    
    let soma = 0, resto;
    for (let i = 1; i <= 9; i++) soma += parseInt(cpf.substring(i - 1, i)) * (11 - i);
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) resto = 0;
    if (resto !== parseInt(cpf.substring(9, 10))) return false;
    
    soma = 0;
    for (let i = 1; i <= 10; i++) soma += parseInt(cpf.substring(i - 1, i)) * (12 - i);
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) resto = 0;
    if (resto !== parseInt(cpf.substring(10, 11))) return false;
    
    return true;
}

// Função para enviar os dados para o Flask
function enviarFormulario(formElement, emailInput, termsCheck, person_name, person_document, enterprise_name) {
    btn.textContent = 'Criando contrato teste...';
    btn.disabled = true;

    // const formData = new FormData(formElement);

    fetch('/contract_test', {
        method: 'POST',
        body: new FormData(formElement)
    })
    .then(response => {

        if (response.status === 429) {
            return response.json().then(errData => {
                throw new Error(errData.message);
            });
        }

        if (!response.ok) throw new Error('Erro na resposta do servidor');
        return response.json();
    })
    .then(data => {
        if (data.id_signer && data.id_document) {
            idContractSession = data.id_document;
            console.log('Novo idSigner recebido:', data.id_signer);
            btn.textContent = 'Criar Contrato Teste'; // Restaura o botão após sucesso
            btn.disabled = false;
            // if (typeof renderizarWidget === 'function') {
            //     renderizarWidget(data.id_signer);
            // }
            renderizarWidget(data.id_signer);
        } else {
            setTimeout(() => {
                console.error('O Flask não enviou a chave id_signer:', data);
                btn.textContent = 'Tente novamente!';
                btn.disabled = false;
                // formElement.reset();
                [emailInput, termsCheck, person_name, person_document].forEach(el => {
                    if (el) el.classList.remove('is-valid', 'is-invalid');
                });
            }, 5000);
        }
    })
    .catch(error => {
        console.error('Erro no envio:', error);
        btn.textContent = error.message;
        btn.style.backgroundColor = "#dc3545";
        btn.style.color = '#ffffff';

        setTimeout(() => {
            btn.textContent = 'Criar Contrato Teste';
            btn.style.backgroundColor = ''; 
            btn.style.color = '';
            btn.disabled = false;
        }, 9000);
    });    
}

// Integração Front-end: Gerenciamento do Widget Embedded da Clicksign
var widgetInstance = null;
var clicksignInterval = null;

function renderizarWidget(idSigner) {
    if (!idSigner) {
        console.error('Nenhum idSigner recebido do Flask ainda.');
        return;
    }

    const container = document.getElementById('container');

    if (widgetInstance) {
        try {
            widgetInstance.unmount();
        } catch (e) {
            console.log('Erro ao desmontar widget anterior:', e);
        }
    }

    container.innerHTML = '';

    widgetInstance = new Clicksign(idSigner);
    widgetInstance.endpoint = 'https://sandbox.clicksign.com';
    widgetInstance.origin = window.location.origin;
    widgetInstance.mount('container');

    widgetInstance.on('loaded', function(event) { 
        console.log('Widget Clicksign carregado com sucesso!'); 
    });

    widgetInstance.on('signed', function(event) {
        console.log('Documento assinado com sucesso pelo usuário!');

        if (clicksignInterval) clearInterval(clicksignInterval);
        
        statusDownload.innerText = "Processando sua assinatura... Por favor, aguarde.";

        checkResponseClicksign();

        clicksignInterval = setInterval(checkResponseClicksign, 5000);
    });
}

// Limpar classes inválidas ao digitar/interagir
['emailInput', 'person_name', 'person_document', 'termsCheck'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
        const eventType = el.type === 'checkbox' ? 'change' : 'input';
        el.addEventListener(eventType, function () {
            this.classList.remove('is-invalid');
        });
    }
});


function checkResponseClicksign() {
    if (!idContractSession) return;

    fetch('/check_response_clicksign?id=' + idContractSession)
        .then(response => response.json())
        .then(data => {
            if (data.signed_file_available) {                 
                // 1. Ativa o botão e muda o texto
                btnPDF.disabled = false;
                btnPDF.innerText = "Baixar Contrato Teste Assinado";

                // 2. Adiciona o evento de clique para abrir o link em nova aba
                btnPDF.onclick = function() {
                    window.open(data.url, '_blank');
                };
                        
                // 3. Atualiza o texto de status
                statusDownload.innerText = "Arquivo gerado com sucesso!";
                        
                // Parar de consultar o servidor já que o arquivo chegou
                clearInterval(clicksignInterval);
                console.log("Checagem encerrada com sucesso.");
            }
        })
        .catch(err => {
            console.error("Erro ao checar status:", err)
        });
}
