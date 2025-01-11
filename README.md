# Bottle Liquid and Cap Detection using OpenCV

This project uses OpenCV (`cv2`) to analyze images and detect:
1. The amount of liquid in a bottle (as a percentage of the total capacity).
2. Whether the bottle has a cap or not.

This solution is particularly useful for quality control in production lines or automation systems where liquid levels and cap presence need to be verified.

---

## Table of Contents
- [Features](#features)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Example Results](#example-results)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## Features

- **Liquid Level Detection**: Detects the height of the liquid in the bottle and calculates the percentage of liquid relative to the total bottle height.
- **Cap Detection**: Identifies whether a cap is present on the bottle.
- **Bounding Boxes**: Visualizes the detected liquid level, bottle boundaries, and cap presence on the image.

---

## How It Works

1. **Reference Image**: A reference image of a fully filled bottle is used to calculate the height of the cap and the total height of the bottle.
2. **Liquid Level Detection**: 
   - Converts the image to grayscale.
   - Applies Gaussian blur to reduce noise.
   - Uses the Canny edge detection algorithm to find edges.
   - Identifies the contour with the largest area to determine the liquid level.
3. **Cap Detection**:
   - Crops the top portion of the image based on the liquid height.
   - Processes the cropped region to detect the largest contour.
   - If the contour area is smaller than a predefined threshold, it determines the cap is missing.
4. **Output**: Displays the processed image with visual indicators (bounding boxes) and prints the results in the console.

---

## Requirements

The project requires the following:
- Python 3.8 or newer
- OpenCV

---

## Installation

