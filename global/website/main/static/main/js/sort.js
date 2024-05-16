document.addEventListener('DOMContentLoaded', function() {
    // Ваш JavaScript код для сортировки пицц
    document.getElementById('sort').addEventListener('change', function() {
        const sortBy = this.value;
        const pizzaMenu = document.querySelector('.pizza-menu');
        const pizzaItems = Array.from(pizzaMenu.children);

        if (sortBy === 'по алфавиту') {
            pizzaItems.sort((a, b) => {
                const nameA = a.querySelector('.name').textContent;
                const nameB = b.querySelector('.name').textContent;
                return nameA.localeCompare(nameB);
            });
        } else if (sortBy === 'по цене') {
            pizzaItems.sort((a, b) => {
                const priceA = parseFloat(a.querySelector('.price').textContent.slice(0, -1)); // Удаляем символ валюты из строки и преобразуем в число
                const priceB = parseFloat(b.querySelector('.price').textContent.slice(0, -1)); // Удаляем символ валюты из строки и преобразуем в число
                return priceA - priceB;
            });
        } else if (sortBy === 'popularity') {
            // Добавьте вашу логику для сортировки по популярности здесь
        }

        pizzaItems.forEach(item => pizzaMenu.appendChild(item));
    });
});
