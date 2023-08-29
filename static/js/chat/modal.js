const modalDeleteButton = document.getElementById('delete-message-button');
const modalButtons = document.querySelectorAll('.modal-button');
const deletionModal = document.getElementById('deletion-modal');
const cancelButton = document.getElementById('cancel-button');
const exitButton = document.getElementById('exit-button');


cancelButton.addEventListener('click', unToggleDeletionModal);

exitButton.addEventListener('click', unToggleDeletionModal);

addModalButtonsListeners(modalButtons);

window.addEventListener('click', (event) => {
    if (event.target === deletionModal) unToggleDeletionModal();
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
