const chat = document.getElementById('messages-container');
let blockNewRequests = false;


chat.addEventListener('scroll', async () => {
    if (!blockNewRequests && -(this.scrollTop) + this.clientHeight >= this.scrollHeight-100) {
        blockNewRequests = true;

        const messagesLength = chat.children.length;
        const url = `/api/v1/chat/${roomName}/messages?start=${messagesLength}&end=${messagesLength+20}`;
        const chatScrollTop = chat.scrollTop;

        await fetch(url, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(async (data) => {
            if (data.error) {
                console.log(data.error);
                return;
            }

            addMessageToChat(data, true);
            
            setTimeout(() => {
                chat.scrollTop = chatScrollTop;
            }, 75);

            await new Promise((resolve) => {
                setTimeout(() => {
                    blockNewRequests = false;
                    resolve();
                }, 300)
            });
        })
        .catch(error => {
            console.log(error);
        });
    }
})

function deleteMessageRequest(id) {
    socket.send(JSON.stringify({
        'type': 'delete_message',
        'message_id': id
    }));
}

function modifyMessageRequest(id, body) {
    socket.send(JSON.stringify({
        'type': 'modify_message',
        'message_id': id,
        'body': body
    }));
}

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    switch (data.type) {
        case 'error':
            return console.log(data.error);
        case 'message_created':
            return addMessageToChat([data], false);
        case 'message_deleted':
            return deleteMessageFromChat(data);
        case 'message_modified':
            return modifyMessageFromChat(data);
        default:
            throw new Error('Invalid socket message type.');
    }
}
