const privateMessagesSidebar = document.getElementById('private-messages-sidebar');
const collapseButton = document.getElementById('collapse-button');
const chatContainer = document.getElementById('chat-container');


collapseButton.addEventListener('click', () => {
    privateMessagesSidebar.classList.toggle('-translate-x-[calc(16rem)]');

    if (chatContainer) chatContainer.classList.toggle('translate-x-[calc(16rem)]');
})