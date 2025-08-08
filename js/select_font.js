const selectFont = document.getElementById("select-font");
const html_font = document.documentElement;

selectFont.addEventListener("change", (event) => {
  // Imposta il font del corpo della pagina in base al valore dell'opzione selezionata
  html_font.style.fontFamily = event.target.value;
});
