// Configure Webhook URL, should not change
const N8N_WEBHOOK_URL = "http://localhost:5680/webhook-test/agent";

// Initializing handles
const messagesEl = document.getElementById('messages');
const formEl = document.getElementById('chat-form');
const inputEl = document.getElementById('user-input');
const sendButtonEl = document.getElementById('send-button');
const statusEl = document.getElementById('status');
const chatContainerEl = document.querySelector('.chat-container');


// Add-messages-to-message-box function and message fade-in animation
function addMessage(role, text, extraContent = null) {
    const row = document.createElement('div');
    row.classList.add('message-row', role);

    // Creating the bubble
    const bubble = document.createElement('div');
    bubble.classList.add('message-bubble');
    bubble.textContent = text;

    // If there is extra content (for now, just the first message where we also supply intent buttons
    if (extraContent) {
        bubble.appendChild(extraContent);
    }

    // ⭐ Star button
    const starbutton = document.createElement('span');
    starbutton.classList.add('star-button');
    starbutton.textContent = '☆'; // outline star

    starbutton.onclick = () => {
        const starred = row.classList.toggle('starred');
        starbutton.textContent = starred ? '⭐' : '☆';
        saveStarredMessage(row.dataset.messageId);
    };

    // Initializing the copy container to contain the icon and the label
    const copyContainer = document.createElement('div');
    copyContainer.classList.add('copy-container');

    // Creating the copy button
    const copyButton = document.createElement('button');
    copyButton.classList.add('copy-button');
    copyButton.textContent = "⧉";

    // Creating the copy label
    const copyLabel = document.createElement('span');
    copyLabel.classList.add('copy-label');
    copyLabel.textContent = "Copy";

    // Building the copy container
    copyContainer.appendChild(copyButton);
    copyContainer.appendChild(copyLabel);

    // Appending the copy container to be inside the bubble, adding bubble to row, row to chat container
    bubble.appendChild(copyContainer);
    row.appendChild(bubble);
    row.appendChild(starbutton);
    messagesEl.appendChild(row);

    // Enacting copying behavior
    copyButton.onclick = () => {
        navigator.clipboard.writeText(text);
    };

    // Fade-in animation for text
    requestAnimationFrame(() => {
        row.classList.add('show');
    });

    messagesEl.scrollTop = messagesEl.scrollHeight;
};

// Creating a function that can build intent buttons
function createIntentButtons() {
    const container = document.createElement('div');
    container.classList.add('intent-btn-row');

    const intents = [
        { label: "Plan an Event", color: "#3a6df0" },
        { label: "Read Upcoming Events", color: "#4b0082"},
        { label: "Set a Reminder", color: "#7a5df5" },
        { label: "Delete an Event", color: "#2aa79b" },
        { label: "Update an Event", color: "#014D4E"},
        { label: "Get Schedule Advice", color: "#C15D1A" },
        { label: "Ask a Question", color: "#5DA9E9" }
    ];

    intents.forEach(intent => {
        const btn = document.createElement('button');
        btn.classList.add('intent-btn');
        btn.textContent = intent.label;
        btn.style.background = intent.color;

        btn.addEventListener('click', () => {
            sendMessageToAgent(`I would like to ${intent.label.toLowerCase()}.`);
        });

        container.appendChild(btn);
    });

    return container;
}

// Automatically sending the welcome message on page load
window.addEventListener("DOMContentLoaded", () => {

    // Reapply dark-mode / light-mode
    loadTheme();
    
    const intentButtons = createIntentButtons();

    addMessage(
        "assistant",
        `Hi! I’m your planning agent. I can add, update, and delete events on your Google Calendar, review your schedule, and suggest the best times to plan new events. What would you like to do? \n \n`,
        intentButtons
    );
});

// Adding speech-to-text functionality
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US';

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById('user-input').value = transcript;

};

function startListening() {
    recognition.start();
}

// Update current UI state
function setLoading(isLoading) {
    if (isLoading) {
        statusEl.textContent = 'Sending message to agent... Please wait just a moment...';
        sendButtonEl.disabled = true;
        inputEl.disabled = true;
    }

    else {
        statusEl.textContent = '';
        sendButtonEl.disabled = false;
        inputEl.disabled = false;
        inputEl.focus()
    }
}

// Send-message-to-n8n-webhook-so-Claude-can-read-it and receiver-of-Claudes-answer asynchronous function
async function sendMessageToAgent(userMessage) {
    addMessage('user', userMessage);
    setLoading(true);

    try {
        const requestBody = {
            message: userMessage,
        };

        //starts 
        const response = await fetch(N8N_WEBHOOK_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error from n8n: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        const assistantText = data.reply;
        addMessage('assistant', assistantText);
    }
    
    catch (error) {
        console.error('Error with communicating with agent: ', error);
        statusEl.textContent = 'Error contacting agent';
    }

    finally {
        setLoading(false);
    }
}


// Restarting chat button action
document.getElementById("restart-chat-button").addEventListener("click", () => {
    messagesEl.innerHTML = "";

    // Reapply dark-mode / light-mode
    loadTheme();

    const intentButtons = createIntentButtons();

    addMessage(
        "assistant",
        "Hi! Welcome to the planning agent that can add and delete events on your Google Calendar, set reminders for you, and more! How can I assist you? \n \n",
        intentButtons
    );

    messagesEl.scrollTop = 0;
});

// Jumping-back-to-top button action
document.getElementById("jump-to-top-button").addEventListener("click", () => {
    chatContainerEl.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});

// Scroll-to-bottom button action
document.getElementById("scroll-bottom-button").addEventListener("click", () => {
    chatContainerEl.scrollTo({
        top: chatContainerEl.scrollHeight,
        behavior: "smooth"
    });
});

// Light mode / dark mode applier function
function applyTheme(selectedMode) {
    let mode = selectedMode;

    // Save user preference
    localStorage.setItem("theme-preference", mode);

    if (mode === "auto") {
        const hour = new Date().getHours();
        const isNight = hour >= 17.5 || hour <= 10.5;
        mode = isNight ? "dark" : "light";
    }

    // Apply to body
    if (mode === "dark") {
        document.body.classList.add("dark-mode");
    } else {
        document.body.classList.remove("dark-mode");
    }

    // Reflect in dropdown UI (if present)
    const themeSelect = document.getElementById("theme-select");
    if (themeSelect && themeSelect.value !== selectedMode) {
        themeSelect.value = selectedMode;
    }
}

// Load user preference or default to auto
function loadTheme() {
    const saved = localStorage.getItem("theme-preference") || "auto";
    applyTheme(saved);
}

loadTheme();


const themeSelectEl = document.getElementById("theme-select");

if (themeSelectEl) {
    themeSelectEl.addEventListener("change", (event) => {
        const value = event.target.value;
        applyTheme(value);
    });
}

// Allowing for shift-clicking to send the message
inputEl.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();   
        formEl.requestSubmit();     
    }
});

// Event listener trigger
formEl.addEventListener('submit', (event) => {
    event.preventDefault();

    const text = inputEl.value.trim();
    if (!text) return;

    inputEl.value = '';
    sendMessageToAgent(text);
});


