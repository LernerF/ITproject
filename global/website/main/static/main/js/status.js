function sendNotification(orderId, newStatus) {
    setTimeout(() => {
        if (document.visibilityState === 'hidden') {
            if (Notification.permission === 'granted') {
                new Notification(`Ваш заказ №${orderId} обновился`, {
                    body: `Статус заказа изменен на: ${newStatus}`,
                });
            }
        }
    }, 3000)
}

function updateOrderStatus(orderId) {
    // Отправляем GET-запрос на сервер для получения статуса заказа
    $.ajax({
        url: '/order-history/get-order-status/' + orderId + '/',
        method: 'GET',
        success: function(data) {
            // Определяем следующий этап статуса заказа
            var nextStatus;
            switch (data.status) {
                case 'Готовится':
                    nextStatus = 'on_the_way';
                    break;
                case 'on_the_way':
                    nextStatus = 'completed';
                    break;
                case 'completed':
                    // Если заказ завершен, прекратить обновление
                    return;
            }
            // Обновляем статус заказа на странице
            $('#order-status-' + orderId).text(nextStatus);
        },
        error: function(error) {
            console.log('Error fetching order status:', error);
        }
    });
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
