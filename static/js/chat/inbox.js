const addNewChatButton = document.getElementById('add-new-chat-button');
const addNewChatBox = document.getElementById('add-new-chat-box');
const addNewChatForm = document.getElementById('add-new-chat-form');
const inboxButton = document.getElementById('inbox-button');
const inbox = document.getElementById('inbox');
const requestButtons = document.querySelectorAll('.request-button');
const alertBox = document.getElementById('alert-box');
const alertMessage = document.getElementById('alert-message');


requestButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const id = button.getAttribute('data-request-id');
        const requestBox = document.getElementById(`request-${id}`)
        const decision = button.getAttribute('data-request-decision');
        const csrftoken = getCookie('csrftoken');

        fetch(`/api/v1/requests/${id}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                decision: decision
            })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                const body = data.success;
    
                alertBox.classList.toggle('hidden');
                alertMessage.innerText = body;
    
                setTimeout(() => {
                    alertBox.classList.toggle('hidden');
                }, 2000)
            }
        })
        .catch(error => {
            console.log(error);
        })

        requestBox.remove();
    })
})

inboxButton.addEventListener('click', () => {
    inbox.classList.toggle('hidden');
})

addNewChatButton.addEventListener('click', () => {
    addNewChatBox.classList.toggle('hidden');
})

addNewChatForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const userToRequest = document.getElementById('user-to-request');
    const userIdentifier = userToRequest.value;
    const csrftoken = getCookie('csrftoken');

    fetch('/api/v1/requests', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            receiver: userIdentifier
        })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log(data);
    })
    .catch(error => {
        console.log(error)
    })

    userToRequest.value = '';
})
