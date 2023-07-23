const form = document.getElementById('form');


form.addEventListener('submit', function(event) {
    event.preventDefault();

    sendFormData();
});

function sendFormData() {
    var url = window.location.href;
    var csrftoken = getCookie('csrftoken');
    var data = new FormData(form);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
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
    .then(data => {
        var errors = data.errors;
        var inputFields = form.querySelectorAll('.invalid-form-input');

        inputFields.forEach(input => {
            var paragraph = document.getElementById(`invalid-${input.name}`);

            input.classList.replace('invalid-form-input', 'standard-form-input');

            paragraph.innerText = '&nbsp;';
            paragraph.classList.replace('visible', 'invisible');
        })

        for (let key in errors) {
            var element = document.getElementsByName(key)[0];
            var paragraph = document.getElementById(`invalid-${key}`);

            element.classList.replace('standard-form-input', 'invalid-form-input');

            paragraph.innerText = errors[key][0];
            paragraph.classList.replace('invisible', 'visible');
        }
    })
    .catch(error => {
        console.log(error);
    });
};

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
