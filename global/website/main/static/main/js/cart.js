document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll('.cart-form');

    forms.forEach(form => {
        form.addEventListener('click', function(event) {
            if (event.target.name === 'action') {
                form.dataset.action = event.target.value;
            }
        });

        form.addEventListener('submit', async function(event) {
            event.preventDefault();

            const action = form.dataset.action;
            const url = form.getAttribute('action');
            const pizzaId = form.closest('.cart-item').dataset.pizzaId;
            const formData = new FormData(form);
            formData.append('action', action);

            console.log(`Submitting form for pizzaId: ${pizzaId}, action: ${action}`);

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                    },
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                console.log('Response data:', data);

                if (data.success) {
                    const cartItems = document.querySelectorAll(`.cart-item[data-pizza-id="${pizzaId}"]`);
                    cartItems.forEach(cartItem => {
                        const quantityElement = cartItem.querySelector('.quantity');
                        const priceElement = cartItem.querySelector('.cart-item-price');
                        const totalPriceElement = document.querySelector('.total-price');

                        if (data.quantity === 0) {
                            console.log(`Removing cart item with pizzaId: ${pizzaId}`);
                            cartItem.remove();
                        } else {
                            const oldQuantity = parseInt(quantityElement.textContent.split(':')[1].trim());
                            console.log(`Old quantity: ${oldQuantity}, new quantity: ${data.quantity}`);
                            if (oldQuantity === data.quantity) {
                                console.error('Ошибка: Количество не изменилось');
                                showSnackbar('Количество не изменилось');
                            } else {
                                quantityElement.textContent = `Количество: ${data.quantity}`;
                                priceElement.textContent = `${data.item_total_price}₽`;
                                showSnackbar('Количество обновлено');
                            }
                        }

                        // Update total price or handle empty cart
                        const remainingItems = document.querySelectorAll('.cart-item');
                        if (remainingItems.length === 0) {
                            totalPriceElement.remove(); // Remove the total price element
                            document.querySelector('ul').remove(); // Remove the list
                            document.querySelector('.order-btn').remove(); // Remove the order button
                            const emptyMessage = document.createElement('p');
                            emptyMessage.textContent = 'Корзина пуста';
                            document.body.appendChild(emptyMessage);
                            showSnackbar('Корзина пуста');
                        } else {
                            totalPriceElement.textContent = `Общая сумма: ${data.total_price}₽`;
                        }
                    });
                } else {
                    console.error('Ошибка: ' + data.error);
                    showSnackbar('Произошла ошибка: ' + data.error);
                }
            } catch (error) {
                console.error('Ошибка:', error);
                showSnackbar('Произошла ошибка: ' + error.message);
            }
        });
    });
});

function showSnackbar(message) {
    const snackbar = document.getElementById("snackbar");
    snackbar.textContent = message;
    snackbar.className = "show";
    setTimeout(() => { snackbar.className = snackbar.className.replace("show", ""); }, 3000);
}
