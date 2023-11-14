const body = document.querySelector("body"),
  sidebar = body.querySelector("nav"),
  toggle = body.querySelector(".toggle"),
  searchBtn = body.querySelector(".search-box"),
  modeSwitch = body.querySelector(".toggle-switch"),
  modeText = body.querySelector(".mode-text");

toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
  toggleImageVisibility();
});

searchBtn.addEventListener("click", () => {
  sidebar.classList.remove("close");
  toggleImageVisibility();
});

function toggleDarkMode() {
  const body = document.querySelector("body");
  const sidebar = document.querySelector(".sidebar");
  const images = document.querySelectorAll(".nav-link img");

  body.classList.toggle("dark");
  sidebar.classList.toggle("dark-sidebar");

  // Change image color and background based on dark mode
  if (body.classList.contains("dark")) {
    images.forEach((img) => {
      img.style.filter = "invert(100%)";
      img.parentNode.style.backgroundColor = "#242526";
    });
  } else {
    images.forEach((img) => {
      img.style.filter = "invert(0%)";
      img.parentNode.style.backgroundColor = "transparent";
    });
  }
}

const darkModeSwitch = document.querySelector(".toggle-switch");
darkModeSwitch.addEventListener("click", toggleDarkMode);


