// main.js

// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatToggle = document.getElementById("chat-toggle");
    const chatWindow = document.getElementById("chat-window");
    const closeChat = document.getElementById("close-chat");
    const sendBtn = document.getElementById("send-btn");
    const userInput = document.getElementById("user-input");
    const chatBody = document.getElementById("chat-body");

    // Particle effect for send button
    sendBtn.addEventListener('mouseenter', function() {
        const particle = this.querySelector('.send-btn-particle');
        particle.style.transform = 'scale(2)';
    });

    sendBtn.addEventListener('mouseleave', function() {
        const particle = this.querySelector('.send-btn-particle');
        particle.style.transform = 'scale(0)';
    });

    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        const maxHeight = 100;
        const newHeight = Math.min(this.scrollHeight, maxHeight);
        this.style.height = newHeight + 'px';
        
        // Ensure chat body stays scrolled to bottom when input grows
        chatBody.scrollTo({
            top: chatBody.scrollHeight,
            behavior: 'smooth'
        });
    });

    chatToggle.addEventListener("click", function() {
        chatWindow.classList.toggle("show");
        if (chatWindow.classList.contains("show")) {
            userInput.focus();
            // Add particle effect to button
            this.classList.add("active");
        } else {
            this.classList.remove("active");
        }
    });

    closeChat.addEventListener("click", function() {
        chatWindow.classList.remove("show");
        chatToggle.classList.remove("active");
    });

    // Prevent empty messages
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;

        // Reset textarea height
        userInput.value = "";
        userInput.style.height = 'auto';

        // Add user message
        addMessage(message, "user");

        // Show typing indicator
        const typingIndicator = document.createElement("div");
        typingIndicator.className = "message ai typing";
        typingIndicator.innerHTML = `
            <div class="ai-message-wrapper">
                <img src="/static/images/ai.svg" alt="AI Avatar" class="avatar">
                <div class="typing-animation">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>
        `;
        chatBody.appendChild(typingIndicator);
        chatBody.scrollTop = chatBody.scrollHeight;

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: message })
            });
            const data = await response.json();

            // Remove typing indicator
            chatBody.removeChild(typingIndicator);
            
            if (data.response) {
                addMessage(data.response, "ai");
            } else {
                addMessage("I couldn't process that request.", "ai");
            }
        } catch (error) {
            chatBody.removeChild(typingIndicator);
            addMessage("I'm having trouble connecting to the server.", "ai");
            console.error("Error:", error);
        }
    }

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    function addMessage(message, sender) {
        const messageElement = document.createElement("div");
        messageElement.className = `message ${sender}`;
        
        const wrapper = document.createElement("div");
        wrapper.className = `${sender}-message-wrapper`;
        
        const content = document.createElement("div");
        content.className = "message-content";
        content.textContent = message;
        
        const avatar = document.createElement("img");
        avatar.className = "avatar";
        avatar.alt = `${sender} Avatar`;
        avatar.src = sender === "user" 
            ? "/static/images/person.svg" 
            : "/static/images/ai.jpg";

        if (sender === "user") {
            wrapper.appendChild(content);
            wrapper.appendChild(avatar);
        } else {
            wrapper.appendChild(avatar);
            wrapper.appendChild(content);
        }
        
        messageElement.appendChild(wrapper);
        chatBody.appendChild(messageElement);
        
        chatBody.scrollTo({
            top: chatBody.scrollHeight,
            behavior: 'smooth'
        });
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});

// Set animation delay for each letter in the animated name
document.addEventListener("DOMContentLoaded", function () {
    const nameContainer = document.getElementById("animated-name");
    if (nameContainer) {
        const letters = Array.from(nameContainer.children);
        letters.forEach((letter, index) => {
            letter.style.animationDelay = `${index * 0.2}s`;
        });
    }
});

// Typing effect for name using Typed.js
document.addEventListener("DOMContentLoaded", function () {
    if (typeof Typed !== "undefined") {
        let typed = new Typed("#typed-name", {
            strings: ["Akshat Gupta", "AI Engineer", "Deep Learning Enthusiast"],
            typeSpeed: 100,
            backSpeed: 60,
            backDelay: 2000,
            loop: true,
        });
    }
});

// --- Projects Slider Initialization ---
// This code initializes the Slick slider for the mobile projects container.
// Ensure that jQuery and Slick are loaded before this code runs.
$(document).ready(function(){
    // Check if the window width is less than 992px and if the mobile projects container exists.
    if (window.innerWidth < 992) {
        if ($('#projects-slider').length) {
            $('#projects-slider').slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                autoplay: true,
                autoplaySpeed: 3000,
                dots: true,
                arrows: false,
                infinite: true
            });
        }
    }
});
