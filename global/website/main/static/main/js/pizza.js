// pizza.js
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal');
    const closeBtn = document.querySelector('.close-btn');
    const modalImage = document.getElementById('modal-image');
    const modalName = document.getElementById('modal-name');
    const modalPrice = document.getElementById('modal-price');
    const modalDescription = document.getElementById('modal-description');
    const ingredientsForm = document.getElementById('ingredients-form');

    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', () => {
            const imageUrl = button.getAttribute('data-image');
            const name = button.getAttribute('data-name');
            const price = button.getAttribute('data-price');
            const description = button.getAttribute('data-description');

            modalImage.src = imageUrl;
            modalName.textContent = name;
            modalPrice.textContent = `${price}₽`;
            modalDescription.textContent = description;

            // Reset form and check all checkboxes
            ingredientsForm.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = true;
            });

            // Set form action URL dynamically
            ingredientsForm.action = `/add_to_cart/${button.getAttribute('data-id')}/`;

            modal.style.display = 'flex';
        });
    });

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    // Добавим обработку нажатия на кнопку удаления ингредиента
    document.querySelectorAll('.remove-ingredient').forEach(removeBtn => {
        removeBtn.addEventListener('click', () => {
            const ingredientId = removeBtn.dataset.id;
            const ingredientCheckbox = document.querySelector(`input[value="${ingredientId}"]`);
            if (ingredientCheckbox) {
                ingredientCheckbox.checked = false;
            }
        });
    });

    // Добавим обработку отправки формы
    ingredientsForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Предотвращаем отправку формы по умолчанию

        // Собираем данные для отправки на сервер
        const formData = new FormData(ingredientsForm);

        try {
            const response = await fetch(ingredientsForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}', // Добавляем CSRF-токен
                }, 
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    // Если успешно добавлено в корзину, закрываем модальное окно
                    modal.style.display = 'none';
                    // Можно добавить здесь логику для отображения уведомления о успешном добавлении в корзину
                } else {
                    console.error('Ошибка при добавлении в корзину:', data.error);
                    // Можно добавить здесь логику для отображения сообщения об ошибке
                }
            } else {
                console.error('Ошибка HTTP:', response.status);
                // Можно добавить здесь логику для отображения сообщения об ошибке
            }
        } catch (error) {
            console.error('Ошибка:', error);
            // Можно добавить здесь логику для отображения сообщения об ошибке
        }
    });
});
