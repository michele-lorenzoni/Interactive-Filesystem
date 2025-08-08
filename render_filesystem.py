# Importazioni necessarie per il funzionamento del programma
import json  # Per leggere e parsare il file JSON del filesystem
import os  # Per operazioni sui path (estrazione estensioni file)
from bs4 import BeautifulSoup

import icons

# Icona generica per file senza tipo specifico - grigio neutro (#c5c5c5)
GENERIC_FILE_ICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
                        <path fill="#c5c5c5" d="M20.414 2H5v28h22V8.586ZM7 28V4h12v6h6v18Z"/>
                        </svg>"""

FOLDER_ICON = icons.folder_icon()
FILE_ICONS = icons.file_icons()


# ========== FUNZIONE RICORSIVA PER RENDERIZZARE I NODI ==========
def render_node(name, content, depth=0):
    """
    Funzione ricorsiva che converte la struttura JSON del filesystem in HTML

    Args:
        name (str): Nome del file o cartella
        content (dict|str): Se dict = cartella con sottoelementi, se str = file con permessi
        depth (int): Livello di profondità per l'indentazione CSS

    Returns:
        list: Lista di stringhe HTML che rappresentano il nodo
    """
    lines = []  # Lista per accumulare le righe HTML generate

    # ========== GESTIONE CARTELLE ==========
    if isinstance(content, dict):
        # Se content è un dizionario, allora è una cartella

        # Estrae i permessi della cartella, default "drwxr-xr-x" se non specificati
        perm = content.get("permissions", "drwxr-xr-x")

        # Crea elemento HTML <details> per cartelle espandibili/contraibili
        lines.append(f"<details style='--depth:{depth}'>")

        # Summary contiene icona cartella + nome + tooltip con permessi
        lines.append(
            f"<summary><span class='icon folder-icon'>{FOLDER_ICON}</span><span class='clickable' title='Permissions: {perm}'>{name}</span></summary>"
        )

        # ========== RICORSIONE PER CONTENUTO CARTELLA ==========
        for child_name, child_content in content.items():
            # Salta la chiave speciale "permissions" che non è un file/cartella reale
            if child_name == "permissions":
                continue

            # Chiamata ricorsiva per ogni figlio, incrementando la profondità
            # extend() aggiunge tutti gli elementi della lista ritornata
            lines.extend(render_node(child_name, child_content, depth + 1))

        # Chiude l'elemento <details>
        lines.append("</details>")

    # ========== GESTIONE FILE ==========
    else:
        # Se content non è un dizionario, è un file (content contiene i permessi)

        # Determina i permessi del file (usa content se stringa, altrimenti default)
        perm = content if isinstance(content, str) else "-rw-r--r--"

        # Estrae l'estensione del file usando os.path.splitext()
        # Esempio: "script.py" -> ("script", ".py")
        _, file_extension = os.path.splitext(name)

        # Cerca l'icona specifica per l'estensione, fallback a icona generica
        icon = FILE_ICONS.get(file_extension, GENERIC_FILE_ICON)

        # Crea attributo data-file-type per possibili utilizzi CSS/JS futuri
        # Rimuove il punto dall'estensione: ".py" -> "py"
        file_type = file_extension.lstrip(".") if file_extension else "generic"

        # Genera HTML per il file (div semplice, non espandibile come le cartelle)
        lines.append(
            f"<div style='--depth:{depth}'><span class='icon file-icon' data-file-type='{file_type}'>{icon}</span><span title='Permissions: {perm}'>{name}</span></div>"
        )

    return lines


# ========== CARICAMENTO STRUTTURA FILESYSTEM ==========
try:
    # Tenta di leggere il file JSON con la struttura del filesystem
    with open("filesystem.json", "r", encoding="utf-8") as f:
        filesystem = json.load(f)

except FileNotFoundError:
    # Se il file non esiste, crea una struttura di esempio
    print("Errore: 'filesystem.json' non trovato. Creando un esempio...")
    filesystem = {
        "home": {
            "user": {
                "documents": {
                    "report.docx": "-rw-r--r--",  # File Word con permessi lettura/scrittura
                    "photo.jpg": "-rw-r--r--",  # Immagine JPEG
                },
                "projects": {
                    "myscript.py": "-rwxr-xr-x",  # Script Python eseguibile
                },
                "settings.ini": "-rw-r--r--",  # File configurazione
            }
        },
        "etc": {
            "hosts": "-rw-r--r--",  # File hosts di sistema
            "nginx": {"nginx.conf": "-rw-r--r--"},  # Configurazione Nginx
        },
    }

# ========== GENERAZIONE STRUTTURA HTML ==========
# Lista che conterrà tutte le righe del documento HTML finale
html_lines = [
    "<!DOCTYPE html>",  # Dichiarazione HTML5
    "<html>",
    "<head>",
    # ========== OTTIMIZZAZIONE CARICAMENTO FONT ==========
    # Preconnect ottimizza il caricamento dei font Google
    "  <link rel='preconnect' href='https://fonts.googleapis.com'>",
    "  <link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>",
    # Carica font Victor Mono (monospaziale per aspetto da terminale)
    "  <link href='https://fonts.googleapis.com/css2?family=Victor+Mono:ital,wght@0,100..700;1,100..700&display=swap' rel='stylesheet'>",
    "  <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/@typopro/web-iosevka@3.7.5/TypoPRO-Iosevka.min.css'>",
    "  <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/monaspace-font@0.0.2/neon.css'>",
    "  <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/monaspace-font@0.0.2/argon.css'>",
    "  <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/monaspace-font@0.0.2/xenon.css'>",
    "  <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/monaspace-font@0.0.2/radon.css'>",
    "  <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/monaspace-font@0.0.2/krypton.css'>",
    # ========== METADATI DOCUMENTO ==========
    "  <meta charset='UTF-8'>",  # Supporto caratteri Unicode
    "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",  # Responsive design
    "  <link rel='stylesheet' href='css/style.css'>",  # Link al CSS esterno
    "  <script src='js/dark_mode.js' defer></script>",
    "  <script src='js/select_font.js' defer></script>",
    "  <title>FileSystem Interattivo</title>",
    "</head>",
    "<body>",
    "<div id='main-cont-0'>",
    "<h1>FileSystem Interattivo</h1>",
]

# ========== GENERAZIONE CONTENUTO FILESYSTEM ==========
# Itera attraverso ogni elemento root del filesystem e lo renderizza
for name, content in filesystem.items():
    html_lines.extend(render_node(name, content))

html_lines += [
    "</div>",
    "<div id='main-cont-1'>",
    # ========== CONTROLLO MODALITÀ SCURA ==========
    "  <div class='color-toggle-container'>",
    "    <input type='checkbox' id='dark-mode-toggle'>",  # Checkbox per attivare/disattivare
    "    <label for='dark-mode-toggle'>Invert Color</label>",  # Label collegata al checkbox
    "  </div>",
    "  <div class='select'>",
    "   <select  id='select-font'>",
    "       <option value='Victor Mono'>Victor Mono</option>",
    "       <option value='TypoPRO Iosevka Term'>TypoPRO Iosevka Term</option>",
    "       <option value='Monaspace Neon'>Monaspace Neon</option>",
    "       <option value='Monaspace Argon'>Monaspace Argon</option>",
    "       <option value='Monaspace Xenon'>Monaspace Xenon</option>",
    "       <option value='Monaspace Radon'>Monaspace Radon</option>",
    "       <option value='Monaspace Krypton'>Monaspace Krypton</option>",
    "   </select>",
    "  </div>",
    "</div>",
    "</body>",
    "</html>",
]

# ========== SCRITTURA FILE HTML FINALE ==========
# Unisce tutte le righe e scrive il file HTML risultante
with open("interactive_filesystem.html", "w", encoding="utf-8") as f:
    html_string = "\n".join(html_lines)
    soup = BeautifulSoup(html_string, "html.parser")
    pretty_html = soup.prettify()
    f.write(pretty_html)

print("File 'interactive_filesystem.html' generato con successo.")
