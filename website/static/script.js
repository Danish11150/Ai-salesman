document.addEventListener("DOMContentLoaded", () => {

    // ===== LOGIN FORM VALIDATION =====
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", (e) => {
            const email = form.email.value.trim();
            const password = form.password.value.trim();

            if (!email || !password) {
                e.preventDefault();
                alert("Please fill in both fields!");
            }
        });
    }

    // ===== SIDE MENU TOGGLE =====
    const menu = document.getElementById("sideMenu");
    const icon = document.querySelector(".menu-icon");

    if (icon && menu) {
        icon.addEventListener("click", () => {
            menu.style.width = menu.style.width === "250px" ? "0" : "250px";
        });

        document.addEventListener("click", (event) => {
            if (!menu.contains(event.target) && !icon.contains(event.target)) {
                menu.style.width = "0";
            }
        });
    }

    // ===== THEME TOGGLE =====
    const toggle = document.getElementById("themeToggle");

    if (toggle) {
        // Load saved theme
        const saved = localStorage.getItem("theme") || "light";
        document.documentElement.setAttribute("data-theme", saved);
        toggle.textContent = saved === "dark" ? "🌞" : "🌙";

        // Toggle theme on click
        toggle.addEventListener("click", () => {
            const current = document.documentElement.getAttribute("data-theme");
            const newTheme = current === "dark" ? "light" : "dark";

            document.documentElement.setAttribute("data-theme", newTheme);
            toggle.textContent = newTheme === "dark" ? "🌞" : "🌙";
            localStorage.setItem("theme", newTheme);
        });
    }

});
