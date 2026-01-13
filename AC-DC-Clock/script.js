function updateClock() {
  const now = new Date();

  const hour = now.getHours();
  const minute = now.getMinutes();
  const second = now.getSeconds();

  const hourDeg = ((hour % 12) + minute / 60) * 30;
  const minuteDeg = (minute + second / 60) * 6;
  const secondDeg = second * 6;

  // No translateX needed
  document.querySelector('.hour-hand').style.transform = `rotate(${hourDeg}deg)`;
  document.querySelector('.minute-hand').style.transform = `rotate(${minuteDeg}deg)`;
  document.querySelector('.second-hand').style.transform = `rotate(${secondDeg}deg)`;

  // Digital time
  const ampm = hour >= 12 ? 'PM' : 'AM';
  const displayHour = (hour % 12 || 12).toString().padStart(2, '0');
  const displayMinute = minute.toString().padStart(2, '0');
  const displaySecond = second.toString().padStart(2, '0');
  const timeString = `${displayHour}:${displayMinute}:${displaySecond} ${ampm}`;
  document.getElementById('digital-time').textContent = timeString;

  // Day and Date
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const day = days[now.getDay()];
  const date = `${now.getDate().toString().padStart(2, '0')}/${(now.getMonth() + 1).toString().padStart(2, '0')}/${now.getFullYear().toString().slice(-2)}`;
  
  document.getElementById('day').textContent = day;
  document.getElementById('date').textContent = date;
}

setInterval(updateClock, 1000);
updateClock();
