const room = document.getElementById(`chat-${roomName}`);
const messageInput = document.getElementById('message-input');
const modalButtons = document.querySelectorAll('.modal-button');
const deletionModal = document.getElementById('deletion-modal');
const cancelButton = document.getElementById('cancel-button');
const exitButton = document.getElementById('exit-button');
const user = JSON.parse(document.getElementById('user').textContent);


document.onload = room.classList.replace('hover:bg-zinc-700/30', 'bg-zinc-900/40');

messageInput.addEventListener('input', function() {
    if (this.scrollHeight >= 304) return;
    this.style.height = 'auto';
    this.style.height = `${this.scrollHeight}px`;
})

messageInput.addEventListener('keydown', function(event) {
    if (event.key == 'Enter' && event.shiftKey == false) {
        let lengthNoSpaces = 0;
        
        event.preventDefault();

        for (let i = 0, len = this.value.length; i < len; i++) {
            if (this.value[i] !== ' ' && this.value[i] !== '\n') {
                lengthNoSpaces += 1;
            }
        }
        if (lengthNoSpaces == 0 || this.value.length >= 511) return;

        socket.send(JSON.stringify({
            'type': 'send_message',
            'message': this.value
        }))

        this.value = '';
        this.style.height = 'auto';
    }
})

function addMessageToChat(data, oldMessage) {
    let fragment = document.createDocumentFragment();
    const date = new Date(); 
    const today = `${date.getFullYear()}-${("0" + (date.getMonth() + 1)).slice(-2)}-${date.getDate()}`
    const yesterday = `${date.getFullYear()}-${("0" + (date.getMonth() + 1)).slice(-2)}-${date.getDate()-1}`

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

        newMessage.innerHTML += `<div class="top-0 left-0 h-full w-14 mr-3 mt-1">
                                    <img src="${avatar}" class="rounded-full h-12 w-12">
                                </div>
                                <div class="w-full overflow-y-auto invisible-scrollbar">
                                    <div class="block">
                                        <span class="cursor-pointer hover:underline">${sender}</span>
                                        <span class="text-sm text-zinc-500">${wasCreated} ${created[1]}</span>
                                    </div>
                                    <div>
                                        <div>
                                            <p class="text-base block whitespace-pre-line break-words">${body}</p>
                                        </div>
                                        <div class="ml-3 text-sm w-1/6">
                                        </div>
                                    </div>
                                </div>`;

        if (user === sender) {
            newMessage.innerHTML += `<div class="hidden absolute group-hover/toolbar:inline-flex top-0 right-0 mr-2 rounded-md transform -translate-y-1/2 text-center bg-zinc-700 border border-zinc-800">
                                        <button class="flex justify-center items-center p-1 rounded-tl-md rounded-bl-md hover:bg-zinc-600">
                                            <img src="/static/images/buttons/add_emote_button.png" class="w-6 h-6">
                                        </button>
                                        <button class="flex justify-center items-center p-1 hover:bg-zinc-600">
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

    newModalButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const message_id = button.getAttribute('data-message-id');
    
            toggleDeletionModal(message_id);
        })        
    })

    oldMessage ? chat.appendChild(fragment) : chat.insertBefore(fragment, chat.firstChild);
}

function deleteMessageFromChat(data) {
    const id = data.id;
    const message = document.getElementById(`message-${id}`);

    message.remove();
}

modalButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const message_id = button.getAttribute('data-message-id');

        toggleDeletionModal(message_id);       
    })
})

window.addEventListener('click', () => {
    if (event.target === deletionModal) {
        unToggleDeletionModal();
    }
})

cancelButton.addEventListener('click', () => {
    unToggleDeletionModal();
})

exitButton.addEventListener('click', () => {
    unToggleDeletionModal();
})

function unToggleDeletionModal() {
    deletionModal.classList.add('hidden');
    deletionModal.classList.remove('flex');
}

function toggleDeletionModal(id) {
    deletionModal.classList.add('flex');
    deletionModal.classList.remove('hidden');

    deleteButton.setAttribute('data-message-id', id);
}
