// Form validation & submit
const form = document.getElementById('contractForm');
 
form.addEventListener('submit', (e) => {
    e.preventDefault();
 
    const email = document.getElementById('emailInput');
    const person_name = document.getElementById('person_name');
    const person_document = document.getElementById('person_document');
    const terms = document.getElementById('termsCheck');
    let valid = true;
 
    // Email
    if (!email.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        email.classList.add('is-invalid');
        email.classList.remove('is-valid');
        valid = false;
    } else {
        email.classList.remove('is-invalid');
        email.classList.add('is-valid');
    }

    // person_name
    // O regex garante: 3 letras iniciais, 1 espaço obrigatório e o restante aceitando letras e espaços.
    // O "person_name.value.length <= 45" garante o limite máximo de tamanho.
    if (!person_name.value || person_name.value.length > 45 || !/^[A-Za-zÀ-ÿ]{3,}\s[A-Za-zÀ-ÿ\s]*$/.test(person_name.value)) {
        person_name.classList.add('is-invalid');
        person_name.classList.remove('is-valid');
        valid = false;
    } else {
        person_name.classList.remove('is-invalid');
        person_name.classList.add('is-valid');
    }



    // if (!person_name.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(person_name.value)) {
    //     person_name.classList.add('is-invalid');
    //     person_name.classList.remove('is-valid');
    //     valid = false;
    // } else {
    //     person_name.classList.remove('is-invalid');
    //     person_name.classList.add('is-valid');
    // }

    // person_document
    let pdValue = e.target.person_document.value.replace(/\D/g, ''); // Remove tudo que não é número
    
    // Aplica a formatação por blocos de dígitos
    if (pdValue.length > 3 && pdValue.length <= 6) {
        pdValue = pdValue.replace(/^(\d{3})(\d+)/, '$1.$2');
    } else if (pdValue.length > 6 && pdValue.length <= 9) {
        pdValue = pdValue.replace(/^(\d{3})(\d{3})(\d+)/, '$1.$2.$3');
    } else if (pdValue.length > 9) {
        pdValue = pdValue.replace(/^(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
    }
    
    // Limita o tamanho máximo ao formato do CPF
    e.target.person_document.value = person_document.value.substring(0, 14);

    if (!person_document.value || !validaCPF(person_document.value)) {
        person_document.classList.add('is-invalid');
        person_document.classList.remove('is-valid');
        valid = false;
    } else {
        person_document.classList.remove('is-invalid');
        person_document.classList.add('is-valid');
    }


    // Terms
    if (!terms.checked) {
        terms.classList.add('is-invalid');
        terms.classList.remove('is-valid');
        valid = false;
    } else {
        terms.classList.remove('is-invalid');
        terms.classList.add('is-valid');
    }
 
    if (!valid) return;
 
    // Simulate submission
    const btn = document.getElementById('submitBtn');
    btn.textContent = 'Criando contrato teste...';
    btn.disabled = true;
});

// 2. Função de cálculo matemático do CPF
function validaCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, ''); // Limpa a máscara para validar
    
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








// function enviarFormulario(event) {
//     if (event) event.preventDefault();

//     const form = document.getElementById('contractForm');
//     const formData = new FormData(form);

//     fetch('/contract', {
//         method:'POST',
//         body: FormData(form)
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.id_signer) {
//             console.log('Novo idSigner recebido:', data.id_signer);
//             renderizarWidget(data.id_signer);
//         } else {
//             setTimeout(() => {
//                 console.error('O Flask não enviou a chave redirect:', data)
//                 btn.textContent = 'Tente novamente!';
//                 btn.disabled = false;
//                 form.reset();
//                 email.classList.remove('is-valid');
//                 email.classList.remove('is-invalid');
//                 terms.classList.remove('is-valid');
//                 terms.classList.remove('is-invalid');
//             }, 5000);
//         }
//     })
//     .catch(error => {
//         console.error('Erro:', error);
//         btn.textContent = 'Erro ao criar contrato!';
//         btn.disabled = false;
//     });    
// });
 
// Remove invalid on input
['emailInput', 'termsCheck'].forEach(id => {
    document.getElementById(id).addEventListener('input', function () {
        this.classList.remove('is-invalid');
    });
});
