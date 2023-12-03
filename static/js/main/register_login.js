const form = document.getElementById('form');


form.addEventListener('submit', (event) => {
    event.preventDefault();

    sendFormData();
})

function sendFormData() {
    const url = window.location.href;
    const csrftoken = getCookie('csrftoken');
    const data = new FormData(form);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: data
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.json();
        }
    })
    .then((data) => {
        const errors = data.errors;
        const inputFields = form.querySelectorAll('.invalid-form-input');

        inputFields.forEach(input => {
            const paragraph = document.getElementById(`invalid-${input.name}`);

            input.classList.replace('invalid-form-input', 'standard-form-input');

            paragraph.innerText = '&nbsp;';
            paragraph.classList.replace('visible', 'invisible');
        })

        for (let key in errors) {
            const element = document.getElementsByName(key)[0];
            const paragraph = document.getElementById(`invalid-${key}`);

            element.classList.replace('standard-form-input', 'invalid-form-input');

            paragraph.innerText = errors[key][0];
            paragraph.classList.replace('invisible', 'visible');
        }
    })
    .catch((error) => {
        console.log(error);
    })
}
