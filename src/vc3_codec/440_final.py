import sys
import wave
from tkinter import Tk, filedialog

import matplotlib.pyplot as plt
import numpy as np
from numpy._core import float64
from numpy._typing import NDArray


def wav_to_points(file_path, downsample=1):
    """
    Parse a WAV file into an array of (time, amplitude) points.

    Args:
        file_path: Path to the .wav file
        downsample: Keep every Nth sample to reduce array size

    Returns:
        points: NumPy array of shape (N, 2)
                Column 0 = time (seconds)
                Column 1 = raw amplitude (integer sample values, not normalized)
    """

    with wave.open(file_path, "rb") as wav:
        sample_rate = wav.getframerate()
        num_frames = wav.getnframes()
        num_channels = wav.getnchannels()
        sample_width = wav.getsampwidth()

        audio_data = wav.readframes(num_frames)

    # Convert raw bytes into numerical samples (no normalization)
    if sample_width == 1:
        # 8-bit WAV is unsigned (0-255); shift to be centered on 0
        audio = np.frombuffer(audio_data, dtype=np.uint8).astype(np.int16) - 128

    elif sample_width == 2:
        audio = np.frombuffer(audio_data, dtype=np.int16)

    elif sample_width == 4:
        audio = np.frombuffer(audio_data, dtype=np.int32)

    else:
        raise ValueError("Unsupported WAV sample width")

    # Reshape stereo/multichannel audio
    audio = audio.reshape(-1, num_channels)

    # Convert to mono by averaging channels
    audio = audio.mean(axis=1)

    # Downsample
    audio = audio[::downsample]

    # Generate time values
    times = np.arange(len(audio)) * downsample / sample_rate

    # Combine time and amplitude into points
    points = np.column_stack((times, audio))

    return points

def five_point_end_point(points, step: float):
    f0, f1, f2, f3, f4 = points
    return 1 / 12 / step * (-25 * f0 + 48 * f1 - 36 * f2 + 16 * f3 - 3 * f4)

def points_to_differences(points: NDArray[float64], sample_rate: int):
    _, audio = points.T
    audio = audio.copy() # don't modify original waveform
    if len(audio) < 5:
        # cannot do any differentiation
        return audio
    step = 1 / sample_rate
    queue: NDArray = audio[:5]
    for i in range(5, len(audio)):
        expected_diff = five_point_end_point(queue, step)
        np.delete(queue, 0)
        queue = np.append(queue, audio[i])
        actual_diff = queue[-1] - queue[-2]
        print(i)
        # audio[i] = expected_diff - actual_diff
        if expected_diff == actual_diff:
            print("perfect")
    print(audio[:50])


def main():

    # Open file selection window
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select a WAV audio file",
        filetypes=[("WAV files", "*.wav")]
    )

    root.destroy()

    if not file_path:
        print("No file selected.")
        sys.exit()

    # Parse selected audio file
    points = wav_to_points(file_path, downsample=10)

    print("Number of points:", len(points))
    print(points[:50])

    points_to_differences(points, 1 / (points[1] - points[0]))

    # Plot waveform
    plt.plot(points[:, 0], points[:, 1])
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude (raw sample value)")
    plt.title("Audio Waveform")
    plt.show()
