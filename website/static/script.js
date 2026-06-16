// Simple login form validation
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  form.addEventListener("submit", (e) => {
    const email = form.email.value.trim();
    const password = form.password.value.trim();

    if (!email || !password) {
      e.preventDefault();
      alert("Please fill in both fields!");
    }
  });
});

function toggleMenu() {
    let menu = document.getElementById("sideMenu");
    if (menu.style.width === "250px") {
        menu.style.width = "0";
    } else {
        menu.style.width = "250px";
    }
}

document.addEventListener("click", function(event) {
    const menu = document.getElementById("sideMenu");
    const icon = document.querySelector(".menu-icon");

    if (!menu.contains(event.target) && !icon.contains(event.target)) {
        menu.style.width = "0";
    }
});

const toggle = document.getElementById("themeToggle");

toggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    const newTheme = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", newTheme);
    toggle.textContent = newTheme === "dark" ? "🌞" : "🌙";
    localStorage.setItem("theme", newTheme);
});

// Load saved theme
const saved = localStorage.getItem("theme") || "light";
document.documentElement.setAttribute("data-theme", saved);
toggle.textContent = saved === "dark" ? "🌞" : "🌙";
