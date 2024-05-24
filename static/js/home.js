// Функция для инициализации карты
function initMap() {
    // Инициализация карты
    var mapCenter = [55.7558, 37.6173]; // Координаты центра Москвы
    var map = DG.map('map', {
        center: mapCenter, // Начальные координаты центра карты
        zoom: 10 // Начальное масштабирование карты
    });

    // Получаем текущее местоположение пользователя
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var userCoords = [position.coords.latitude, position.coords.longitude];
            // Используем местоположение пользователя в качестве центра карты
            map.setView(userCoords, 15); // Устанавливаем приближение на местоположение пользователя

            // Добавляем маркер на местоположение пользователя
            var userMarker = DG.marker(userCoords).addTo(map);
            userMarker.bindPopup('Ваше местоположение').openPopup(); // Отображаем всплывающее окно с названием местоположения

            // Получаем адрес по координатам пользователя
            var xhr = new XMLHttpRequest();
            var url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat=' + userCoords[0] + '&lon=' + userCoords[1] + '&zoom=18&addressdetails=1';
            xhr.open('GET', url, true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var response = JSON.parse(xhr.responseText);
                    if (response && response.address) {
                        var addressDetails = response.address;

                        // Получаем необходимые части адреса (например, улицу и номер дома)
                        var street = addressDetails.road || '';
                        var houseNumber = addressDetails.house_number || '';
                        var address = street + ', ' + houseNumber;

                        console.log('Ваше местоположение:', address);

                        // Обновляем значение поля "Откуда"
                        document.getElementById('pickupLocation').value = address;

                        // Центрируем карту и приближаемся к адресу пользователя
                        map.setView(userCoords, 15);
                    }
                }
            };
            xhr.send(null);

        }, function () {
            console.log('Не удалось получить текущее местоположение.');
        });
    } else {
        console.log('Геолокация не поддерживается данным браузером.');
    }

    // Настройка стилей для карты
    map.options.attributionControl = false; // Убираем атрибуцию
    map.getContainer().style.backgroundColor = '#f5f5f5'; // Устанавливаем серый цвет фона карты

    // Обработчик события клика на карту для предотвращения скрытия верхней полосы
    map.getContainer().addEventListener('click', function (e) {
        e.stopPropagation();
    });


    // Функция для центрирования карты по адресу
    function centerMap(address) {
        // Получаем координаты по адресу
        var geocoder = DG.geocoding({apiKey: '261dd9c7-7968-4e32-924a-14a15afb00c7'});
        geocoder.geocode(address, function (result) {
            if (result.length > 0) {
                var coordinates = result[0].center;
                // Центрируем карту по координатам
                map.setView(coordinates, 15);

                // Устанавливаем маркер на новое местоположение
                userMarker.setLatLng(coordinates);

                // Получаем адрес по координатам
                var xhr = new XMLHttpRequest();
                var url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat=' + coordinates[0] + '&lon=' + coordinates[1] + '&zoom=18&addressdetails=1';
                xhr.open('GET', url, true);
                xhr.onreadystatechange = function () {
                    if (xhr.readyState == 4 && xhr.status == 200) {
                        var response = JSON.parse(xhr.responseText);
                        if (response && response.address) {
                            var addressDetails = response.address;

                            // Получаем необходимые части адреса (например, улицу и номер дома)
                            var street = addressDetails.road || '';
                            var houseNumber = addressDetails.house_number || '';
                            var address = street + ', ' + houseNumber;

                            console.log('Новое местоположение:', address);

                            // Обновляем значение поля "Откуда"
                            document.getElementById('pickupLocation').value = address;
                        }
                    }
                };
                xhr.send(null);
            } else {
                console.log('Адрес не найден.');
            }
        });
    }

    // Обработчик события изменения значения поля "Откуда"
    document.getElementById('pickupLocation').addEventListener('change', function () {
        var address = this.value;
        centerMap(address);
    });
}

// Запускаем инициализацию карты после загрузки страницы
window.onload = function () {
    // Инициализация карты
    initMap();
};