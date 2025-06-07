# KI-basiertes Taktzeit-Monitoring für menschliche Montageprozesse in der Mensch-Roboter-Kollaboration

Dieses Projekt dient der Entwicklung eines KI-basierten Systems zur Überwachung und Analyse von Taktzeiten in menschlichen Montageprozessen, insbesondere in der Mensch-Roboter-Kollaboration.

**Projektziele:**
- Literaturrecherche und Anforderungsanalyse
- Objekterkennung (YOLO/SSD) zur Identifikation von Werkzeugen/Montageteilen
- Pose Estimation (MediaPipe/OpenPose) zur Bewegungserfassung des Menschen
- Automatische Segmentierung von Montagephasen (z. B. Greifen, Fügen, Verschrauben)
- Berechnung der Taktzeit pro Schritt mittels Ereignis-basiertem Triggering
- Testen und Validieren im realen Szenario

**Voraussetzungen:**
- Grundkenntnisse in Computer Vision (OpenCV, TensorFlow/PyTorch)
- Programmierkenntnisse in Python/C++
- Engagierte und selbstständige Arbeitsweise

---

# YOLO + MediaPipe Hand Tracking mit Basler Kamera

Dieses Projekt bietet Python-Skripte für die Echtzeit-Handerkennung und Objekterkennung mit YOLO und MediaPipe. Unterstützt werden sowohl Basler-Industriekameras (über pypylon) als auch Standard-Webcams (über OpenCV).

## Features
- Hand-Tracking mit MediaPipe
- Objekterkennung mit YOLO (GPU-beschleunigt, falls verfügbar)
- Unterstützung für Basler-Kameras (volle Sensorfläche oder ROI)
- Flexible Umschaltung zwischen Kameraquellen
- Automatische Videoaufnahme und Speicherung in den Ordner `videos/` (wird nicht versioniert)
- Einfache Konfiguration und Automatisierung (Batch-Datei)

## Voraussetzungen
- Python 3.8+
- Basler-Kamera (optional, für industrielle Anwendungen)
- Alle Abhängigkeiten aus `requirements.txt`

## Installation & Setup
1. **Projektdateien auf den Rechner kopieren oder clonen.**
2. **Virtuelle Umgebung erstellen und aktivieren (empfohlen):**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Abhängigkeiten installieren:**
   ```powershell
   pip install -r requirements.txt
   ```

## Ausführung der Skripte

### Hand- und Objekterkennung (YOLO + MediaPipe)
1. Virtuelle Umgebung aktivieren:
   ```powershell
   .venv\Scripts\activate
   ```
2. Skript starten:
   ```powershell
   python src/yolo_mediapipe_test.py
   ```
   - Für eine bestimmte Kamera (z.B. Index 1):
     ```powershell
     python src/yolo_mediapipe_test.py --camera 1
     ```

### Videoaufnahme (Rohvideo)
1. Virtuelle Umgebung aktivieren:
   ```powershell
   .venv\Scripts\activate
   ```
2. Aufnahme starten (endet mit 'q'):
   ```powershell
   python src/raw_video_capture.py
   ```
   - Die Videos werden automatisch mit Zeitstempel im Ordner `videos/` gespeichert.
   - Der Ordner `videos/` ist in `.gitignore` eingetragen und wird nicht versioniert.

### Mit Batch-Datei (Windows)
Die Batch-Datei `run_yolo_mediapipe.bat` automatisiert die Aktivierung der Python-Umgebung und den Start des Hand-/Objekterkennungs-Skripts. Sie sorgt dafür, dass du das Skript bequem per Doppelklick starten kannst, ohne manuell die virtuelle Umgebung aktivieren oder Befehle in der Konsole eingeben zu müssen.

**Ablauf der Batch-Datei:**
- Aktiviert die virtuelle Umgebung (`.venv`)
- Startet das Skript `src/yolo_mediapipe_test.py`
- Wartet auf Tastendruck, damit das Fenster nicht sofort schließt

**Inhalt der Batch-Datei:**
```bat
@echo off
call .venv\Scripts\activate.bat
python src/yolo_mediapipe_test.py
pause
```

Doppelklick auf `run_yolo_mediapipe.bat` startet das Skript direkt.

## Hinweise
- Capturing kann über die Variable `CAPTURE_ENABLED` im Skript aktiviert/deaktiviert werden.
- Für Webcams wird der Standard- oder angegebene Kamera-Index verwendet.
- Mit `q` im Vorschaufenster kann das Programm beendet werden.
- Die aufgenommenen Videos werden im Ordner `videos/` gespeichert und nicht versioniert.

## Troubleshooting
- Fehlende Abhängigkeiten? Sicherstellen, dass die virtuelle Umgebung aktiv ist und alle Pakete installiert sind.
- Probleme mit Basler-Auflösung? Unterstützte Auflösungen der Kamera prüfen und ggf. die Werte im Skript anpassen.

---
