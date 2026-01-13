// Simple in-memory file system
const files = {
  "index.html": {
    language: "html",
    content: `<!DOCTYPE html>
<html>
<head>
  <title>VS Code Clone</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>Hello World</h1>
  <script src="main.js"></script>
</body>
</html>`
  },
  "style.css": {
    language: "css",
    content: `body {
  background-color: #1e1e1e;
  color: white;
  font-family: sans-serif;
}`
  },
  "main.js": {
    language: "javascript",
    content: `
// Insert a friendly message into the page
document.body.insertAdjacentHTML('beforeend', '<p style="font-family: monospace; color: #007acc;">JavaScript is working! 🎉</p>');

// Log a welcoming message to the console
console.log("Hello! JavaScript is running smoothly.");
`
  }
};

let currentFile = "index.html";
let editor;
let currentTheme = "vs-dark";
let terminalVisible = false;

const terminalContainer = document.getElementById("terminal-container");
const editorElement = document.getElementById("editor");
const appElement = document.getElementById("app");

let commandHistory = [];
let historyIndex = -1;

// Load Monaco editor once
if (!window.monacoLoaded) {
  window.monacoLoaded = true;
  require.config({ paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@latest/min/vs" } });

  require(["vs/editor/editor.main"], () => {
    editor = monaco.editor.create(editorElement, {
      value: files[currentFile].content,
      language: files[currentFile].language,
      theme: currentTheme,
      automaticLayout: true
    });

    appElement.classList.add("dark-theme");
    document.body.classList.add("dark-theme");

    setupEventHandlers();
    renderPreview();
  });
}

function setupEventHandlers() {
  // File tabs and sidebar clicks
  document.querySelectorAll(".tab, #file-list li").forEach(el => {
    el.addEventListener("click", () => {
      const file = el.getAttribute("data-file");
      if (file === currentFile) return;

      // Save current content before switching
      files[currentFile].content = editor.getValue();

      // Update active UI states
      document.querySelector(".tab.active").classList.remove("active");
      document.querySelector(`.tab[data-file="${file}"]`).classList.add("active");

      document.querySelector("#file-list li.active").classList.remove("active");
      document.querySelector(`#file-list li[data-file="${file}"]`).classList.add("active");

      // Switch editor content and language
      currentFile = file;
      const { content, language } = files[file];
      editor.setValue(content);
      monaco.editor.setModelLanguage(editor.getModel(), language);

      renderPreview();
    });
  });

  // Theme toggle button
  document.getElementById("toggle-theme").addEventListener("click", () => {
    if (currentTheme === "vs-dark") {
      currentTheme = "vs-light";
      monaco.editor.setTheme(currentTheme);
      appElement.classList.replace("dark-theme", "light-theme");
      document.body.classList.replace("dark-theme", "light-theme");
    } else {
      currentTheme = "vs-dark";
      monaco.editor.setTheme(currentTheme);
      appElement.classList.replace("light-theme", "dark-theme");
      document.body.classList.replace("light-theme", "dark-theme");
    }
  });

  // Terminal toggle button
  document.getElementById("open-terminal").addEventListener("click", () => {
    terminalVisible = !terminalVisible;

    if (terminalVisible) {
      terminalContainer.style.display = "block";
      editorElement.style.flex = "1 0 calc(100% - 200px)"; // adjusted height for terminal
      if (!terminalContainer.querySelector(".input-line")) appendPrompt();

      // Hide live preview when terminal is open
      const preview = document.getElementById("live-preview");
      if (preview) preview.style.display = "none";

    } else {
      terminalContainer.style.display = "none";
      editorElement.style.flex = "1";

      // Show and update live preview when terminal is closed
      const preview = document.getElementById("live-preview");
      if (preview) preview.style.display = "block";

      renderPreview();
    }
  });

  // Update preview on editor content change
  editor.onDidChangeModelContent(() => {
    files[currentFile].content = editor.getValue();
    renderPreview();
  });
}

// === Terminal logic ===

const PROMPT = "$ ";
const startTime = Date.now();

const commands = {
  help: `
Available commands:
help         - Show this help message
clear        - Clear the terminal output
echo [text]  - Print the provided text
date         - Show current date/time
about        - About this dummy terminal
ls           - List files
cat [file]   - Show file content
pwd          - Fake path
whoami       - User name
js [code]    - Run JavaScript
math [expr]  - Evaluate math expression
uptime       - Show fake uptime
exit         - Hide terminal
`,

  clear: () => {
    terminalContainer.innerHTML = "";
  },

  echo: args => args.join(" "),

  date: () => new Date().toString(),

  about: "This is a dummy terminal simulating VS Code's terminal.",

  ls: () => Object.keys(files).join("\n"),

  cat: args => {
    if (!args.length) return "Specify a file name.";
    const file = args[0];
    return files[file] ? files[file].content : `File not found: ${file}`;
  },

  pwd: () => "/home/user",

  whoami: () => "user",

  js: args => {
    try {
      const result = eval(args.join(" "));
      return String(result);
    } catch (e) {
      return `JS Error: ${e.message}`;
    }
  },

  math: args => {
    try {
      const result = eval(args.join(" "));
      return String(result);
    } catch (e) {
      return `Math Error: ${e.message}`;
    }
  },

  uptime: () => {
    const seconds = Math.floor((Date.now() - startTime) / 1000);
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `Uptime: ${h}h ${m}m ${s}s`;
  },

  exit: () => {
    terminalContainer.style.display = "none";
    editorElement.style.flex = "1";
    terminalVisible = false;

    const preview = document.getElementById("live-preview");
    if (preview) preview.style.display = "block";
    renderPreview();

    return "Terminal closed.";
  }
};

function appendLine(text, className = "output-line") {
  const line = document.createElement("div");
  line.textContent = text;
  line.className = className;
  terminalContainer.appendChild(line);
  terminalContainer.scrollTop = terminalContainer.scrollHeight;
}

function appendPrompt() {
  const line = document.createElement("div");

  const promptSpan = document.createElement("span");
  promptSpan.className = "prompt";
  promptSpan.textContent = PROMPT;

  const inputSpan = document.createElement("span");
  inputSpan.className = "input-line";
  inputSpan.contentEditable = true;
  inputSpan.spellcheck = false;

  line.appendChild(promptSpan);
  line.appendChild(inputSpan);
  terminalContainer.appendChild(line);

  inputSpan.focus();

  // Only add click listener once on terminalContainer to focus input
  if (!terminalContainer._hasClickListener) {
    terminalContainer.addEventListener("click", e => {
      const inputLine = terminalContainer.querySelector(".input-line");
      if (inputLine && !inputLine.contains(e.target)) {
        inputLine.focus();
        e.preventDefault();
      }
    });
    terminalContainer._hasClickListener = true;
  }

  inputSpan.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      e.preventDefault();
      const input = inputSpan.textContent.trim();
      runCommand(input);
      commandHistory.push(input);
      historyIndex = commandHistory.length;
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      if (commandHistory.length === 0) return;
      historyIndex = Math.max(0, historyIndex - 1);
      inputSpan.textContent = commandHistory[historyIndex];
      placeCaretAtEnd(inputSpan);
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      if (commandHistory.length === 0) return;
      historyIndex = Math.min(commandHistory.length, historyIndex + 1);
      if (historyIndex === commandHistory.length) {
        inputSpan.textContent = "";
      } else {
        inputSpan.textContent = commandHistory[historyIndex];
      }
      placeCaretAtEnd(inputSpan);
    }
  });
}

