const chat = document.getElementById('messages-container');
const messageInput = document.getElementById('message-input');
const room = document.getElementById(`chat-${roomName}`);
let isSendingMessage = false;


document.onload = room.classList.replace('hover:bg-zinc-700/30', 'bg-zinc-900/40');

messageInput.addEventListener('keydown', function(event) {
    if (event.key == 'Enter' && event.shiftKey == false) {
        var lengthNoSpaces = 0;
        
        event.preventDefault();

        for (var i = 0, len = this.value.length; i < len; i++) {
            if (this.value[i] !== ' ' && this.value[i] !== '\n') {
                lengthNoSpaces += 1;
            };
        };
        if (lengthNoSpaces == 0 || this.value.length >= 511) return;

        socket.send(JSON.stringify({
            'message': this.value
        }));

        this.value = '';
        this.style.height = 'auto';
    };
});

messageInput.addEventListener('input', function() {
    if (this.scrollHeight >= 304) return;
    this.style.height = 'auto';
    this.style.height = `${this.scrollHeight}px`;
});

chat.addEventListener('scroll', function() {
    if (!isSendingMessage && -(this.scrollTop) + this.clientHeight >= this.scrollHeight-100) {
        var messagesLength = chat.children.length;
        var url = `${window.location.origin}/channels/chat/load/messages?chat=${roomName}&length=${messagesLength}`;
        var chatScrollTop = chat.scrollTop;

        isSendingMessage = true;

        fetch(url, {
            method: 'GET'
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.log(data.error);
            } else {
                chat.innerHTML += data.messages;
                
                setTimeout(() => {
                    chat.scrollTop = chatScrollTop;
                }, 50)
            };

            setTimeout(() => {
                isSendingMessage = false;
            }, 500);
        });
    };
});

socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var message = data['message'];
    var sender = data['sender'];
    var avatar = data['avatar'];
    var created = data['created'];

    var newMessage = document.createElement('li');

    newMessage.classList.add('flex', 'rounded-xl', 'hover:bg-zinc-800/30', 'px-2', 'mt-4');

    newMessage.innerHTML += `<div class="top-0 left-0 h-full w-14 mr-3">
                                 <img src="${avatar}" class="rounded-full h-12 w-12">
                             </div>
                             <div class="w-full">
                                 <div class="block">
                                     <span class="cursor-pointer hover:underline">${sender}</span>
                                     <span class="text-sm text-zinc-500">Today at ${created}</span>
                             </div>
                                 <p class="block text-base break-all whitespace-pre-line">${message}</p>
                             </div>`;

    chat.insertBefore(newMessage, chat.firstChild);
};