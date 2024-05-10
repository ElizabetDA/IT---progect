document.addEventListener('DOMContentLoaded', function() {
    // Обработчик отправки формы
    document.querySelector('form').addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем отправку формы по умолчанию

        // Получаем данные из полей формы
        var formData = new FormData(this);

        // Отправляем POST-запрос на сервер
        fetch('/login', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value // Получаем CSRF токен из скрытого поля
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка при отправке формы');
            }
            return response.json();
        })
        .then(data => {
            // Обрабатываем успешный ответ от сервера
            console.log(data);
            // Перенаправляем пользователя на страницу order.html
            window.location.href = '/order.html';
        })
        .catch(error => {
            // Обрабатываем ошибки
            console.error('Произошла ошибка:', error);
        });
    });
});
