// Form validation & submit
const form = document.getElementById('contractForm');
 
form.addEventListener('submit', (e) => {
    e.preventDefault();
 
    const email = document.getElementById('emailInput');
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
