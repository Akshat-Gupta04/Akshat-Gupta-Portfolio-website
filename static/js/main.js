// main.js

// Toggle chat window visibility
document.getElementById("chat-toggle").addEventListener("click", function () {
    var chatWindow = document.getElementById("chat-window");
    if (chatWindow.style.display === "flex") {
        chatWindow.style.display = "none";
    } else {
        chatWindow.style.display = "flex";
    }
});

// Close chat window
document.getElementById("close-chat").addEventListener("click", function () {
    document.getElementById("chat-window").style.display = "none";
});

// Handle sending message
document.getElementById("send-btn").addEventListener("click", async function () {
    var userInput = document.getElementById("user-input").value;
    if (userInput.trim() !== "") {
        // Show user message
        addMessage(userInput, "user");

        // Clear input field
        document.getElementById("user-input").value = "";

        // Show loading AI message
        addMessage("Thinking...", "ai");

        try {
            // Send user input to the backend using fetch
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: userInput })
            });

            const data = await response.json();
            if (data.response) {
                // Display AI response
                updateAIResponse(data.response);
            } else {
                updateAIResponse("Sorry, I couldn't understand that.");
            }
        } catch (error) {
            updateAIResponse("Sorry, I'm having trouble connecting to the server.");
        }
    }
});

// Add user or AI message to the chat
function addMessage(message, sender) {
    var chatBody = document.getElementById("chat-body");
    var messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.textContent = message;
    chatBody.appendChild(messageElement);
    chatBody.scrollTop = chatBody.scrollHeight; // Scroll to bottom
}

// Update AI response message
function updateAIResponse(message) {
    var chatBody = document.getElementById("chat-body");
    var aiMessageElement = chatBody.querySelector(".message.ai");
    if (aiMessageElement) {
        aiMessageElement.textContent = message;
    }
}

// Optional: Handle "Enter" key for sending messages
document.getElementById("user-input").addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        document.getElementById("send-btn").click();
    }
    document.addEventListener("DOMContentLoaded", function () {
        const nameContainer = document.getElementById("animated-name");
        const letters = Array.from(nameContainer.children);
    
        letters.forEach((letter, index) => {
            letter.style.animationDelay = `${index * 0.2}s`; // Adjust delay dynamically
        });
    });
});