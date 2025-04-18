
import cv2
import os
import numpy as np

# Ordner mit Videos
VIDEO_DIR = "videos"
# Basisordner für Vorschaubilder
SNAPSHOT_DIR = "snapshots"
SNAPSHOT_TAG = os.path.join(SNAPSHOT_DIR, "tag")
SNAPSHOT_NACHT = os.path.join(SNAPSHOT_DIR, "nacht")
# Datei für Ergebnisliste
OUTPUT_FILE = "videos_mit_bewegung.txt"

# Parameter für Tag-/Nachtunterscheidung
NACHT_GRENZE = 50
PARAMS_NACHT = {"threshold": 15, "blur": (3, 3), "bewegung_pixel": 1000}
PARAMS_TAG = {"threshold": 20, "blur": (5, 5), "bewegung_pixel": 2000}

# Ergebnisliste
videos_mit_bewegung = []

# Vorschaubild-Ordner vorbereiten
for ordner in [SNAPSHOT_DIR, SNAPSHOT_TAG, SNAPSHOT_NACHT]:
    if not os.path.exists(ordner):
        os.makedirs(ordner)

def get_parameter_by_brightness(helligkeit):
    return PARAMS_NACHT if helligkeit < NACHT_GRENZE else PARAMS_TAG

def get_snapshot_subdir_by_brightness(helligkeit):
    return SNAPSHOT_NACHT if helligkeit < NACHT_GRENZE else SNAPSHOT_TAG

def bild_mit_maximalem_delta_zum_mittelwert(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Video kann nicht geöffnet werden: {video_path}")

    frames = []
    helligkeitswerte = []

    # 1. Alle Frames einlesen
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            break
        frames.append(frame)
        helligkeit = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).mean()
        helligkeitswerte.append(helligkeit)

    cap.release()

    if len(frames) < 2:
        raise RuntimeError(f"Zu wenig gültige Frames in: {video_path}")

    # 2. Helligkeit im Mittel
    durchschnitt_helligkeit = sum(helligkeitswerte) / len(helligkeitswerte)
    params = get_parameter_by_brightness(durchschnitt_helligkeit)
    snapshot_subdir = get_snapshot_subdir_by_brightness(durchschnitt_helligkeit)

    # 3. Mittelbild berechnen
    mittelbild = np.mean([f.astype(np.float32) for f in frames], axis=0).astype(np.uint8)

    # 4. Vergleich jedes Frames mit dem Mittelbild
    max_delta = 0
    best_frame = None
    best_thresh = None

    for frame in frames:
        diff = cv2.absdiff(mittelbild, frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, params["blur"], 0)
        _, thresh = cv2.threshold(blur, params["threshold"], 255, cv2.THRESH_BINARY)

        # Unteren Bereich abschneiden (untere 5 % ignorieren)
        höhe = thresh.shape[0]
        grenze = int(höhe * 0.95)
        maske = thresh[:grenze, :]

        bewegung_pixel = cv2.countNonZero(maske)

        if bewegung_pixel > max_delta:
            max_delta = bewegung_pixel
            best_frame = frame.copy()
            best_thresh = thresh.copy()

    # 5. Speichern, wenn nennenswerte Abweichung
    if best_frame is not None and max_delta > params["bewegung_pixel"]:
        # Nur obere 95 % zur Konturenerkennung verwenden
        höhe = best_thresh.shape[0]
        grenze = int(höhe * 0.95)
        maskiert = best_thresh[:grenze, :]

        contours, _ = cv2.findContours(maskiert, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            größte_kontur = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(größte_kontur)
            cv2.rectangle(best_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Bild auf doppelten Maßstab vergrößern
        vergroessert = cv2.resize(best_frame, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)

        snapshot_path = os.path.join(snapshot_subdir, os.path.basename(video_path) + "_maxdelta.jpg")
        cv2.imwrite(snapshot_path, vergroessert, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        return True
    else:
        return False

# Hauptlauf
alle_videos = sorted(
    [
        f
        for f in os.listdir(VIDEO_DIR)
        if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))
    ]
)

for filename in alle_videos:
    video_path = os.path.join(VIDEO_DIR, filename)
    print(f"Prüfe: {filename}")
    try:
        if bild_mit_maximalem_delta_zum_mittelwert(video_path):
            print(f"Bewegung erkannt: {filename}")
            videos_mit_bewegung.append(filename)
        else:
            print(f"Keine signifikante Bewegung: {filename}")
    except Exception as e:
        print(f"Fehler bei {filename}: {e}")

# Ergebnisdatei schreiben
try:
    with open(OUTPUT_FILE, "w") as f:
        for name in videos_mit_bewegung:
            f.write(name + "\n")
except Exception as e:
    print(f"Fehler beim Schreiben der Ergebnisdatei: {e}")

# Zusammenfassung
anzahl_gesamt = len(alle_videos)
anzahl_erkannt = len(videos_mit_bewegung)
prozentsatz = round((anzahl_erkannt / anzahl_gesamt) * 100, 1) if anzahl_gesamt > 0 else 0

print("\nAnalyse abgeschlossen.")
print(f"Ergebnisdatei: {OUTPUT_FILE}")
print(f"Vorschaubilder Tag: {SNAPSHOT_TAG}/")
print(f"Vorschaubilder Nacht: {SNAPSHOT_NACHT}/")
print(f"Erkannte Bewegung in {anzahl_erkannt} von {anzahl_gesamt} Videos ({prozentsatz:.1f} %).")
