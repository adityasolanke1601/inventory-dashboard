function openModal() {
  document.getElementById("modalOverlay").classList.add("open");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  document.getElementById("modalOverlay").classList.remove("open");
  document.body.style.overflow = "";
}

function filterTable() {
  const q = document.getElementById("searchInput").value.toLowerCase();
  const rows = document.querySelectorAll("#inventoryTable tbody tr");
  rows.forEach(row => {
    const text = row.textContent.toLowerCase();
    row.style.display = text.includes(q) ? "" : "none";
  });
}

document.addEventListener("keydown", e => {
  if (e.key === "Escape") closeModal();
});

document.querySelectorAll(".nav-item[href^='#']").forEach(link => {
  link.addEventListener("click", function(e) {
    document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));
    this.classList.add("active");
  });
});

window.addEventListener("scroll", () => {
  const sections = ["dashboard", "inventory", "alerts"];
  sections.forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    const rect = el.getBoundingClientRect();
    if (rect.top <= 120 && rect.bottom > 0) {
      document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));
      const navLink = document.querySelector(`.nav-item[href="#${id}"]`);
      if (navLink) navLink.classList.add("active");
    }
  });
});
