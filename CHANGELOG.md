# 📷 Wildlife Camera – Changelog

## v0.1 – Project Start
- Project idea defined: Automatic analysis of wildlife camera videos.
- Goal: Motion detection – identify which video shows a mammal.
- Chose Python as the programming language.
- Collected and labeled first sample images – tagged for motion/no motion and animal type.

## v0.2 – Data Access & Structure
- Script created to read image files from directory.

## v0.3 – Basic Motion Detection
- Implemented pixel-difference algorithm for image comparison.
- Output written to `videos_mit_bewegung.txt`.

## v0.4 – Improved Motion Detection
- Experimental adjustment of sensitivity threshold – tested various parameters with limited success.
- Reduced background noise (e.g. wind-blown leaves, light changes).
- Added filter to smooth difference images.

## v0.5 – Screenshot Extraction & Result Display
- Extracted a single frame from videos with detected motion.
- Saved extracted images in the `Screenshots` folder.

## v0.6 – Highlighting Motion
- Added green bounding box around detected moving object in extracted image.
- Simplifies identification of motion and what caused it.

## v0.7 – Day/Night Classification
- Analyzed average brightness of each frame.
- Classified images from videos as "Day" or "Night" and moved them to respective folders.
- Reason: Daytime videos have more false positives due to wind-related motion.

## v1.0 – Stable Release
- Gamechanger idea (user-developed):
  - Identify the largest deviation!
  - Compute mean from frames with **no motion** in the video.
  - Then find the frame with the greatest deviation from that minimum.
  - Detection rate nearly 100%.

## v1.1
- Added `ReadMe.md` with installation instructions and usage examples.
- Project released on GitHub.
