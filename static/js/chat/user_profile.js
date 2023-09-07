const showUserProfileButton = document.getElementById('show-user-profile-button');
const userProfileContainer = document.getElementById('user-profile-container')
const hideUserProfileButton = document.getElementById('hide-user-profile-button');
const profileEditButtons = document.querySelectorAll('.profile-edit-button');
const saveUserProfileButton = document.getElementById('save-user-profile-button');
const mobileNavbar = document.getElementById('mobile-navbar');


showUserProfileButton.addEventListener('click', () => {
    userProfileContainer.classList.replace('scale-0', 'scale-100');
    if (mobileNavbar) mobileNavbar.classList.toggle('hidden');
})

hideUserProfileButton.addEventListener('click', () => {
    userProfileContainer.classList.replace('scale-100', 'scale-0');
    if (mobileNavbar) mobileNavbar.classList.toggle('hidden');
})

profileEditButtons.forEach(button => {
    const fieldEditType = button.getAttribute('data-edit-type');
    const field = document.getElementById(`edit-profile-${fieldEditType}`);
    let initialText = field.textContent;

    button.addEventListener('click', () => {
        if (field.contentEditable === 'false') {
            field.contentEditable = true;
        }
        else {
            field.textContent = initialText;
            field.contentEditable = false;
        }
    })
})

saveUserProfileButton.addEventListener('click', () => {
    const id = document.getElementById('edit-profile-identifier').textContent;
    const username = document.getElementById(`edit-profile-username`).textContent;
    const email = document.getElementById(`edit-profile-email`).textContent;
    const alias = document.getElementById(`edit-profile-alias`).textContent;
    const description = document.getElementById(`edit-profile-description`).textContent;
    const csrftoken = getCookie('csrftoken');

    fetch(`/api/v1/users/${id}`, {
        method: 'PATCH',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            email: email,
            alias: alias,
            description: description
        })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/channels/@me';
        }
    })
    .catch(error => {
        console.log(error);
    })
})