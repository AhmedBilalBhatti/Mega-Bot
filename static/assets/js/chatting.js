$(document).ready(function () {
    $('form').on('submit', function (event) {
        event.preventDefault();
        var messageInput = $('#userInput');
        var chatlogContainer = $('#chatlog');
        var userMessage = messageInput.val();

        var userMessageHtml = `<div class="msg right-msg"><div class="msg-bubble"><div class="msg-text"><strong>You:</strong> ${userMessage}</div></div></div>`;
        chatlogContainer.append(userMessageHtml);
        chatlogContainer.append(`<div class="msg left-msg"><div class="msg-bubble botchat typing"><p><strong>Dexter:</strong><span class="typewriter glow">Thinking<span class="dots"></span></span></p></div></div>`);

        // Check if the message input is empty
        if (userMessage.trim() !== '') {
            $('.no-chat').addClass('d-none'); // If not empty, hide the "no chat" message
        }

        $.ajax({
            type: 'POST',
            url: '/chat/',
            data: {
                message: userMessage,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                console.log(data);
                chatlogContainer.find('.botchat.typing').remove();

                if (data.bot_response) {
                    var botResponse = $('<div class="msg left-msg"><div class="msg-bubble botchat"><p><strong>Dexter:</strong> <span class="typewriter">' + data.bot_response + '</span></p></div></div>');
                    chatlogContainer.append(botResponse);

                    typeWriter(botResponse.find('.typewriter'), function () {
                        messageInput.val('');
                        // Scroll to the bottom of the chat log
                        chatlogContainer.scrollTop(chatlogContainer.prop("scrollHeight"));
                    });
                }
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText); 
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