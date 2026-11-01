!!! UPDATE !!!  version 2.2 --- https://github.com/sven007sven/RAMpartExtractor_Pro/releases/tag/2.2

# 🛡️ RAMpartExtractor Pro (v2.2)

<img width="1002" height="672" alt="grafik" src="https://github.com/user-attachments/assets/05b388d9-b8ea-461a-8473-04b3bd6e6e9c" />


### Zero-Disk Archive Isolation & Hardening Security Tool
**Developed by Sven Nahrstedt**

![Plattform](https://shields.io)
![Lizenz](https://shields.io)

---

## 🚀 Was ist RAMpartExtractor Pro?

Herkömmliche Entpackungsprogramme schreiben Daten beim Öffnen oft temporär auf die SSD, was das Infektionsrisiko erhöht und die Hardware abnutzt. **RAMpartExtractor Pro löst dieses Problem radikal**, indem es den Arbeitsspeicher (RAM) als isolierte Quarantäne-Zone nutzt. Archive werden zu 100 % im RAM zerlegt und geprüft, bevor die SSD berührt wird.

---

## 🆕 Neu in Version 2.2: Die Steuerzentrale 🎛️

Mit **v2.2** wird das Tool zur Kontroll-App mit einem neuen **Zwei-Spalten-Layout (Side-by-Side)**:
*   **Dynamische RAM-Limitierung:** Speicherlimit (8 GB bis 128 GB) im laufenden Betrieb anpassen.
*   **Schutzschilde On/Off:** YARA-Scanner, Auto-Watcher und ZIP-Bomben-Defuser per Schalter steuern.
*   **Integrierte Malware-Heuristik & Ordner-Schutz:** Scannt nach Exploit-Ketten und legt bei bestehenden Ordnern automatisch fortlaufende Unterordner an.
*   **Nativer Windows-API Watcher:** Läuft über `ReadDirectoryChangesW` mit 0 % CPU im Standby.

---

## ⚡ Die Sicherheits-Schilde im Detail

*   **Zero-Disk-Quarantäne (`io.BytesIO`):** Vollständige In-Memory-Isolierung.
*   **SSD-Schutz & Langlebigkeit:** Schont TBW-Werte durch Vermeidung unnötiger Schreibzyklen.
*   **Schutzfunktionen:** Enthält ZIP-Bomb-Defuser, Zip-Slip-Schutz, strikte Endungs-Sperre, native Windows-Push-Alarme sowie Multi-Format- und Krypto-Support.

---

## 🛠️ Systemanforderungen & Installation

Als portable Standalone-Anwendung hinterlässt das Tool keine Registry-Einträge.
*   **Kompatibilität:** Windows 10 / Windows 11 (64-Bit).
*   **Empfehlung:** Aufgrund der In-Memory-Extraktion für Systeme **ab 8 GB RAM** empfohlen.

---

## 📄 Lizenz, Support & Weitere Details

Das Projekt ist als kostenlose **Freeware** lizenziert. Den vollständigen und detaillierten Text der README inklusive Lizenzvereinbarungen und Spendenhinweisen finden Sie in der Original-Dokumentation.
