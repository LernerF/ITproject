document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("orderForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Предотвращаем стандартное действие формы

        var formData = new FormData(this);

        var xhr = new XMLHttpRequest();
        xhr.open("POST", this.action);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    var snackbar = document.getElementById("snackbar");
                    snackbar.style.visibility = "visible";
                    setTimeout(function() {
                        snackbar.style.visibility = "hidden";
                    }, 3000);
                    setTimeout(function() {
                        window.location.reload();
                    }, 3000);
                } else {
                    console.error("Ошибка при оформлении заказа:", xhr.statusText);
                }
            }
        };
        xhr.send(formData);
    });
});
