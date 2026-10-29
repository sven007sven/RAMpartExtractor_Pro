# extractor.py
import io
import os
import zipfile
from security import MAX_GESAMT_GROESSE, MAX_DATEI_GROESSE

try:
    import py7zr
except ImportError:
    py7zr = None
try:
    import rarfile
except ImportError:
    rarfile = None

class InMemoryExtractor:
    def __init__(self, security_engine, log_callback, ask_password_callback):
        self.security = security_engine
        self.log = log_callback
        self.frage_passwort = ask_password_callback

    def verarbeite_archiv(self, pfad, ziel, ext):
        """Liest das Archiv komplett in den RAM und startet das Entpacken"""
        archiv_groesse = os.path.getsize(pfad)
        if not self.security.pruefe_ram_verfuegbarkeit(archiv_groesse):
            self.log("[!] ABBRUCH: Nicht genügend freier RAM vorhanden, um das Archiv sicher zu puffern!")
            return None

        try:
            with open(pfad, "rb") as f:
                ram_buffer = io.BytesIO(f.read())
            self.log("[+] Datei erfolgreich in Quarantäne-RAM isoliert.")
        except Exception as e:
            self.log(f"[!] Ladefehler: {e}")
            return None

        isolierter_speicher = {}
        passwort = None
        gesamt_groesse_akkumuliert = 0

        # --- ZIP VERARBEITUNG ---
        if ext == ".zip":
            with zipfile.ZipFile(ram_buffer) as archiv:
                if archiv.namelist():
                    try:
                        archiv.testzip()
                    except RuntimeError:
                        passwort = self.frage_passwort()

                for info in archiv.infolist():
                    if info.is_dir(): 
                        continue
                    
                    if not self.security.validiere_pfad(info.filename, ziel):
                        self.log(f"[!] WARNUNG: Path Traversal Versuch blockiert bei: {info.filename}")
                        continue

                    if not self.security.pruefe_endung(info.filename):
                        continue

                    if not self.security.pruefe_ressourcen(info.compress_size, info.file_size, info.filename):
                        continue

                    gesamt_groesse_akkumuliert += info.file_size
                    if gesamt_groesse_akkumuliert > MAX_GESAMT_GROESSE:
                        self.log("[!] ABBRUCH: Maximales Gesamt-Extraktionslimit für RAM überschritten!")
                        return None

                    if not self.security.pruefe_ram_verfuegbarkeit(info.file_size):
                        self.log(f"[!] ABBRUCH: RAM erschöpft während der Pufferung von '{info.filename}'.")
                        return None

                    isolierter_speicher[info.filename] = archiv.read(info, pwd=passwort.encode() if passwort else None)

        # --- 7Z VERARBEITUNG ---
        elif ext == ".7z" and py7zr:
            try:
                with py7zr.SevenZipFile(ram_buffer, mode="r") as archiv:
                    if archiv.needs_password():
                        passwort = self.frage_passwort()
                
                ram_buffer.seek(0)
                with py7zr.SevenZipFile(ram_buffer, mode="r", password=passwort) as s7:
                    for name, bio in s7.readall().items():
                        if not self.security.validiere_pfad(name, ziel):
                            self.log(f"[!] WARNUNG: Path Traversal Versuch blockiert bei: {name}")
                            continue

                        if not self.security.pruefe_endung(name):
                            continue

                        datei_bytes = bio.read()
                        entpackte_groesse = len(datei_bytes)

                        if entpackte_groesse > MAX_DATEI_GROESSE:
                            self.log(f"[!] BLOCKIERT: '{name}' überschreitet Limit.")
                            continue

                        gesamt_groesse_akkumuliert += entpackte_groesse
                        if gesamt_groesse_akkumuliert > MAX_GESAMT_GROESSE:
                            self.log("[!] ABBRUCH: Maximales Gesamt-Extraktionslimit überschritten!")
                            return None

                        isolierter_speicher[name] = datei_bytes
            except Exception as e:
                self.log(f"[!] 7z Fehler: {e}")
                return None

        # --- RAR VERARBEITUNG ---
        elif ext == ".rar" and rarfile:
            try:
                with rarfile.RarFile(ram_buffer) as archiv:
                    if archiv.needs_password():
                        passwort = self.frage_passwort()
                    for info in archiv.infolist():
                        if info.isdir(): 
                            continue
                        
                        if not self.security.validiere_pfad(info.filename, ziel):
                            self.log(f"[!] WARNUNG: Path Traversal blockiert bei: {info.filename}")
                            continue

                        if not self.security.pruefe_endung(info.filename):
                            continue

                        if not self.security.pruefe_ressourcen(info.compress_size, info.file_size, info.filename):
                            continue

                        gesamt_groesse_akkumuliert += info.file_size
                        if gesamt_groesse_akkumuliert > MAX_GESAMT_GROESSE:
                            self.log("[!] ABBRUCH: Gesamt-Extraktionslimit überschritten!")
                            return None

                        isolierter_speicher[info.filename] = archiv.read(info.filename, psw=passwort)
            except Exception as e:
                self.log(f"[!] RAR Fehler: {e}")
                return None

        return isolierter_speicher, gesamt_groesse_akkumuliert
