const room = document.getElementById(`chat-${roomName}`);
const messageInput = document.getElementById('message-input');
const modalButtons = document.querySelectorAll('.modal-button');
const deletionModal = document.getElementById('deletion-modal');
const cancelButton = document.getElementById('cancel-button');
const exitButton = document.getElementById('exit-button');
const editButtons = document.querySelectorAll('.edit-button');
const user = JSON.parse(document.getElementById('user').textContent);


room.classList.replace('hover:bg-zinc-700/30', 'bg-zinc-900/40');

addModalButtonsListeners(modalButtons);

addEditButtonsListeners(editButtons);

messageInput.addEventListener('input', function() {
    if (this.scrollHeight >= 304) return;
    this.style.height = 'auto';
    this.style.height = `${this.scrollHeight}px`;
})

messageInput.addEventListener('keydown', (event) => {
    if (event.key == 'Enter' && event.shiftKey === false) {
        let lengthNoSpaces = 0;
        
        event.preventDefault();

        for (let i = 0, len = messageInput.value.length; i < len; i++) {
            if (messageInput.value[i] !== ' ' && messageInput.value[i] !== '\n') {
                lengthNoSpaces += 1;
            }
        }
        if (lengthNoSpaces == 0 || messageInput.value.length >= 511) return;

        socket.send(JSON.stringify({
            'type': 'send_message',
            'message': messageInput.value
        }))

        messageInput.value = '';
        messageInput.style.height = 'auto';
    }
})

function addMessageToChat(data, oldMessage) {
    let fragment = document.createDocumentFragment();
    const date = new Date();
    const today = `${date.getFullYear()}-${("0" + (date.getMonth() + 1)).slice(-2)}-${date.getDate()}`;
    const yesterday = `${date.getFullYear()}-${("0" + (date.getMonth() + 1)).slice(-2)}-${date.getDate()-1}`;

    for (let message in data) {
        const id = data[message].id;
        const body = data[message].body;
        const sender = data[message].sender;
        const avatar = data[message].avatar;
        const created = data[message].created.split(" ");
        let wasCreated;

        if (today === created[0]) {
            wasCreated = 'Today at';
        } else if (yesterday === created[0]) {
            wasCreated = 'Yesterday at';
        } else {
            wasCreated = created[0];
        }
        
        const newMessage = document.createElement('li');
    
        newMessage.id = `message-${id}`;
        
        newMessage.classList.add('flex', 'relative', 'group/toolbar', 'rounded-xl', 'hover:bg-zinc-800/30', 'px-2', 'mt-4');

        newMessage.innerHTML += `
        <div class="top-0 left-0 h-full w-14 mr-2 mt-1">
            <img src="${avatar}" class="rounded-full h-12 w-12">
        </div>
        <div class="w-full overflow-y-auto invisible-scrollbar">
            <div class="block px-1">
                <span class="cursor-pointer hover:underline">${sender}</span>
                <span class="text-sm text-zinc-500">${wasCreated} ${created[1]}</span>
            </div>
            <div>
                <div>
                    <p id="message-${id}-body" class="text-base block whitespace-pre-line break-words px-1 rounded-lg focus:outline-none" contenteditable="false">${body}</p>
                </div>
                <div id="message-${id}-modified" class="text-sm w-1/6">
                </div>
            </div>
        </div>`;

        if (user === sender) {
            newMessage.innerHTML += `
            <div class="hidden absolute group-hover/toolbar:inline-flex top-0 right-0 mr-2 rounded-md transform -translate-y-1/2 text-center bg-zinc-700 border border-zinc-800">
                <button class="flex justify-center items-center p-1 rounded-tl-md rounded-bl-md hover:bg-zinc-600">
                    <img src="/static/images/buttons/add_emote_button.png" class="w-6 h-6">
                </button>
                <button class="edit-button flex justify-center items-center p-1 hover:bg-zinc-600" data-message-id="${id}">
                    <img src="/static/images/buttons/edit_message_button.png" class="w-6 h-6">
                </button>
                <button class="modal-button flex justify-center items-center p-1 rounded-tr-md rounded-br-md hover:bg-zinc-600" data-message-id="${id}">
                    <img src="/static/images/buttons/delete_message_button.png" class="w-6 h-6">
                </button>
            </div>`;
        }


        fragment.appendChild(newMessage);
    }

    const newModalButtons = fragment.querySelectorAll('.modal-button');
    const newEditButtons = fragment.querySelectorAll('.edit-button');

    addModalButtonsListeners(newModalButtons);

    addEditButtonsListeners(newEditButtons);

    oldMessage ? chat.appendChild(fragment) : chat.insertBefore(fragment, chat.firstChild);
}

function deleteMessageFromChat(data) {
    const id = data.id;
    const message = document.getElementById(`message-${id}`);

    message.remove();
}

window.addEventListener('click', (event) => {
    if (event.target === deletionModal) unToggleDeletionModal();
})

cancelButton.addEventListener('click', unToggleDeletionModal)

exitButton.addEventListener('click', unToggleDeletionModal)

function unToggleDeletionModal() {
    deletionModal.classList.add('hidden');
    deletionModal.classList.remove('flex');
}

function toggleDeletionModal(id) {
    deletionModal.classList.add('flex');
    deletionModal.classList.remove('hidden');

    deleteButton.setAttribute('data-message-id', id);
}

function modifyMessageFromChat(data) {
    const id = data.id;
    const time = data.time;
    const body = data.body;
    const message = document.getElementById(`message-${id}-body`);
    const modified = document.getElementById(`message-${id}-modified`);

    message.textContent = body;
    
    modified.innerHTML = `
    <span class="group/modified text-zinc-500">
        (modified)
        <span class="hidden absolute rounded-md group-hover/modified:block transform -translate-y-12 -translate-x-4 bg-zinc-700 text-white py-1 px-2">
            Today at ${time}
        </span>
    </span>`
}
 
function addModalButtonsListeners(buttons) {
    buttons.forEach((button) => {
        button.addEventListener('click', () => {
            const messageId = button.getAttribute('data-message-id');
    
            toggleDeletionModal(messageId);       
        })
    })
}

function addEditButtonsListeners(buttons) {
    buttons.forEach((button) => {
        let initialTextContent;
    
        button.addEventListener('click', () => {
            const messageId = button.getAttribute('data-message-id');
            const message = document.getElementById(`message-${messageId}-body`);
    
            if (message.contentEditable === 'false') {
                message.contentEditable = true;
                message.classList.add('bg-zinc-700/40');
                
                initialTextContent = message.textContent; 
    
                message.addEventListener('keydown', (event) => {
                    if (event.key === 'Enter' && event.shiftKey == false) {
                        let lengthNoSpaces = 0;
    
                        if (message.textContent === initialTextContent) return;
                        
                        for (let i = 0, len = message.textContent.length; i < len; i++) {
                            if (message.textContent[i] !== ' ' && message.textContent[i] !== '\n') {
                                lengthNoSpaces += 1;
                            }
                        }
                        
                        if (lengthNoSpaces == 0 || message.textContent.length >= 511) {
                            event.preventDefault();
                            return;
                        }
    
                        message.contentEditable = false;
                        message.classList.remove('bg-zinc-700/40');
    
                        modifyMessageRequest(messageId, message.textContent);
                    }
                })
            } else {
                message.contentEditable = false;
                message.classList.remove('bg-zinc-700/40');
    
                message.textContent = initialTextContent;
            }
        })
    })
};
