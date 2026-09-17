document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert').forEach((el) => setTimeout(() => { el.classList.add('fade-out'); setTimeout(() => el.remove(), 400); }, 4200));
});
