# Motion Detection Parameters – Wildlife Camera

This document explains the key parameters used in the motion detection algorithm of the wildlife camera project. The algorithm processes each video frame-by-frame, compares it to an average reference frame, and highlights significant motion. Different parameter settings are applied depending on whether the video is classified as "day" or "night" based on average brightness.

## Parameter Overview

| Parameter         | Value (Day/Night)              | Description                                                                 |
|------------------|--------------------------------|-----------------------------------------------------------------------------|
| `threshold`       | 20 / 15                        | Pixel intensity threshold for motion detection (binary threshold).          |
| `blur`            | (5, 5) / (3, 3)                | Kernel size for Gaussian blur, helps reduce noise before thresholding.     |
| `bewegung_pixel`  | 2000 / 1000                    | Minimum number of changed pixels to consider motion as significant.        |
| `NACHT_GRENZE`    | 50                             | Brightness value below which a video is considered "nighttime".            |
| frame cropping    | top 95% only                   | Bottom 5% of the image ignored to avoid motion artifacts (e.g., timestamp).|
| bounding box      | green rectangle                | Drawn around the largest detected contour of motion.                       |
| resize factor     | 2.0                            | Enlarges the result image for better visibility.                           |
| JPEG quality      | 70                             | Compression quality of the saved snapshot image.                           |

## Summary

The most influential parameters for detection accuracy are:

- **Threshold (`threshold`)**: Affects sensitivity to brightness changes. Lower values detect finer motion but may increase false positives.
- **Motion Pixel Count (`bewegung_pixel`)**: Defines the minimum amount of detected motion to be considered relevant. This filters out minor fluctuations.
- **Gaussian Blur (`blur`)**: Reduces noise that could lead to incorrect detection.
- **Brightness Threshold (`NACHT_GRENZE`)**: Dynamically switches between day/night settings, crucial for balancing sensitivity.

Together, these parameters ensure robust motion detection under varying lighting conditions and reduce false alarms caused by environmental effects like wind or shadows.

### Disclaimer

This info was summerized by the bot on base of the Python-Script Wildkamera_Snapshots_Sortiert.py