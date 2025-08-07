// Selettori DOM per il toggle e il body
const toggle = document.getElementById("dark-mode-toggle");
const html = document.documentElement;

// Recupera la modalità salvata dal localStorage
const savedMode = localStorage.getItem("dark-mode");

// ========== INIZIALIZZAZIONE MODALITÀ ==========
// Applica la modalità salvata al caricamento della pagina
if (savedMode === "enabled") {
  html.classList.add("dark-mode"); // Aggiunge classe CSS per modalità scura
  toggle.checked = true; // Sincronizza stato checkbox
}

// ========== EVENT LISTENER PER TOGGLE ==========
// Ascolta i cambi di stato del checkbox
toggle.addEventListener("change", () => {
  if (toggle.checked) {
    // Attiva modalità scura
    html.classList.add("dark-mode");
    localStorage.setItem("dark-mode", "enabled"); // Salva preferenza
  } else {
    // Disattiva modalità scura
    html.classList.remove("dark-mode");
    localStorage.setItem("dark-mode", "disabled"); // Salva preferenza
  }
});
