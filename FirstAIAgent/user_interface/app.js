// Configure Webhook URL, should not change
const N8N_WEBHOOK_URL = "http://localhost:5680/webhook-test/agent";

// Initializing handles
const messagesEl = document.getElementById('messages');
const formEl = document.getElementById('chat-form');
const inputEl = document.getElementById('user-input');
const sendButtonEl = document.getElementById('send-button');
const statusEl = document.getElementById('status');

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
    container.classList.add('intent-button-row');

    const intents = [
        { label: "Plan an Event", color: "#3a6df0" },
        { label: "Set a Reminder", color: "#7a5df5" },
        { label: "Delete an Event", color: "#2aa79b" },
        { label: "Ask a Question", color: "#ff914d" }
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
    const intentButtons = createIntentButtons();

    addMessage(
        "assistant",
        `Hi! Welcome to the planning agent that can add and delete events on your Google Calendar, set reminders for you, and more! How can I assist you? \n \n`,
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

// Light mode / dark mode applier function
function applyThemeByTime() {
    const hour = new Date().getHours()
    const ifNight = hour >= 17.5 || hour <= 7.5

    if (ifNight) {
        document.body.classList.add("dark-mode")
    } else {
        document.body.classList.remove("dark-mode")
    }
}

// Apply theme on load/refresh
applyThemeByTime();

// Event listener trigger
formEl.addEventListener('submit', (event) => {
    event.preventDefault();

    const text = inputEl.value.trim();
    if (!text) return;

    inputEl.value = '';
    sendMessageToAgent(text);
});


