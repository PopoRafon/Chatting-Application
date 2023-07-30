const chat = document.getElementById('messages-container');
const messageInput = document.getElementById('message-input');
const room = document.getElementById(`chat-${roomName}`);


room.classList.replace('hover:bg-zinc-700/30', 'bg-zinc-900/40');

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

socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var message = data['message'];
    var sender = data['sender'];
    var avatar = data['avatar'];
    var created = data['created'];

    var newMessage = document.createElement('li');

    newMessage.classList.add('flex', 'rounded-xl', 'hover:bg-zinc-800/30', 'px-2', 'mt-3');

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