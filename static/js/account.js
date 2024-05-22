document.addEventListener('DOMContentLoaded', function() {
    // Обработчик нажатия на кнопку смены пароля
    document.querySelector('.change-password-button').addEventListener('click', function() {
        // Перенаправляем пользователя на страницу смены пароля
        window.location.href = '/changePassword.html';
    });
});
