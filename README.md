# 🛡️ RAMpartExtractor Pro (v2.1)

<img width="702" height="582" alt="grafik" src="https://github.com/user-attachments/assets/19b36dd8-7fc5-41e5-907b-90d0b12d6a71" />


### Zero-Disk Archive Isolation & Hardening Security Tool
**Developed by Sven Nahrstedt**

[![Python Version](https://shields.io)](https://python.org)
[![License](https://shields.io)](LICENSE)
[![Platform](https://shields.io)]()

---

## 🚀 Was ist RAMpartExtractor Pro?

Herkömmliche Entpackungsprogramme (wie WinRAR oder 7-Zip) haben ein gefährliches Geheimnis: Wenn du ein Archiv öffnest, schreiben sie die Daten sofort im Hintergrund temporär auf deine SSD. Befindet sich darin Schadcode, hat die Malware bereits die Oberfläche deiner Festplatte berührt – noch bevor dein Antiviren-Scanner reagieren kann. Das erhöht das Infektionsrisiko und nutzt durch ständige Schreib- und Löschzyklen die empfindlichen Speicherzellen deiner SSD ab.

## 🆕 Changelog v2.1 (Community Hardening Update)
Dank des großartigen Feedbacks aus der ComputerBase-Community wurden folgende kritische Verbesserungen umgesetzt:
- **Volle Thread-Sicherheit:** GUI-Kommunikation komplett über Queues entkoppelt (beseitigt sporadische Abstürze).
- **Echter Zip-Slip Schutz:** Harte Pfad-Validierung verhindert Verzeichnis-Ausbrüche (`../`).
- **Ressourcen-Grenzwerte aktiv:** Scharfe Durchsetzung von Speicherlimits und Kompressions-Ratios gegen ZIP-Bomben.
- **Echtes In-Memory-7z:** Vollständige Streaming-Pipeline für `.7z`-Archive implementiert.
- **Dynamischer RAM-Check:** Vorab-Prüfung via `psutil` verhindert System-Freezes bei kleinen Systemen (z.B. 8 GB RAM).
- **Prozess-Sicherheit:** Der Download-Watcher wird beim Schließen des Fensters nun sauber beendet (keine Zombie-Threads).
- **UI-Upgrade:** Neuer animierter Live-Fortschrittsbalken während des SSD-Schreibvorgangs inklusive exakter GB-Anzeige.


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

Das Tool wurde als **portable Standalone-Anwendung** konzipiert, um das "Zero-Disk"-Konzept treu zu bleiben. Es hinterlässt keine Registry-Einträge. Kompatibel mit Win10 / Win11, Entpacken und loslegen.

## 📄 Lizenz & Haftungsausschluss

Dieses Projekt ist als kostenlose **Freeware** lizenziert. Das bedeutet: Freie Nutzung, Installation und Weiterverbreitung der originalen ausführbaren Datei (EXE) für private und kommerzielle Zwecke. Jegliche Modifikation, Dekompilierung oder Veränderung der Binärdatei ist untersagt. Die Software wird ohne jegliche Gewährleistung oder Haftung ("as is") bereitgestellt. Siehe die Datei [LICENSE](LICENSE) für die vollständige Endnutzer-Lizenzvereinbarung (EULA).

---

## ☕ Unterstütze das Projekt
Der RAMpartExtractor Pro ist und bleibt noch Freeware. Wenn das Tool deine SSD schont und dir gefällt, freue ich mich riesig über eine kleine Unterstützung auf [Ko-fi / PayPal] (z. B. 10 Cent für einen virtuellen Kaffee)!


## 🔍 Unabhängiger Sicherheits-Check (VirusTotal)
Um maximale Transparenz und Sicherheit zu gewährleisten, wurde die ausführbare Datei unabhängig von über 70 Antiviren-Scannern geprüft:

* **Ergebnis:** 0 / 74 (100% Sauber)
* **SHA-256 Hash:** `28e0b23cfe26a51329061ce6d9196b04f37489f76ce3130480672de8724b9d22`
* **Direktlink zum Scan:** [VirusTotal Analysebericht ansehen](https://www.virustotal.com/gui/file/28e0b23cfe26a51329061ce6d9196b04f37489f76ce3130480672de8724b9d22/detection)
