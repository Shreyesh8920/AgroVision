const input = document.querySelector('.chat-input');
const sendBtn = document.querySelector('.send-btn');
const voiceBtn = document.querySelector('.voice-btn');
const chatContainer = document.querySelector('.chat-container');
const clearBtn = document.querySelector('.icon-btn');
const chatContent = document.querySelector('.chat-content');
const DEFAULT_PLACEHOLDER = input.placeholder;



let sessionId = null;
const MIN_HEIGHT = 28;
const MAX_HEIGHT = 120;
//mic speech recog.
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

let recognition = null;

if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.lang = 'hi-IN';   
  recognition.interimResults = false;
  recognition.continuous = false;
}


//Auto-grow textarea
function autoGrow() {
  input.style.height = 'auto';

  const newHeight = Math.min(
    Math.max(input.scrollHeight, MIN_HEIGHT),
    MAX_HEIGHT
  );

  input.style.height = newHeight + 'px';
  input.style.overflowY =
    input.scrollHeight > MAX_HEIGHT ? 'auto' : 'hidden';
}

//Toggle mic to send button
function toggleSendButton() {
  const hasText = input.value.trim().length > 0;

  if (hasText) {
    sendBtn.style.display = 'flex';
    voiceBtn.style.display = 'none';
  } else {
    sendBtn.style.display = 'none';
    voiceBtn.style.display = 'flex';
  }
}

/* Send message */
function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  chatContainer.classList.add('chat-active');
  const chatMessages = document.querySelector('.chat-messages');

  // user msg
  const userDiv = document.createElement('div');
  userDiv.className = 'message user';
  userDiv.innerHTML = `
    <div class="message-avatar">
      <svg viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10"/>
        <path d="M9 12l2 2 4-4"/>
      </svg>
    </div>
    <div class="message-bubble"></div>
  `;
  userDiv.querySelector('.message-bubble').textContent = text;
  chatMessages.appendChild(userDiv);



  // ai msg typing
  const typingDiv = document.createElement('div');
  typingDiv.className = 'message ai';
  typingDiv.innerHTML = `
    <div class="message-avatar">
      <svg viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10"/>
        <path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/>
      </svg>
    </div>
    <div class="message-bubble">Typing…</div>
  `;
  chatMessages.appendChild(typingDiv);

  chatContent.scrollTop = chatContent.scrollHeight;

  fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: text,
      session_id: sessionId
    })
  })
    .then(res => res.json())
    .then(data => {
      typingDiv.remove();

      sessionId = data.session_id || sessionId;

      // ai reply msg
      const aiDiv = document.createElement('div');
      aiDiv.className = 'message ai';
      aiDiv.innerHTML = `
        <div class="message-avatar">
          <svg viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10"/>
            <path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/>
          </svg>
        </div>
        <div class="message-bubble"></div>
      `;
      aiDiv.querySelector('.message-bubble').innerHTML = marked.parse(data.reply || "No response from AI. Try again.");
      chatMessages.appendChild(aiDiv);
      chatContent.scrollTop = chatContent.scrollHeight;
    })
    .catch(err => {
      typingDiv.remove();

      const errorDiv = document.createElement('div');
      errorDiv.className = 'message ai';
      errorDiv.innerHTML = `
        <div class="message-avatar">
          <svg viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10"/>
            <path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/>
          </svg>
        </div>
        <div class="message-bubble">
          Error contacting server. Try again.
        </div>
      `;
      chatMessages.appendChild(errorDiv);
      chatContent.scrollTop = chatContent.scrollHeight;
      console.error(err);
    });

  input.value = '';
  autoGrow();
  toggleSendButton();
  input.focus();
}


/* Events */
input.addEventListener('input', () => {
  autoGrow();
  toggleSendButton();
});

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

sendBtn.addEventListener('click', sendMessage);
let isListening = false;

voiceBtn.addEventListener('click', () => {
  if (!recognition) {
    alert('Mic not supported');
    return;
  }

  if (!isListening) {
    //listning start
    recognition.abort();
    recognition.start();

    isListening = true;
    voiceBtn.classList.add('listening');
    input.placeholder = 'Listening…';
    
  } else {
    //listning stop
    recognition.stop();

    isListening = false;
    voiceBtn.classList.remove('listening');
  }
});

//mic result handling
if (recognition) {
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;

    input.value = transcript;
    autoGrow();
    toggleSendButton();
    input.focus();
    recognition.stop();
    voiceBtn.classList.remove('listening');
  };

  recognition.onerror = (event) => {
    isListening = false;
    voiceBtn.classList.remove('listening');
    console.error('Mic error:', event.error);
    input.placeholder = DEFAULT_PLACEHOLDER;
    
  };
  recognition.onend = () => {
    isListening = false;
    voiceBtn.classList.remove('listening');
    input.placeholder = DEFAULT_PLACEHOLDER;
    
  };

}

autoGrow();
toggleSendButton();

clearBtn.addEventListener('click', () => {
  // UI reset
  document.querySelector('.chat-messages').innerHTML = '';
  chatContainer.classList.remove('chat-active');

  // Backend reset
  if (sessionId) {
    fetch('/api/clear', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId })
    });
  }

  sessionId = null;
});