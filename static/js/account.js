// Функция для отправки формы смены пароля
function submitChangePasswordForm() {
  // Получаем форму смены пароля
  const changePasswordForm = document.getElementById("changePasswordForm");

  // Создаем объект FormData для отправки данных формы
  const formData = new FormData(changePasswordForm);

  // Отправляем запрос на сервер с использованием fetch API
  fetch('/change_password', {
    method: 'POST',
    body: formData
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
}

// Добавляем обработчик события для кнопки "Сменить пароль"
document.addEventListener('DOMContentLoaded', function() {
  const changePasswordButton = document.querySelector('.change-password-button');
  if (changePasswordButton) {
    changePasswordButton.addEventListener('click', function() {
      submitChangePasswordForm();
    });
  }
});
document.addEventListener('DOMContentLoaded', function() {
    // Обработчик нажатия на кнопку смены пароля
    document.querySelector('.change-password-button').addEventListener('click', function() {
        // Перенаправляем пользователя на страницу смены пароля
        window.location.href = '/changePassword.html';
    });
});
