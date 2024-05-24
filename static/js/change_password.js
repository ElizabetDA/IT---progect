// Обработчик события для формы смены пароля
document.getElementById('ChangePasswordForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартную отправку формы

    // Получаем форму смены пароля
    const changePasswordForm = document.getElementById("ChangePasswordForm");

    // Отправляем запрос на сервер с использованием fetch API
    fetch('/change_password', {
        method: 'POST',
        body: new FormData(changePasswordForm)
    })
    .then(response => {
        // Проверяем статус ответа
        if (response.ok) {
            // Если ответ успешный, получаем данные ответа
            return response.json();
        } else {
            // Если ответ неуспешный, выводим ошибку
            throw new Error('Ошибка при смене пароля');
        }
    })
    .then(data => {
        // Если ответ успешный, выводим сообщение об успешной смене пароля
        alert(data.message);
        // Перенаправляем пользователя на другую страницу, например, на главную
        window.location.href = '/';
    })
    .catch(error => {
        // Если произошла ошибка, выводим сообщение об ошибке
        alert(error);
    });
});