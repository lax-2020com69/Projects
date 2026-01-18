const pads = document.querySelectorAll(".pad");
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playSound(freq) {
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();

  osc.type = "square";
  osc.frequency.value = freq;

  gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(
    0.001,
    audioCtx.currentTime + 0.3
  );

  osc.connect(gain);
  gain.connect(audioCtx.destination);

  osc.start();
  osc.stop(audioCtx.currentTime + 0.3);
}

function activatePad(pad) {
  pad.classList.add("active");
  setTimeout(() => pad.classList.remove("active"), 100);
}

pads.forEach(pad => {
  pad.addEventListener("click", () => {
    activatePad(pad);
    playSound(200 + Math.random() * 400);
  });
});

window.addEventListener("keydown", e => {
  const pad = document.querySelector(`.pad[data-key="${e.keyCode}"]`);
  if (!pad) return;
  activatePad(pad);
  playSound(200 + Math.random() * 400);
});
