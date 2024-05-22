document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal');
    const closeBtn = document.querySelector('.close-btn');
    const modalImage = document.getElementById('modal-image');
    const modalName = document.getElementById('modal-name');
    const modalPrice = document.getElementById('modal-price');
    const modalDescription = document.getElementById('modal-description');
    const ingredientsForm = document.getElementById('ingredients-form');
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value; // Получаем CSRF-токен

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
                checkbox.checked = false;
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
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Добавим обработчик кнопки "Добавить в корзину"
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', async (event) => {
            event.preventDefault(); // Предотвращаем отправку формы по умолчанию
            const pizzaId = button.getAttribute('data-id');
            const pizzaImage = button.parentElement.parentElement.querySelector('.pizza-image');
            const clonedImage = pizzaImage.cloneNode(true);
    
            // Получаем все ингредиенты
            const ingredients = Array.from(document.querySelectorAll('.ingredients input[type="checkbox"]:checked')).map(input => input.value);
    
            const data = {
                pizza_id: pizzaId,
                ingredients: ingredients // Передаем выбранные ингредиенты
            };
    
            clonedImage.classList.add('cart-animation');
            document.body.appendChild(clonedImage);
    
            const cartButton = document.querySelector('.cart-btn');
            const cartRect = cartButton.getBoundingClientRect();
            const pizzaRect = pizzaImage.getBoundingClientRect();
    
            clonedImage.style.left = `${pizzaRect.left}px`;
            clonedImage.style.top = `${pizzaRect.top}px`;
            clonedImage.style.width = `${pizzaRect.width}px`;
            clonedImage.style.height = `${pizzaRect.height}px`;
    
            setTimeout(() => {
                clonedImage.style.transform = `translate(${cartRect.left - pizzaRect.left}px, ${cartRect.top - pizzaRect.top}px) scale(0.5)`;
                clonedImage.style.opacity = '0';
            }, 10);
    
            clonedImage.addEventListener('transitionend', () => {
                clonedImage.remove();
            });
    
            // Отправляем запрос на сервер для добавления в корзину
            const success = await addToCart(pizzaId, csrfToken, data);
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
                    'X-CSRFToken': csrfToken, // Передаем CSRF-токен в заголовок
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

    // Функция для отправки запроса добавления в корзину
    async function addToCart(pizzaId, csrfToken, data) {
        try {
            const response = await fetch(`/add_to_cart/${pizzaId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(data), // Отправляем данные об ингредиентах вместе с идентификатором пиццы
            });

            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }

            const responseData = await response.json();
            if (!responseData.success) {
                console.error('Ошибка при добавлении в корзину:', responseData.error);
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    }
});
