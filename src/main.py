# main.py
import os
import queue
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk

from security import SecurityEngine
from extractor import InMemoryExtractor

# Optionale Sicherheits-Bibliotheken dynamisch laden
try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
except ImportError:
    FileSystemEventHandler, Observer = None, None
try:
    from win10toast import ToastNotifier
except ImportError:
    ToastNotifier = None

DOWNLOADS_ORDNER = os.path.join(os.path.expanduser("~"), "Downloads")

# WATCHER
class DownloadWatcher(FileSystemEventHandler):
    def __init__(self, app_callback):
        self.app_callback = app_callback

    def on_created(self, event):
        if not event.is_directory:
            _, ext = os.path.splitext(event.src_path.lower())
            if ext in [".zip", ".7z", ".rar"]:
                self.app_callback(event.src_path)


class RAMpartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RAMpart Extractor Pro - Zero-Disk Quarantäne v2.1")
        self.root.geometry("700x550")
        self.root.configure(bg="#1e1e1e")
        
        # Thread-sichere Queues für GUI-Updates und Datei-Abfänge
        self.file_queue = queue.Queue()
        self.gui_queue = queue.Queue()

        # Engines initialisieren (reine Thread-Sicherheit durch Callbacks)
        self.security = SecurityEngine(log_callback=self.log)
        self.extractor = InMemoryExtractor(
            security_engine=self.security, 
            log_callback=self.log, 
            ask_password_callback=self.frage_passwort_aus_thread
        )

        # UI Layout
        titel = tk.Label(root, text="🛡️ RAMpartExtractor", font=("Arial", 20, "bold"), fg="#00ff66", bg="#1e1e1e")
        titel.pack(pady=(15, 0))
        
        # Untertitel mit namentlicher Signatur und Version 2.1
        untertitel = tk.Label(
            root, 
            text="by Sven Nahrstedt  |  v2.1", 
            font=("Times New Roman", 11, "italic"), 
            fg="#ffffff", 
            bg="#1e1e1e"
        )
        untertitel.pack(pady=(2, 15))

        self.erstelle_pfad_gui()

        self.btn_start = tk.Button(root, text="ARCHIV SICHER IM RAM PRÜFEN & ENTPACKEN", font=("Arial", 11, "bold"), bg="#00ff66", fg="black", command=self.starte_manuell)
        self.btn_start.pack(pady=10, fill="x", padx=20)

        # Unbestimmter Fortschrittsbalken (wird dynamisch über .pack() gesteuert)
        self.progress = ttk.Progressbar(root, orient="horizontal", mode="indeterminate", length=400)

        tk.Label(root, text="Sicherheits-Protokoll:", fg="white", bg="#1e1e1e").pack(anchor="w", padx=20)
        self.log_area = scrolledtext.ScrolledText(root, bg="#111111", fg="#00ff66", font=("Consolas", 10))
        self.log_area.pack(padx=20, pady=5, fill="both", expand=True)

        self.log("[*] RAMpart Schilde online. System bereit.")
        self.pruefe_module()
        self.starte_downloads_watcher()
        # Fängt das "X"-Schließen-Kreuz ab und leitet an unsere Beenden-Logik weiter
        self.root.protocol("WM_DELETE_WINDOW", self.beende_anwendung)
        # Periodische Timer für Queues im Hauptthread
        self.root.after(100, self.verarbeite_file_queue)
        self.root.after(50, self.verarbeite_gui_queue)

    def erstelle_pfad_gui(self):
        f1 = tk.Frame(self.root, bg="#1e1e1e")
        f1.pack(pady=3, fill="x", padx=20)
        tk.Label(f1, text="Archiv-Pfad: ", fg="white", bg="#1e1e1e", width=12).pack(side="left")
        self.entry_zip = tk.Entry(f1, bg="#2d2d2d", fg="white")
        self.entry_zip.pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(f1, text="Durchsuchen...", command=self.waehle_archiv, bg="#444").pack(side="right")

        f2 = tk.Frame(self.root, bg="#1e1e1e")
        f2.pack(pady=3, fill="x", padx=20)
        tk.Label(f2, text="Zielordner: ", fg="white", bg="#1e1e1e", width=12).pack(side="left")
        self.entry_ziel = tk.Entry(f2, bg="#2d2d2d", fg="white")
        self.entry_ziel.pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(f2, text="Durchsuchen...", command=self.waehle_ziel, bg="#444").pack(side="right")

    def pruefe_module(self):
        if not getattr(sys.modules['extractor'], 'py7zr', None): self.log("[-] Warnung: 'py7zr' fehlt. Keine .7z Unterstützung.")
        if not getattr(sys.modules['extractor'], 'rarfile', None): self.log("[-] Warnung: 'rarfile' fehlt. Keine .rar Unterstützung.")
        if not Observer: self.log("[-] Warnung: 'watchdog' fehlt. Auto-Scan deaktiviert.")
        if not getattr(sys.modules['security'], 'psutil', None): self.log("[-] Warnung: 'psutil' fehlt. Dynamischer RAM-Check inaktiv.")

    def log(self, text):
        """Kann sicher aus jedem Worker-Thread aufgerufen werden (nutzt Queue)"""
        self.gui_queue.put(("LOG", text))

    def send_windows_notification(self, titel, nachricht):
        if ToastNotifier:
            try:
                ToastNotifier().show_toast(titel, nachricht, icon_path=None, duration=5, threaded=True)
            except: pass

    def starte_downloads_watcher(self):
        if Observer:
            handler = DownloadWatcher(lambda pfad: self.file_queue.put(pfad))
            self.observer = Observer()
            self.observer.schedule(handler, path=DOWNLOADS_ORDNER, recursive=False)
            self.observer.start()
            self.log("[+] Auto-Schild aktiv: Überwache Downloads-Ordner...")

    def verarbeite_file_queue(self):
        try:
            datei_pfad = self.file_queue.get_nowait()
            self.entry_zip.delete(0, tk.END)
            self.entry_zip.insert(0, datei_pfad)
            self.send_windows_notification("RAMpart Schutzschild", f"Archiv abgefangen: {os.path.basename(datei_pfad)}")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            self.entry_ziel.delete(0, tk.END)
            self.entry_ziel.insert(0, os.path.join(desktop, "RAMpart_Sicher_Extrakt"))
            self.starte_prozess(datei_pfad, self.entry_ziel.get())
        except queue.Empty: pass
        self.root.after(100, self.verarbeite_file_queue)

    def verarbeite_gui_queue(self):
        """Verarbeitet UI-Aktionen strikt im Main-Thread (Thread-Sicherheit)"""
        try:
            while True:
                aktion, daten = self.gui_queue.get_nowait()
                if aktion == "LOG":
                    self.log_area.insert(tk.END, daten + "\n")
                    self.log_area.see(tk.END)
                elif aktion == "ERROR_MSG":
                    messagebox.showerror("Fehler", daten)
                elif aktion == "ALERT_MSG":
                    messagebox.showerror("ALARM", daten)
                elif aktion == "CLEAR_LOG":
                    self.log_area.delete("1.0", tk.END)
                elif aktion == "START_PROGRESS":
                    # 'after=self.btn_start' zwingt den Balken, sich direkt unter dem Button zu platzieren!
                    self.progress.pack(after=self.btn_start, pady=5)
                    self.progress.start(10)
                elif aktion == "STOP_PROGRESS":
                    self.progress.stop()
                    self.progress.pack_forget()
        except queue.Empty: pass
        self.root.after(50, self.verarbeite_gui_queue)

    def waehle_archiv(self):
        datei = filedialog.askopenfilename(filetypes=[("Archive", "*.zip *.7z *.rar")])
        if datei:
            self.entry_zip.delete(0, tk.END)
            self.entry_zip.insert(0, datei)

    def waehle_ziel(self):
        ordner = filedialog.askdirectory()
        if ordner:
            self.entry_ziel.delete(0, tk.END)
            self.entry_ziel.insert(0, ordner)

    def frage_passwort_aus_thread(self):
        """Erlaubt dem Worker-Thread, synchron nach Passwörtern zu fragen, ohne abzustürzen"""
        res = []
        def ask(): 
            res.append(simpledialog.askstring("Passwort", "Archiv ist verschlüsselt. Passwort:", show="*"))
        self.root.after(0, ask)
        while not res: 
            time.sleep(0.1)
        return res

    def starte_manuell(self):
        self.starte_prozess(self.entry_zip.get(), self.entry_ziel.get())

    def starte_prozess(self, archiv_pfad, ziel_ordner):
        if not archiv_pfad or not ziel_ordner:
            messagebox.showerror("Fehler", "Pfade unvollständig!")
            return

        self.gui_queue.put(("CLEAR_LOG", None))
        self.log(f"[*] STARTE HARDENING-ANALYSE FÜR: {os.path.basename(archiv_pfad)}")

        _, ext = os.path.splitext(archiv_pfad.lower())
        threading.Thread(
            target=self._hintergrund_analyse_workflow, 
            args=(archiv_pfad, ziel_ordner, ext), 
            daemon=True
        ).start()

    def _hintergrund_analyse_workflow(self, pfad, ziel, ext):
        """Der Worker-Thread Workflow - Ladebalken startet erst beim Schreiben auf die SSD"""
        ergebnis = self.extractor.verarbeite_archiv(pfad, ziel, ext)
        
        if ergebnis is None:
            return

        isolierte_daten, gesamt_bytes_ram = ergebnis

        if not isolierte_daten:
            self.log("[-] Keine extrahierbaren oder sicheren Dateien im Archiv gefunden.")
            return

        # YARA Signatur Scan im RAM
        if self.security.yara_scanner:
            self.log("[*] Starte YARA-Malware-Signatur-Scan im RAM...")
            for name, datei_bytes in isolierte_daten.items():
                if not self.security.scanne_bytes(name, datei_bytes):
                    alarm_msg = f"VIRUS ERKANNT: '{name}' enthält bekannte Malware-Muster!"
                    self.log(f"[!!!] {alarm_msg}")
                    self.send_windows_notification("🚨 KRITISCHER ALARM", alarm_msg)
                    self.gui_queue.put(("ALERT_MSG", alarm_msg))
                    return

        self.log("[+] Alle Schilde grün. Keine Bedrohungen gefunden.")
        self.log("[*] Schreibe bereinigte Daten auf das Ziellaufwerk...")

        # Aktiviert den Ladebalken exakt im Moment der SSD-Interaktion
        self.gui_queue.put(("START_PROGRESS", None))

        try:
            zaehler = 0
            for name, datei_bytes in isolierte_daten.items():
                end_pfad = os.path.abspath(os.path.join(ziel, name))
                os.makedirs(os.path.dirname(end_pfad), exist_ok=True)
                with open(end_pfad, "wb") as f_out:
                    f_out.write(datei_bytes)
                
                # GUI-Entlastung: Alle 100 verarbeiteten Dateien die UI aktualisieren
                zaehler += 1
                if zaehler % 100 == 0:
                    self.root.update_idletasks()

            # Umrechnung in Gigabyte
            gesamt_gb_ssd = gesamt_bytes_ram / (1024 * 1024 * 1024)

            self.log(f"[++++] SUCCESS: {len(isolierte_daten)} Dateien sicher entpackt.")
            self.log(f"[INFO] Gesamtgröße auf SSD abgelegt: {gesamt_gb_ssd:.2f} GB")
            self.send_windows_notification("RAMpart Schutzschild", f"Archiv absolut sicher entpackt! ({gesamt_gb_ssd:.2f} GB)")
            
        except Exception as e:
            self.log(f"[!] Schreibfehler auf Datenträger: {e}")
        finally:
            self.gui_queue.put(("STOP_PROGRESS", None))

    def beende_anwendung(self):
        """Stoppt den Download-Watcher sauber, bevor das Fenster geschlossen wird"""
        if hasattr(self, 'observer') and self.observer:
            self.log("[*] Schließe RAMpart-Schilde... Bitte warten...")
            self.root.update_idletasks()
            
            # Watcher signalisieren, dass er stoppen soll
            self.observer.stop()
            
            # Warten, bis der Watcher-Thread sich komplett aufgelöst hat
            self.observer.join()
            
        # Erst jetzt das Tkinter-Fenster endgültig zerstören
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = RAMpartApp(root)
    root.mainloop()
