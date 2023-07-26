const chat = document.getElementById('messages-container');
const messageInput = document.getElementById('message-input');


messageInput.addEventListener('input', function() {
    if (this.scrollHeight >= 304) return;
    this.style.height = 'auto';
    this.style.height = `${this.scrollHeight}px`;
});

socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var message = data['message'];
};