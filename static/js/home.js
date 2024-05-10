// Функция для инициализации карты
function initMap() {
    // Инициализация карты
    var mapCenter = [55.7558, 37.6173]; // Координаты центра Москвы
    var map = DG.map('map', {
        center: mapCenter, // Начальные координаты центра карты
        zoom: 10 // Начальное масштабирование карты
    });

    // Функция для обновления значения поля "Откуда"
    function updatePickupLocation(address) {
        document.getElementById('pickupLocation').value = address;
    }

    // Функция для обработки события ввода адреса пользователем
    function handleAddressInput() {
        var inputAddress = document.getElementById('pickupLocation').value;

        // Выполняем геокодирование введенного адреса
        DG.geocoding().text(inputAddress).run(function (error, response) {
            if (!error && response.results && response.results.length > 0) {
                // Получаем координаты найденного адреса
                var coords = response.results[0].position;

                // Устанавливаем центр карты и масштаб на найденный адрес
                map.setView(coords, 15);
                map.panTo(coords); // Центрируем карту на найденном адресе

                // Обновляем значение поля "Откуда"
                updatePickupLocation(inputAddress);
            }
        });
    }

    // Добавляем обработчик события ввода адреса
    document.getElementById('pickupLocation').addEventListener('input', handleAddressInput);

    // При загрузке страницы выполняем инициализацию карты
    handleAddressInput();
}

// Запускаем инициализацию карты после загрузки страницы
window.onload = function () {
    // Инициализация карты
    initMap();
};
