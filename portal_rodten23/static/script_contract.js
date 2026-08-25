// Form validation & submit
const form = document.getElementById('contractForm');
const btn = document.getElementById('submitBtn');

form.addEventListener('submit', (e) => {
    e.preventDefault();
 
    const email = document.getElementById('emailInput');
    const person_name = document.getElementById('person_name');
    const person_document = document.getElementById('person_document');
    const terms = document.getElementById('termsCheck');
    let valid = true;
 
    // Email (Obrigatório)
    if (!email.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        email.classList.add('is-invalid');
        email.classList.remove('is-valid');
        valid = false;
    } else {
        email.classList.remove('is-invalid');
        email.classList.add('is-valid');
    }

    // person_name (Opcional - valida apenas se houver texto)
    if (person_name.value.trim() !== "") {
        if (person_name.value.length > 45 || !/^[A-Za-zÀ-ÿ]{3,}\s[A-Za-zÀ-ÿ\s]*$/.test(person_name.value)) {
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
    if (person_document.value.trim() !== "") {
        if (!validaCPF(person_document.value)) {
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
    if (!terms.checked) {
        terms.classList.add('is-invalid');
        terms.classList.remove('is-valid');
        valid = false;
    } else {
        terms.classList.remove('is-invalid');
        terms.classList.add('is-valid');
    }
 
    if (!valid) return;
 
    // Enviar formulário via API
    enviarFormulario(form, email, terms);
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
function enviarFormulario(formElement, email, terms) {
    btn.textContent = 'Criando contrato teste...';
    btn.disabled = true;

    const formData = new FormData(formElement);

    fetch('/contract', {
        method: 'POST',
        body: formData 
    })
    .then(response => {
        if (!response.ok) throw new Error('Erro na resposta do servidor');
        return response.json();
    })
    .then(data => {
        if (data.id_signer) {
            console.log('Novo idSigner recebido:', data.id_signer);
            if (typeof renderizarWidget === 'function') {
                renderizarWidget(data.id_signer);
            }
        } else {
            setTimeout(() => {
                console.error('O Flask não enviou a chave id_signer:', data);
                btn.textContent = 'Tente novamente!';
                btn.disabled = false;
                formElement.reset();
                [email, terms, document.getElementById('person_name'), document.getElementById('person_document')].forEach(el => {
                    el.classList.remove('is-valid', 'is-invalid');
                });
            }, 5000);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        btn.textContent = 'Erro ao criar contrato!';
        btn.disabled = false;
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
