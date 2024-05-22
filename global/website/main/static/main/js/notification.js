button.addEventListener ('click', async () => {
    const perm = await Notification.requestPermission()

    if (perm === 'granted'){
        new Notification('Спасибо!', {
            body: 'Теперь мы можем уведомлять вас о важных событиях!',
        })
    }
})