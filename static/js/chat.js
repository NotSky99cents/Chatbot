const form = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatMessages = document.getElementById('chat-messages');

form.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const message = userInput.value.trim();
    
    if (message !== '') {
        // Send user input to the server
        sendMessage(message);
        
        // Display the user's message in the chat interface
        displayMessage(message, 'user');
        
        // Clear the input field
        userInput.value = '';
    }
});

function sendMessage(message) {
    // Send an AJAX request to the server
    fetch('/chatbot/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for Django
        },
        body: 'user_input=' + encodeURIComponent(message)
    })
    .then(response => response.json())
    .then(data => {
        const botResponse = data.response;
        
        // Display the bot's response in the chat interface
        displayMessage(botResponse, 'bot');
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message ' + sender;
    messageElement.innerText = message;
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}