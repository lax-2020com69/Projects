function toggleChatbox() {
  const chatWidget = document.getElementById("chat-widget");
  const chatBox = document.getElementById("chat-box");

  if (chatWidget.style.display === "flex") {
    chatWidget.style.display = "none";
  } else {
    chatWidget.style.display = "flex";

    // Auto greet if first time opened
    if (!chatBox.hasChildNodes()) {
      setTimeout(() => {
        appendMessage("bot", "👋 Hi! I'm AgriBot. Type `help` to get started or ask me about crops, pests, or fertilizers.");
      }, 300);
    }
  }
}

// Send message on Enter key
document.addEventListener("DOMContentLoaded", () => {
  const inputField = document.getElementById("user-input");
  inputField.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});

async function sendMessage() {
  const input = document.getElementById("user-input");
  const text = input.value.trim();
  if (!text) return;

  appendMessage("user", text);
  input.value = "";

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  });

  const data = await res.json();
  appendMessage("bot", data.response);
}

function appendMessage(sender, text) {
  const chatBox = document.getElementById("chat-box");

  const message = document.createElement("div");
  message.className = `message ${sender}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = sender === "user" ? "👤" : "🤖";

  const bubble = document.createElement("div");
  bubble.className = "text";
  bubble.textContent = text;

  message.appendChild(avatar);
  message.appendChild(bubble);
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;
}