// Helper to put cursor at end of contenteditable span
function placeCaretAtEnd(el) {
  el.focus();
  if (typeof window.getSelection != "undefined" && typeof document.createRange != "undefined") {
    const range = document.createRange();
    range.selectNodeContents(el);
    range.collapse(false);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }
}

function runCommand(input) {
  const lastLine = terminalContainer.lastChild;
  const inputSpan = lastLine.querySelector(".input-line");
  inputSpan.contentEditable = false;

  if (!input) {
    appendPrompt();
    return;
  }

  const args = input.split(" ");
  const cmd = args.shift().toLowerCase();

  if (commands[cmd]) {
    const result = typeof commands[cmd] === "function" ? commands[cmd](args) : commands[cmd];
    if (result !== undefined) appendLine(result);
  } else {
    appendLine(`Command not found: ${cmd}`);
  }

  appendPrompt();
}

// === Live Output Preview ===
function renderPreview() {
  let iframe = document.getElementById("live-preview");
  if (!iframe) {
    iframe = document.createElement("iframe");
    iframe.id = "live-preview";
    iframe.style.height = "200px";
    iframe.style.width = "100%";
    iframe.style.border = "1px solid #555";
    iframe.style.marginTop = "10px";
    editorElement.parentNode.appendChild(iframe);
  }

  // Compose HTML content from files
  let html = files["index.html"].content;
  // Replace style.css link with style tag
  html = html.replace(
    /<link\s+rel=["']stylesheet["']\s+href=["']style\.css["']\s*\/?>/i,
    `<style>${files["style.css"].content}</style>`
  );

  // Replace main.js script tag with inline script
  html = html.replace(
    /<script\s+src=["']main\.js["']\s*><\/script>/i,
    `<script>${files["main.js"].content}</script>`
  );

  // Write to iframe document
  const doc = iframe.contentDocument || iframe.contentWindow.document;
  doc.open();
  doc.write(html);
  doc.close();
}

// Optional: Save current file content on page unload
window.addEventListener("beforeunload", () => {
  if (editor) {
    files[currentFile].content = editor.getValue();
  }
});
