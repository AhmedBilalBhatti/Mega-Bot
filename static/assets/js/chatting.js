const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_MSGS = ["Hey !!", "Can you please send me $20.59 ?", "Received it", "Can you please share your QR-code ?", "Oky..!! ", "Thank you..!!", "Yes, I’ll send in 10 min"];


const BOT_IMG = "{% static 'assets/images/icons/pro1.png' %}";
const PERSON_IMG = "{% static 'assets/images/icons/pro1.png' %}";
const BOT_NAME = "BOT";
const PERSON_NAME = "Kristin Williams";

// msgerForm.addEventListener("submit", (event) => {
//     event.preventDefault();

//     const msgText = msgerInput.value;
//     if (!msgText) return;

//     appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
//     msgerInput.value = "";

//     botResponse();

//     const nochat = document.querySelector(".no-chat");
//     nochat.classList.add("d-none");
// });

// function appendMessage(name, img, side, text) {
//     //   Simple solution for small apps
//     const msgHTML = `
//     <div class="msg ${side}-msg">
//       <div class="msg-bubble">
//             <div class="msg-text">${text}</div>
//       </div>
//     </div>
//   `;

//     msgerChat.insertAdjacentHTML("beforeend", msgHTML);
//     msgerChat.scrollTop += 500;
// }

// function botResponse() {
//     const r = random(0, BOT_MSGS.length - 1);
//     const msgText = BOT_MSGS[r];
//     const delay = msgText.split(" ").length * 100;

//     setTimeout(() => {
//         appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
//     }, delay);
// }
$(document).ready(function () {
    $('form').on('submit', function (event) {
        event.preventDefault();
        var messageInput = $('#userInput');
        var chatlogContainer = $('#chatlog');
        var botImage = "{% static '/assets/images/user/1.jpg' %}";
        var userMessage = messageInput.val();
        // if ('{{ image_data }}') {
        //     imgSrc = 'data:image/png;base64,' + '{{ image_data }}';
        // }
        var userMessageHtml = '<div class="humanchat" style="color: red;"><img src="' + botImage + '" class="rounded-circle user_img_msg"/><p><strong>You:</strong> ' + userMessage + '</p></div>';
        
        chatlogContainer.append(userMessageHtml);
        chatlogContainer.append('<div class="botchat typing"><img src="' + botImage + '" class="rounded-circle user_img_msg"/><p><strong>Dexter:</strong> <span class="typewriter glow">Thinking<span class="dots"></span></span></p></div>');
        $.ajax({
            type: 'POST',
            url: '{% url "chat" %}',
            data: {
                message: userMessage,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
            success: function (data) {
                chatlogContainer.find('.bocha typing').remove();

                var botResponse = $('<div class=".botchat typing"><img src="' + botImage + '" class="rounded-circle user_img_msg"/><p><strong>Dexter:</strong> <span class="typewriter">' + data.bot_response + '</span></p></div>');
                chatlogContainer.append(botResponse);

                typeWriter(botResponse.find('.typewriter'), function () {
                    messageInput.val('');
                    chatlogContainer.animate({ scrollTop: chatlogContainer[0].scrollHeight });
                });
            }
        });
    });

    function typeWriter(element, callback) {
        var text = element.text();
        element.empty();
        var i = 0;
        var typingEffect = setInterval(function () {
            if (i < text.length) {
                element.append(text.charAt(i));
                i++;
            } else {
                clearInterval(typingEffect);
                if (callback) callback();
            }
        }, 70);
    }
    function toggleDots() {
        var dots = $('.dots');
        dots.text(dots.text() + '.');
        if (dots.text().length > 5) {
            dots.text('');
        }
    }
    setInterval(toggleDots, 300);
});

// Utils
function get(selector, root = document) {
    return root.querySelector(selector);
}

function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();

    return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
}
