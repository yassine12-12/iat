# KI-basiertes Taktzeit-Monitoring für menschliche Montageprozesse in der Mensch-Roboter-Kollaboration
(Bsher Karbouj – TU Berlin)

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

Dieses Projekt bietet ein Python-Skript für die Echtzeit-Handerkennung und Objekterkennung mit YOLO und MediaPipe. Unterstützt werden sowohl Basler-Industriekameras (über pypylon) als auch Standard-Webcams (über OpenCV).

## Features
- Hand-Tracking mit MediaPipe
- Objekterkennung mit YOLO (GPU-beschleunigt, falls verfügbar)
- Unterstützung für Basler-Kameras (ROI-Cropping für Performance)
- Flexible Umschaltung zwischen Kameraquellen
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

## Ausführung des Skripts

### Mit virtueller Umgebung (empfohlen)
1. Virtuelle Umgebung aktivieren:
   ```powershell
   .venv\Scripts\activate
   ```
2. Skript starten:
   ```powershell
   python src/yolo_mediapipe_test.py
   ```
   - Standardmäßig ist das Capturing aktiviert, wenn `CAPTURE_ENABLED = True` im Skript gesetzt ist.
   - Für eine bestimmte Kamera (z.B. Index 1):
     ```powershell
     python src/yolo_mediapipe_test.py --camera 1
     ```

### Mit Batch-Datei (Windows)
Die Batch-Datei `run_yolo_mediapipe.bat` automatisiert Aktivierung und Start:

```bat
@echo off
call .venv\Scripts\activate.bat
python src/yolo_mediapipe_test.py
pause
```

Doppelklick auf `run_yolo_mediapipe.bat` startet das Skript.

## Hinweise
- Capturing kann über die Variable `CAPTURE_ENABLED` im Skript aktiviert/deaktiviert werden.
- Bei Basler-Kameras wird das Bild automatisch auf einen mittigen 640x480-Bereich gecroppt.
- Für Webcams wird der Standard- oder angegebene Kamera-Index verwendet.
- Mit `q` im Vorschaufenster kann das Programm beendet werden.

## Troubleshooting
- Fehlende Abhängigkeiten? Sicherstellen, dass die virtuelle Umgebung aktiv ist und alle Pakete installiert sind.
- Probleme mit Basler-ROI? Unterstützte Auflösungen der Kamera prüfen und ggf. `ROI_W` und `ROI_H` im Skript anpassen.

---

**Autor:** Bsher Karbouj (TU Berlin)
