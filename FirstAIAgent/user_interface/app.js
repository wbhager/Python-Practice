// Configure Webhook URL, should not change
const N8N_WEBHOOK_URL = "http://localhost:5680/webhook-test/agent";

// Initializing handles
const messagesEl = document.getElementById('messages');
const formEl = document.getElementById('chat-form');
const inputEl = document.getElementById('user-input');
const sendButtonEl = document.getElementById('send-button');
const statusEl = document.getElementById('status');

// Add-messages-to-message-box function
function addMessage(role, text) {
    const row = document.createElement('div');
    row.classList.add('message-row', role);

    const bubble = document.createElement('div');
    bubble.classList.add('message-bubble');
    bubble.textContent = text;

    row.appendChild(bubble);
    messagesEl.appendChild(row);

    messagesEl.scrollTop = messagesEl.scrollHeight;
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

// Event listener trigger
formEl.addEventListener('submit', (event) => {
    event.preventDefault();

    const text = inputEl.value.trim();
    if (!text) return;

    inputEl.value = '';
    sendMessageToAgent(text);
});


