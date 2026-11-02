# 🛡️ RAMpartExtractor Pro

<img width="1022" height="712" alt="grafik" src="https://github.com/user-attachments/assets/fa59f027-29c6-4577-ba88-4c23593063ac" />


### Zero-Disk Archive Isolation & Hardening Security Tool

**Entwickelt von Sven Nahrstedt**

---

## 💡 Warum wurde RAMpartExtractor Pro ins Leben gerufen?

Herkömmliche Entpackungsprogramme (wie WinRAR, 7-Zip oder der Windows-Explorer) haben eine gravierende Sicherheitslücke: Sie schreiben Daten beim Öffnen oder Scannen oft unbemerkt **temporär auf die Festplatte (SSD/HDD)**. 

Das birgt zwei große Probleme:
1. **Sicherheitsrisiko:** Schadcode, Zero-Day-Exploits oder getarnte Viren berühren sofort deine Hardware. Wenn ein Antivirenscanner zu spät reagiert, kann sich die Malware bereits im System einnisten.
2. **Hardware-Abnutzung:** Das ständige Schreiben und Löschen von temporären Dateien treibt die TBW-Werte (Total Bytes Written) deiner SSD unnötig in die Höhe und verkürzt deren Lebensdauer.

**RAMpartExtractor Pro löst diese Probleme radikal.** Das Tool wurde entwickelt, um eine absolut sichere Bruchbude (Quarantäne-Zone) für Archive zu schaffen, bei der potenzielle Viren die Festplatte **niemals** berühren, bevor sie nicht zu 100 % als sicher verifiziert wurden.

---

## 🚀 Was macht das Tool und wie funktioniert es?

RAMpartExtractor Pro nutzt ein **Zero-Disk-Verfahren**. Es lädt das komplette Archiv (ZIP, RAR oder 7z) direkt in eine isolierte Struktur im **Arbeitsspeicher (RAM)**. 

1. **Vollständige Isolierung:** Die Dateien werden ausschließlich im flüchtigen RAM entpackt (`io.BytesIO`). 
2. **In-Memory-Analyse:** Noch während die Daten im RAM liegen, jagen die aktiven Schutzschilde und Heuristiken über die Dateien.
3. **Sichere Freigabe:** Erst wenn feststeht, dass eine Datei absolut sauber ist, wird sie auf deine Festplatte geschrieben. Wird eine Bedrohung erkannt, wird der RAM-Inhalt gelöscht. Der Virus verpufft im Nirgendwo, ohne jemals eine Spur auf deiner SSD hinterlassen zu haben!

---

## 🛠️ Die Kernfeatures & Schutz-Schilde im Überblick

Das Tool bündelt alle kritischen Abwehr-Mechanismen in einer übersichtlichen, taktischen **Steuerzentrale**:

### 🛡️ Die aktiven Schutz-Schilde
* **YARA-Signatur-Scanner:** Scannt den RAM-Puffer im laufenden Betrieb gegen bekannte Malware-Muster und bösartige Code-Strukturen.
* **ZIP-Bomben-Defuser:** Erkennt Archive mit extremen Kompressionsraten (z. B. 1:1000), die darauf ausgelegt sind, deinen PC durch plötzliche Datenüberlastung zum Absturz zu bringen, und blockiert sie sofort.
* **Malware-Heuristik:** Überprüft Skripte und Binärdateien im Speicher auf verdächtige Befehlsketten (wie versteckte PowerShell- oder CMD-Aufrufe).
* **Path-Traversal-Schutz (Zip-Slip):** Verhindert, dass manipulierbare Archive versuchen, Dateien außerhalb des Zielordners in deine Systemverzeichnisse zu schmuggeln.
* **Strikte Endungs-Sperre:** Blockiert hochgefährliche Dateiendungen (wie `.exe`, `.bat`, `.cmd`, `.vbs`, `.ps1`) automatisch im Archiv, um eine versehentliche Ausführung zu verhindern.

### ⚙️ Komfort- & Systemfeatures
* **Downloads-Auto-Schild:** Überwacht deinen Windows-Downloads-Ordner nativ im Hintergrund über die Windows-API (`ReadDirectoryChangesW`). Es verbraucht im Standby **0 % CPU** und fängt neu heruntergeladene Archive sofort automatisch ab.
* **Dynamisches RAM-Limit:** Über ein Dropdown-Menü lässt sich festlegen, wie viel deines Arbeitsspeichers das Tool maximal für die Extraktion beanspruchen darf (von 8 GB bis 128 GB).
* **Automatischer Ordner-Schutz:** Ist ein Zielordner bereits belegt, überschreibt das Tool keine Daten, sondern legt vollautomatisch einen neuen, fortlaufenden Unterordner an.
* **Internationale Sprachmatrix:** Unterstützt den fliegenden Wechsel der kompletten Benutzeroberfläche und aller Sicherheits-Logs zwischen **Deutsch**, **Englisch**, **Chinesisch** und **Russisch**.

---

## 🖥️ Systemanforderungen & Installation

Da RAMpartExtractor Pro als **portable Standalone-Anwendung** entwickelt wurde, ist keine Installation notwendig. Das Tool hinterlässt keine Registry-Leichen auf deinem System.

* **Betriebssystem:** Windows 10 / Windows 11 (64-Bit)
* **Hardware-Empfehlung:** Aufgrund der hochsicheren In-Memory-Verarbeitung wird ein System mit **mindestens 8 GB RAM** empfohlen.

---

## 💬 Community & Support

Du hast Fragen, möchtest Feedback geben oder Fehler melden? Schau auf unseren offiziellen Plattformen vorbei:

* **Support & Austausch:** Tritt unserem offiziellen [Discord-Server](https://discord.gg/scPs8qzCx) bei!
* **Updates & Source-Code:** Das jeweils aktuellste, von Antiviren-Plattformen verifizierte Release findest du immer direkt hier auf [GitHub](https://github.com/sven007sven/RAMpartExtractor_Pro).

---
*RAMpartExtractor Pro ist kostenlose Freeware. Schütze dein System, schone deine SSD.*

---

## ⚖️ Lizenz & Rechtlicher Haftungsausschluss (Disclaimer)

Dieses Programm wird als kostenlose Freeware zur Verfügung gestellt. 

### 🚨 HAFTUNGSAUSSCHLUSS:
DIE SOFTWARE WIRD OHNE JEDE AUSDRÜCKLICHE ODER IMPLIZIERTE GARANTIE BEREITGESTELLT, EINSCHLIESSLICH, ABER NICHT BESCHRÄNKT AUF DIE GARANTIE DER MARKTGÄNGIGKEIT, DER EIGNUNG FÜR EINEN BESTIMMTEN ZWECK UND DER NICHTVERLETZUNG VON RECHTEN DRITTER. 

IN KEINEM FALL JEDOCH HAFTET DER AUTOR (SVEN NAHRSTEDT) FÜR ANSPRÜCHE, SCHÄDEN ODER ANDERE VERPFLICHTUNGEN, OB IN EINEM VERTRAGSVERFAHREN, EINEM DELIKT ODER AUF ANDERE WEISE, DIE SICH AUS, IM ZUSAMMENHANG MIT DER SOFTWARE ODER DER NUTZUNG ODER ANDEREN GESCHÄFTEN MIT DER SOFTWARE ERGEBEN.

Die Nutzung des Tools zur Analyse potenziell schädlicher Archive erfolgt vollumfänglich auf eigene Gefahr des Endanwenders. Für eventuelle Datenverluste, Systemfehler oder Schäden an der Hardware wird keinerlei Verantwortung übernommen.

