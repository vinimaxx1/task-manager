// Seleção de elementos
const professorBtn = document.getElementById('professorBtn');
const alunoBtn = document.getElementById('alunoBtn');
const formContainer = document.getElementById('form-container');
const roleInput = document.getElementById('role');
const formTitle = document.getElementById('form-title');
const formSubmit = document.getElementById('formSubmit');
const toggleFormText = document.getElementById('toggleText');
const toggleForm = document.getElementById('toggleForm');
const selectedRole = document.getElementById('selectedRole'); 
let isLogin = true;  // Variável de controle para alternar entre login e registro

// URL base do backend Flask
const apiBaseUrl = 'http://127.0.0.1:5000';  

// Escolher função
professorBtn.addEventListener('click', () => {
    roleInput.value = 'Professor';
    formContainer.classList.remove('hidden');
    selectedRole.textContent = 'Função selecionada: PROFESSOR';  // Exibe "PROFESSOR"
    selectedRole.classList.remove('hidden');  // Torna o texto visível
});

alunoBtn.addEventListener('click', () => {
    roleInput.value = 'Aluno';
    formContainer.classList.remove('hidden');
    selectedRole.textContent = 'Função selecionada: ALUNO';  // Exibe "ALUNO"
    selectedRole.classList.remove('hidden');  // Torna o texto visível
});

// Alternar entre login e registro
toggleForm.addEventListener('click', () => {
    isLogin = !isLogin;
    formTitle.textContent = isLogin ? 'Login' : 'Registro';
    formSubmit.textContent = isLogin ? 'Entrar' : 'Registrar';
    toggleFormText.textContent = isLogin ? 'Registre-se aqui' : 'Faça login aqui';
});

// Enviar formulário
document.getElementById('userForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = {
        role: roleInput.value,
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    if (isLogin) {
        // Fazer requisição de login
        loginUser(formData);
    } else {
        // Fazer requisição de registro
        registerUser(formData);
    }
});

// Função para fazer login
function loginUser(data) {
    fetch(`${apiBaseUrl}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Erro no login');
        }
    })
    .then(result => {
        console.log('Login bem-sucedido:', result);
        // Redirecionar o usuário ou exibir mensagem de sucesso
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao fazer login. Verifique suas credenciais.');
    });
}

// Função para registrar usuário
function registerUser(data) {
    fetch(`${apiBaseUrl}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Erro no registro');
        }
    })
    .then(result => {
        console.log('Registro bem-sucedido:', result);
        alert('Conta criada com sucesso! Faça login para continuar.');
        // Alternar para o formulário de login
        toggleForm.click();
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao registrar. Tente novamente.');
    });
}
