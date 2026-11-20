# WAV Audio Parser

## Overview
This Python script reads a `.wav` audio file and converts its waveform into an array of numerical points representing time and amplitude.

## Features
- Opens a file picker to select a `.wav` file.
- Reads audio data and extracts individual samples.
- Supports mono and stereo audio (stereo is averaged into mono).
- Allows downsampling to reduce the number of data points.
- Plots the resulting waveform using Matplotlib.

## Output Format
The parser returns a NumPy array containing two columns:

- **Column 1:** Time in seconds.
- **Column 2:** Audio amplitude (not normalized).

Each row represents one point in the audio waveform.

Example:
```python
[
    [0.00000, 0.12],
    [0.00023, 0.18],
    [0.00045, 0.25]
]
```

## Requirements
Install the required libraries:

```bash
pip install numpy matplotlib
```

The `wave` and `tkinter` modules are included with standard Python installations.

## How to Run
1. Open the project in VS Code.
2. Run the Python script.
3. Select a `.wav` file when the file picker appears.
4. The script parses the audio and generates an array of points.
5. A Matplotlib window displays the audio waveform.

## Downsampling
The `downsample` parameter controls how many audio samples are skipped.

For example:
```python
points = wav_to_points(file_path, downsample=10)
```

This keeps every tenth sample, reducing the array size by approximately 90%.

## Test File
`sample_test_tone.wav` is provided for testing. It contains a 3-second audio signal with 440 Hz and 880 Hz sine waves.
