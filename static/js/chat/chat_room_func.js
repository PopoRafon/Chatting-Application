const chat = document.getElementById('messages-container');
let blockNewRequests = false;


chat.addEventListener('scroll', async function() {
    if (!blockNewRequests && -(this.scrollTop) + this.clientHeight >= this.scrollHeight-100) {
        blockNewRequests = true;

        const messagesLength = chat.children.length;
        const url = `${window.location.origin}/api/v1/messages/chat/${roomName}?start=${messagesLength}&end=${messagesLength+20}`;
        const chatScrollTop = chat.scrollTop;

        await fetch(url, {
            method: 'GET'
        })
        .then((response) => {
            return response.json();
        })
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
        .catch((err) => {
            console.log(err);
        });
    }
})

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    addMessageToChat([data], false);
};