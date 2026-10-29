# security.py
import os
import yara

try:
    import psutil
except ImportError:
    psutil = None

# --- ERWEITERTE CONFIG FÜR GROSSE ARCHIVE (v2.1) ---
MAX_DATEI_GROESSE = 5 * 1024 * 1024 * 1024       # Erhöht auf 5 GB für riesige Packdateien
MAX_GESAMT_GROESSE = 25 * 1024 * 1024 * 1024     # Erhöht auf 25 GB Gesamtgröße im RAM (Perfekt für deine 48 GB RAM)
MAX_KOMPRESSIONS_RATIO = 1500                    # Erhöht auf 1500x für stark gepackte Spieldaten
DOWNLOADS_ORDNER = os.path.join(os.path.expanduser("~"), "Downloads")

GEFAEHRLICHE_ENDUNGEN = {
    ".exe", ".dll", ".sys", ".com", ".bat", ".cmd", ".vbs", ".vbe", ".js", 
    ".jse", ".wsf", ".wsh", ".ps1", ".msc", ".lnk", ".pif", ".scr", ".sh", ".py"
}

YARA_REGELN_TEXT = """
rule Verdaechtiges_Muster_Entdeckt {
    strings:
        $cmd_exec = "cmd.exe /c" nocase
        $powershell = "powershell -nop -w hidden" nocase
        $download_string = "DownloadString(" nocase
        $shellcode_pattern = { E8 00 00 00 00 58 }
    condition:
        any of them
}
"""

class SecurityEngine:
    def __init__(self, log_callback):
        self.log = log_callback
        self.yara_scanner = None
        self.init_yara()

    def init_yara(self):
        if yara:
            try:
                self.yara_scanner = yara.compile(source=YARA_REGELN_TEXT)
            except Exception as e:
                self.log(f"[-] Fehler beim Kompilieren der YARA-Regeln: {e}")

    def validiere_pfad(self, datei_name, ziel_ordner):
        """Verhindert Path Traversal (Zip-Slip Schwachstelle)"""
        absoluter_zielordner = os.path.abspath(ziel_ordner)
        ziel_datei_pfad = os.path.abspath(os.path.join(absoluter_zielordner, datei_name))
        return ziel_datei_pfad.startswith(absoluter_zielordner + os.sep) or ziel_datei_pfad == absoluter_zielordner

    def pruefe_ressourcen(self, groesse_komprimiert, groesse_entpackt, datei_name):
        """Überprüft Dateigrößen-Limits und Kompressions-Ratios (Zip-Bomb/DOS Schutz)"""
        if groesse_entpackt > MAX_DATEI_GROESSE:
            self.log(f"[!] BLOCKIERT: '{datei_name}' überschreitet maximale zulässige Einzelgröße ({MAX_DATEI_GROESSE // 1024 // 1024} MB).")
            return False
        
        if groesse_komprimiert > 0:
            ratio = groesse_entpackt / groesse_komprimiert
            if ratio > MAX_KOMPRESSIONS_RATIO:
                self.log(f"[!] BLOCKIERT: Verdacht auf Zip-Bombe bei '{datei_name}' (Ratio: {ratio:.1f}x).")
                return False
        return True

    def pruefe_ram_verfuegbarkeit(self, benoetigter_ram):
        """Verhindert MemoryError/System-Crash bei zu geringem RAM"""
        if psutil:
            verfuegbar = psutil.virtual_memory().available
            if benoetigter_ram + (150 * 1024 * 1024) > verfuegbar:
                return False
        return True

    def pruefe_endung(self, datei_name):
        """Überprüft, ob die Dateiendung als gefährlich eingestuft ist"""
        _, endung = os.path.splitext(datei_name.lower())
        if endung in GEFAEHRLICHE_ENDUNGEN:
            self.log(f"[!] BLOCKIERT: Gefährliche Endung '{endung}' bei '{datei_name}'.")
            return False
        return True

    def scanne_bytes(self, datei_name, datei_bytes):
        """Führt einen In-Memory YARA-Scan durch"""
        if self.yara_scanner:
            treffer = self.yara_scanner.match(data=datei_bytes)
            if treffer:
                return False
        return True
