document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const pizzaId = this.dataset.pizzaId;
            addToCart(pizzaId);
        });
    });

    function addToCart(pizzaId) {
        fetch('/add_to_cart/' + pizzaId + '/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                console.log('Pizza added to cart');
                updateCartCount();  // Обновляем счетчик корзины
            } else {
                console.error('Error adding pizza to cart');
            }
        })
        .catch(error => console.error('Error adding pizza to cart:', error));
    }

    // Функция для получения значения CSRF-токена из куки
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Функция для обновления счетчика корзины
    function updateCartCount() {
        fetch('/cart/count/')
        .then(response => response.json())
        .then(data => {
            const cartCountElement = document.querySelector('.cart-count');
            if (cartCountElement) {
                cartCountElement.textContent = data.cart_count;
            }
        })
        .catch(error => console.error('Error updating cart count:', error));
    }
});
