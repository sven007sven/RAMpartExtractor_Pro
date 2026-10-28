# 🛡️ RAMpartExtractor Pro (v2.0)

<img width="702" height="582" alt="grafik" src="https://github.com/user-attachments/assets/19b36dd8-7fc5-41e5-907b-90d0b12d6a71" />


### Zero-Disk Archive Isolation & Hardening Security Tool
**Developed by Sven Nahrstedt**

[![Python Version](https://shields.io)](https://python.org)
[![License](https://shields.io)](LICENSE)
[![Platform](https://shields.io)]()

---

## 🚀 Was ist RAMpartExtractor Pro?

Herkömmliche Entpackungsprogramme (wie WinRAR oder 7-Zip) haben ein gefährliches Geheimnis: Wenn du ein Archiv öffnest, schreiben sie die Daten sofort im Hintergrund temporär auf deine SSD. Befindet sich darin Schadcode, hat die Malware bereits die Oberfläche deiner Festplatte berührt – noch bevor dein Antiviren-Scanner reagieren kann. Das erhöht das Infektionsrisiko und nutzt durch ständige Schreib- und Löschzyklen die empfindlichen Speicherzellen deiner SSD ab.

**RAMpartExtractor Pro löst dieses Problem radikal.** 

Das Tool nutzt die brachiale Geschwindigkeit deines **Arbeitsspeichers (RAM) als isolierte, militärisch gesicherte Quarantäne-Zone**. Archive werden zu 100 % im RAM virtuell zerlegt und dort auf Herz und Nieren geprüft. Erst wenn alle Sicherheits-Schilde grünes Licht geben, dürfen die sauberen Daten deine SSD berühren.

---

## ⚡ Die Sicherheits-Schilde im Detail

<img width="699" height="746" alt="grafik" src="https://github.com/user-attachments/assets/dc78247a-72c5-4384-852f-9a1b6045d406" />


* **Zero-Disk-Quarantäne (`io.BytesIO`):** Vollständige In-Memory-Isolierung. Kein physischer Festplattenkontakt vor dem finalen Sicherheits-Go.
* **SSD-Schutz & Langlebigkeit:** Verhindert unnötige Schreibzyklen durch infizierte temporäre Dateien und schützt die Lebensdauer deiner Hardware.
* **Militärisches Hardening gegen Exploits:**
  * **ZIP-Bomb-Defuser:** Überwacht das Kompressionsverhältnis in Echtzeit. Wenn sich Daten bösartig aufblähen, wird die Reißleine gezogen, um RAM-Overloads zu verhindern.
  * **Zip-Slip-Schutz:** Erkennt und blockiert Pfad-Traversierungs-Angriffe (Ausbrüche aus dem Zielverzeichnis).
  * **Strikte Endungs-Whitelist:** Gefährliche System- und Skriptdateien (`.exe`, `.dll`, `.bat`, `.ps1` etc.) werden im Keim erstickt.
* **YARA-Malware-Signatur-Scanner:** Scannt den RAM-Inhalt direkt gegen konfigurierbare Industriestandard-Malware-Signaturen.
* **Auto-Schild für Downloads:** Ein integrierter Hintergrund-Wächter überwacht deinen Windows-Downloads-Ordner und fängt neu heruntergeladene Archive vollautomatisch ab.
* **Native Windows-Push-Alarme:** Bei blockierten Bedrohungen schlägt das Tool direkt über das Windows-Info-Center echten Systemalarm.
* **Multi-Format & Krypto-Support:** Unterstützt `.zip`, `.rar` und `.7z` – inklusive sicherer In-Memory-Passwortentschlüsselung.

---

## 🛠️ Systemanforderungen & Installation

Das Tool wurde als **portable Standalone-Anwendung** konzipiert, um das "Zero-Disk"-Konzept treu zu bleiben. Es hinterlässt keine Registry-Einträge.

### Für Entwickler (Ausführen als Python-Skript):
1. **Repository klonen:**
   ```bash
   git clone https://github.com
   cd RAMpartExtractor
   ```
2. **Abhängigkeiten installieren:**
   ```bash
   pip install py7zr rarfile watchdog win10toast yara-python
   ```
3. **Starten:**
   ```bash
   python "RAMpart Extractor.py"
   ```

---

## 📦 Als portable Standalone-EXE kompilieren

Du möchtest das Tool als einzelne, schicke `.exe` mit dem offiziellen Festungs-Icon exportieren? Nutzen den `PyInstaller`:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --noconfirm --icon="app_icon.ico" --name="RAMpartExtractor_Pro" "RAMpart Extractor.py"
```
Die fertige Anwendung findest du anschließend im Ordner `/dist`.

---

## 📄 Lizenz & Haftungsausschluss

Dieses Projekt ist unter der **MIT-Lizenz** lizenziert. Das bedeutet: Freie Nutzung und Modifikation, jedoch unter vollständigem Ausschluss jeglicher Gewährleistung und Haftung ("as is"). Siehe die Datei [LICENSE](LICENSE) für Details.

---

## ☕ Unterstütze das Projekt
Der RAMpartExtractor Pro ist und bleibt Open Source. Wenn das Tool deine SSD schont und dir gefällt, freue ich mich riesig über eine kleine Unterstützung auf [Ko-fi / PayPal] (z. B. 10 Cent für einen virtuellen Kaffee)!
