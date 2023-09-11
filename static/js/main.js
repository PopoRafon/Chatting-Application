const passwordAlert = document.getElementById('password-alert');


if (passwordAlert) {
    setTimeout(() => {
        passwordAlert.remove();
    }, 2000)
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}