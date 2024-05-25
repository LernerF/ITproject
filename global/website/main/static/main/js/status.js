function sendNotification(orderId, newStatus) {
    setTimeout(() => {
        if (document.visibilityState === 'hidden') {
            if (Notification.permission === 'granted') {
                new Notification(`Ваш заказ №${orderId} обновился`, {
                    body: `Статус заказа изменен на: ${newStatus}`,
                });
            }
        } else {
            // Выводим Snackbar с уведомлением
            showSnackbar(`Ваш заказ №${orderId} обновился. Статус заказа изменен на: ${newStatus}`);
        }
    }, 3000)
}

// Функция для отображения Snackbar
function showSnackbar(message) {
    // Находим элемент Snackbar на странице
    var snackbar = document.getElementById("snackbar");
    // Устанавливаем текст сообщения
    snackbar.textContent = message;
    // Показываем Snackbar
    snackbar.className = "show";
    // Через 3 секунды скрываем Snackbar
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 3000);
}

$(document).ready(function() {
    // Получаем все элементы с классом 'order-id' и проходимся по ним
    $('.order-id').each(function() {
        // Получаем ID заказа из атрибута 'data-order-id'
        var orderId = $(this).data('order-id');
        // Получаем текущий статус из Local Storage (если есть)
        var storedStatus = localStorage.getItem('order-status-' + orderId);
        // Если статус найден, устанавливаем его на странице
        if (storedStatus) {
            $('#order-status-' + orderId).text(storedStatus);
        } else {
            // Если статус не найден, устанавливаем стандартный статус "preparing"
            $('#order-status-' + orderId).text('Готовится');
        }
        // Проверяем, если статус "completed" или "on the way", то не обновляем его
        if (storedStatus !== 'Завершен' && storedStatus !== 'В пути') {
            // Переключаем статус на "on the way" через 20 секунд
            setTimeout(function() {
                $('#order-status-' + orderId).text('В пути');
                // Сохраняем новый статус в Local Storage
                localStorage.setItem('order-status-' + orderId, 'В пути');
                // Отправляем уведомление
                sendNotification(orderId, 'В пути');
            }, 10000); // 10 секунд
            // Переключаем статус на "completed" через 20 секунд
            setTimeout(function() {
                $('#order-status-' + orderId).text('Завершен');
                // Сохраняем новый статус в Local Storage
                localStorage.setItem('order-status-' + orderId, 'Завершен');
                // Отправляем уведомление
                sendNotification(orderId, 'Завершен');
            }, 20000); // 20 секунд
        }
    });
});
