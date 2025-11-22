const API = "http://127.0.0.1:8000";

let sessionId = null;
let recognition = null;
let isListening = false;

// DOM Elements
const chatWindow = document.getElementById("chatWindow");
const userInput = document.getElementById("userInput");
const micBtn = document.getElementById("micBtn");
const statusText = document.getElementById("statusText");

// Create message
function addMessage(text, sender) {
  let div = document.createElement("div");
  div.className = `message ${sender}`;
  div.textContent = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Speak bot message
function speak(text) {
  const utter = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(utter);
}

// Start speech recognition
function initVoice() {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    statusText.textContent = "Voice not supported";
    return;
  }

  recognition = new SpeechRecognition();
  recognition.lang = "en-US";

  recognition.onstart = () => {
    isListening = true;
    micBtn.classList.add("active");
    statusText.textContent = "Listening...";
  };

  recognition.onend = () => {
    isListening = false;
    micBtn.classList.remove("active");
    statusText.textContent = "";
  };

  recognition.onresult = (event) => {
    userInput.value = event.results[0][0].transcript;
  };
}

micBtn.onclick = () => {
  if (!recognition) return;
  if (isListening) recognition.stop();
  else recognition.start();
};

// ----------------------- API CALLS -----------------------

document.getElementById("startBtn").onclick = async () => {
  const role = document.getElementById("role").value;
  const level = document.getElementById("level").value;
  const mode = document.getElementById("mode").value;

  const res = await fetch(`${API}/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role, level, mode }),
  });

  const data = await res.json();
  sessionId = data.sessionId;

  chatWindow.innerHTML = "";
  addMessage(data.botMessage, "bot");
  speak(data.botMessage);

  statusText.textContent = `Interview started for ${role} (${level})`;
};

document.getElementById("sendBtn").onclick = sendMessage;

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";

  const res = await fetch(`${API}/message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sessionId, userMessage: text }),
  });

  const data = await res.json();
  addMessage(data.botMessage, "bot");
  speak(data.botMessage);
}

document.getElementById("finishBtn").onclick = async () => {
  const res = await fetch(`${API}/finish`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sessionId }),
  });

  const data = await res.json();

  addMessage("Interview completed. Showing feedback below.", "bot");
  speak("Your interview feedback is ready!");

  document.getElementById("feedbackSection").style.display = "block";

  document.getElementById("feedbackIntro").textContent = data.botMessage;

  const strengths = document.getElementById("strengthsList");
  const areas = document.getElementById("areasList");
  const tips = document.getElementById("tipsList");

  strengths.innerHTML = "";
  data.summary.strengths.forEach(
    (s) => (strengths.innerHTML += `<li>${s}</li>`)
  );

  areas.innerHTML = "";
  data.summary.areasToImprove.forEach(
    (a) => (areas.innerHTML += `<li>${a}</li>`)
  );

  tips.innerHTML = "";
  data.summary.tips.forEach((t) => (tips.innerHTML += `<li>${t}</li>`));

  document.getElementById("ratingValue").textContent =
    data.summary.overallRating.toFixed(1);
};

// Initialize voice
initVoice();
