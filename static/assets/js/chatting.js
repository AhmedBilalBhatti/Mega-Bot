const msgerForm = document.querySelector(".msger-inputarea");
const msgerInput = document.querySelector(".msger-input");
const msgerChat = document.querySelector(".msger-chat");

msgerForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const userMessage = msgerInput.value.trim();
    if (!userMessage) return;

    appendMessage("You", PERSON_IMG, "right", userMessage);
    msgerInput.value = "";

    sendUserMessage(userMessage);
});

function appendMessage(name, img, side, text) {
    const msgHTML = `
        <div class="msg ${side}-msg">
            <div class="msg-bubble">
                <div class="msg-text">${text}</div>
            </div>
        </div>
    `;

    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop = msgerChat.scrollHeight;
}

function sendUserMessage(message) {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    
    fetch('{% url "chat" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            message: message
        })
    })
    .then(response => response.json())
    .then(data => {
        const botResponse = data.bot_response;
        appendMessage("Bot", BOT_IMG, "left", botResponse);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
