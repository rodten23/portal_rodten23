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
 
    if (!valid) return;
 
    // Simulate submission
    const btn = document.getElementById('submitBtn');
    btn.textContent = 'Criando contrato teste...';
    btn.disabled = true;
 
    setTimeout(() => {
      btn.textContent = 'Tente novamente!';
      btn.disabled = false;
      form.reset();
      email.classList.remove('is-valid');
 
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 3000);
    }, 1400);
});
 
// Remove invalid on input
['emailInput'].forEach(id => {
    document.getElementById(id).addEventListener('input', function () {
        this.classList.remove('is-invalid');
    });
});