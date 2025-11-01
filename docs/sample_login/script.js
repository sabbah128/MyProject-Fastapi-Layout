const form = document.getElementById('loginForm');
const errorMessage = document.getElementById('errorMessage');
const successMessage = document.getElementById('successMessage');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    errorMessage.style.display = 'none';
    successMessage.style.display = 'none';

    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    try {
        const response = await fetch('http://127.0.0.1:8000/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            successMessage.textContent = 'ورود موفقیت‌آمیز بود!';
            successMessage.style.display = 'block';
            
            // می‌توانید کاربر را به صفحه دیگری هدایت کنید
            setTimeout(() => {
                // window.location.href = '/dashboard';
            }, 1500);
        } else {
            const error = await response.json();
            errorMessage.textContent = error.message || 'نام کاربری یا رمز عبور اشتباه است';
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        errorMessage.textContent = 'خطا در برقراری ارتباط با سرور';
        errorMessage.style.display = 'block';
    }
});