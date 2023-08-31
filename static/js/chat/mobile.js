const channelsNavbar = document.getElementById('channels-navbar');
const privateMessagesSidebar = document.getElementById('private-messages-sidebar');
const collapseButton = document.getElementById('collapse-button');
const chatContainer = document.getElementById('chat-container');


collapseButton.addEventListener('click', () => {
    channelsNavbar.classList.toggle('-translate-x-[calc(4rem+16rem+4rem)]');
    privateMessagesSidebar.classList.toggle('-translate-x-[calc(4rem+16rem)]');

    chatContainer.classList.toggle('translate-x-[calc(4rem+16rem)]');
})