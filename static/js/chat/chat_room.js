const chat = document.getElementById('messages-container');


socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var message = data['message'];

    chat.innerHTML += `<p>${message}</p>`;
};