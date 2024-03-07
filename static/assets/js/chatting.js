
$(document).ready(function () {
    $('form').on('submit', function (event) {
        event.preventDefault();
        var messageInput = $('#message');
        var chatlogContainer = $('#chatlog');
        var botImage = "{% static 'assets/images/icons/pro1.png' %}";
        var userImage = "{% static 'assets/images/icons/profile.png' %}";
        var personName = "Kristin Williams";

        var userMessage = messageInput.val();

        var userMessageHtml = `
            <div class="msg user-msg">
                <div class="msg-bubble">
                    <div class="msg-text">${userMessage}</div>
                </div>
            </div>
        `;

        chatlogContainer.append(userMessageHtml);
        chatlogContainer.append('<div class="msg bot-msg typing"><p><strong>BOT:</strong> Thinking</p></div>');
        messageInput.val('');

        $.ajax({
            type: 'POST',
            url: '{% url "chat" %}',
            data: {
                'message': userMessage,
                'csrfmiddlewaretoken': '{% csrf_token %}'
            },
            success: function (data) {
                chatlogContainer.find('.typing').remove();

                var botResponse = `
                    <div class="msg bot-msg">
                        <div class="msg-bubble">
                            <div class="msg-text">${data.message}</div>
                        </div>
                    </div>
                `;
                chatlogContainer.append(botResponse);

                chatlogContainer.animate({ scrollTop: chatlogContainer[0].scrollHeight });
            },
            error: function (xhr, status, error) {
                console.log("Error: " + error);
            }
        });
    });
});