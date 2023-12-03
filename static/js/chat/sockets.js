const roomName = JSON.parse(document.getElementById('chat-name').textContent);

const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
)

socket.onclose = (event) => {
    console.log("Exiting socket connection.");
}
