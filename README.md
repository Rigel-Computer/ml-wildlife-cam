# Wild Camera Analysis: Motion Detection via Delta Comparison

This Python script is designed to automatically evaluate footage from wildlife cameras. It detects videos with significant motion—such as animals—and saves an enlarged snapshot of the most relevant moment from each video.

---

## 🔍 How It Works

Wild cameras generate a large number of videos, but only a few contain relevant events. The goal of this project is to **automatically identify** those videos that actually contain motion. To achieve this, the script uses an innovative approach:

> **Delta Frame Analysis**: Each frame is compared to the **average image** (mean frame) across the video. The frame with the **largest deviation** is assumed to show the most significant motion.

---

## 🧠 The Innovation: Delta to the Mean Frame

Unlike traditional frame differencing, this script calculates a **mean frame** (the average over all video frames). Each frame is then compared against this reference to highlight **when and where changes occur**. This approach is especially robust for nature scenes where wind or light changes may occur—but real movement stands out clearly.

---

## 📂 Directory Structure

The script expects the following directory structure:

```
.
├── videos/                   ← Original video files (e.g. .mp4, .avi)
├── snapshots/                ← Snapshot output folder
│   ├── tag/                  ← Snapshots for daytime videos
│   └── nacht/                ← Snapshots for nighttime videos
├── videos_mit_bewegung.txt   ← List of all videos with detected motion
├── Wildkamera_Snapshots_Sortiert.py ← Main script
```

---

## ⚙️ Steps Overview

1. **Load all videos** from `videos/`
2. **Brightness check** to distinguish day/night
3. **Compute mean frame** from all frames
4. **Find frame with maximum motion (delta)**
5. **Draw bounding box** on motion (optional)
6. **Enlarge image 2× and save as JPEG (quality 70)**
7. **Store in subfolder**: `snapshots/tag/` or `snapshots/nacht/`
8. **Log results** in `videos_mit_bewegung.txt`

---

## 🧰 Used Libraries

| Library         | Purpose                                  |
|----------------|-------------------------------------------|
| `opencv-python` | Video/image processing                    |
| `numpy`         | Mathematical operations, mean calculation |
| `os`            | File system operations                    |

> Install requirements with: `pip install opencv-python numpy`

---

## 📸 Example Images

Example outputs with bounding boxes are available here:

👉 https://www.rigel-computer.com/wildkamera

---

## 🧪 Supported Formats

- `.mp4`
- `.avi`
- `.mov`
- `.mkv`

---

## 👥 Audience

This project is suitable for:

- **Non-technical users** wanting to automate wildlife video review
- **Python developers** interested in motion detection methods

---

## 🚀 Future Features

Planned or possible enhancements:

- Heatmaps for motion intensity
- Batch logs with analytics
- Web dashboard for quick reviews

---

## 📄 License

MIT License — feel free to use and modify, but please give credit.

## 📄 Of course

This text was written with assistance of GenAI-Tools
