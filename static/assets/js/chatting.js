$(document).ready(function () {
    var chatStarted = false;
    var isBotResponding = false; // Flag to track if the bot is responding
    var currentTypingEffect; // To store the current typing effect interval
    var currentBotResponse; // To store the current bot response element

    $('form').on('submit', function (event) {
        event.preventDefault();
        var messageInput = $('#userInput');
        var chatlogContainer = $('#chatlog');
        var userMessage = messageInput.val().trim();

        if (userMessage === '' || isBotResponding) { // Check if user input is empty or bot is responding
            return;
        }

        // Clear input field
        messageInput.val('');

        // Disable input during bot response
        messageInput.prop('disabled', true);

        var userMessageHtml = `<div class="msg right-msg"><div class="msg-bubble"><div class="msg-text"><strong>You:</strong> ${userMessage}</div></div></div>`;
        chatlogContainer.append(userMessageHtml);
        chatlogContainer.append(`<div class="msg left-msg"><div class="msg-bubble botchat typing"><p><strong>Dexter:</strong><span class="typewriter glow">Thinking<span class="dots"></span></span></p></div></div>`);

        if (!chatStarted) {
            $('.no-chat').addClass('d-none');
            $('.main-chat').css('background-color', '#0a0e17');
            $('.chat-header').css('background-color', '#0a0e17');
            chatStarted = true;
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
                    var botResponse = $('<div class="msg left-msg"><div class="msg-bubble botchat"><p><strong>Dexter:</strong> <span class="typewriter"></span></p><button class="gg-play-button-o"></button></div></div>');
                    chatlogContainer.append(botResponse);
                    currentBotResponse = botResponse.find('.typewriter');

                    currentTypingEffect = typeWriter(currentBotResponse, data.bot_response, function () {
                        chatlogContainer.animate({ scrollTop: chatlogContainer[0].scrollHeight });

                        // Enable input after bot response
                        messageInput.prop('disabled', false);
                        isBotResponding = false;
                    });

                    // Handle play/pause button click
                    botResponse.find('.gg-play-button-o').on('click', function () {
                        clearInterval(currentTypingEffect); // Stop typewriter effect
                        $(this).remove(); // Remove the play/pause button
                        isBotResponding = false; // Reset flag
                        messageInput.prop('disabled', false); // Enable input
                    });
                }
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
                // Enable input in case of error
                messageInput.prop('disabled', false);
                isBotResponding = false;
            },
            beforeSend: function () {
                // Set flag to indicate bot is responding
                isBotResponding = true;
            }
        });
    });

    function typeWriter(element, text, callback) {
        var i = 0;
        return setInterval(function () {
            if (i < text.length) {
                element.text(element.text() + text.charAt(i));
                i++;
            } else {
                clearInterval(currentTypingEffect);
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