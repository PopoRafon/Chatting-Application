const modalDeleteButton = document.getElementById('delete-message-button');
const modalButtons = document.querySelectorAll('.modal-button');
const deletionModal = document.getElementById('deletion-modal');
const cancelButton = document.getElementById('cancel-button');
const exitButton = document.getElementById('exit-button');
const conversationSearch = document.getElementById('conversation-search');
const chatsList = document.getElementById('chats-list');


conversationSearch.addEventListener('input', () => {
    const usernameToSearch = conversationSearch.value;

    for (const child of chatsList.children) {
        const usernameElement = child.getElementsByTagName('p')[0];
        const username = usernameElement.textContent;
        
        child.classList.remove('hidden');

        if (!username.includes(usernameToSearch)) {
            child.classList.add('hidden');
        } else {
            usernameElement.innerHTML = username.replace(new RegExp(usernameToSearch, 'gi'), match => `<mark>${match}</mark>`);
        }
    }
})

cancelButton.addEventListener('click', unToggleDeletionModal);

exitButton.addEventListener('click', unToggleDeletionModal);

addModalButtonsListeners(modalButtons);

window.addEventListener('click', (event) => {
    if (event.target === deletionModal) unToggleDeletionModal();
    if (!addNewChatBox.contains(event.target) && !addNewChatButton.contains(event.target)) addNewChatBox.classList.add('hidden');
    if (!inbox.contains(event.target) && !inboxButton.contains(event.target)) inbox.classList.add('hidden');
})

modalDeleteButton.addEventListener('click', () => {
    const messageId = modalDeleteButton.getAttribute('data-message-id');
    const chatId = modalDeleteButton.getAttribute('data-chat-id');

    if (messageId) {
        deleteMessageRequest(messageId);
    } else if (chatId) {
        deleteChatRequest(chatId);
    }

    unToggleDeletionModal();
})

function addModalButtonsListeners(buttons) {
    buttons.forEach((button) => {
        button.addEventListener('click', () => {
            const messageId = button.getAttribute('data-message-id');
            const chatId = button.getAttribute('data-chat-id');
            
            if (messageId) {
                toggleDeletionModal('message', messageId);       
            } else if (chatId) {
                toggleDeletionModal('chat', chatId);
            }
        })
    })
}

function deleteChatRequest(id) {
    const csrftoken = getCookie('csrftoken');

    fetch(`/api/v1/chat/${id}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then((response) => {
        if (response.ok) {
            window.location.href = '/channels/@me';
        }
    })
    .catch(err => {
        console.log(err);
    })
}

function toggleDeletionModal(type, id) {
    const modalMessage = document.getElementById('modal-message');

    deletionModal.classList.add('flex');
    deletionModal.classList.remove('hidden');

    if (type === 'message') {
        modalDeleteButton.setAttribute('data-message-id', id);
        modalMessage.innerText = 'Deleting this message will permanently remove it.\nAre you sure you want to do that?\nThis action cannot be undone.';
    } else if (type === 'chat') {
        modalDeleteButton.setAttribute('data-chat-id', id);
        modalMessage.innerText = 'Deleting this chat will premanently remove all messages within.\nAre you sure you want to do that?\nThis action cannot be undone.';
    }
}

function unToggleDeletionModal() {
    deletionModal.classList.add('hidden');
    deletionModal.classList.remove('flex');

    modalDeleteButton.removeAttribute('data-message-id');
    modalDeleteButton.removeAttribute('data-chat-id');
}
