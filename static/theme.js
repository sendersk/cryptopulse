const toggleButton = document.getElementById('theme-toggle');
const body = document.body;

// Load saved theme from localStorage
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
  body.classList.add('light-mode');
  toggleButton.textContent = '☀️ Light Mode';
}

// Toggle between dark and light mode
toggleButton.addEventListener('click', () => {
  body.classList.toggle('light-mode');
  const isLight = body.classList.contains('light-mode');

  toggleButton.textContent = isLight ? '☀️ Light Mode' : '🌙 Dark Mode';
  localStorage.setItem('theme', isLight ? 'light' : 'dark');
});
