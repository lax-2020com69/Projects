function toggleChatbox() {
  const chatWidget = document.getElementById("chat-widget");
  const chatBox = document.getElementById("chat-box");

  if (chatWidget.style.display === "flex") {
    chatWidget.style.display = "none";
  } else {
    chatWidget.style.display = "flex";

    // முதன்முறை திறக்கும் போது தானாக வணக்கம் கூறும்
    if (!chatBox.hasChildNodes()) {
      setTimeout(() => {
        appendMessage("bot", "👋 வணக்கம்! நான் விவசாய உதவியாளர். தொடங்க 'உதவி' என தட்டச்சு செய்யவும் அல்லது பயிர்கள், பூச்சிகள், உரங்கள் பற்றி கேளுங்கள்.");
      }, 300);
    }
  }
}

// Enter விசையை அழுத்தும் போது செய்தி அனுப்பு
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
