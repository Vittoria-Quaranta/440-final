import sys
import wave
from tkinter import Tk, filedialog

import matplotlib.pyplot as plt
import numpy as np


def wav_to_points(file_path, downsample=1):
    """
    Parse a WAV file into an array of (time, amplitude) points.

    Args:
        file_path: Path to the .wav file
        downsample: Keep every Nth sample to reduce array size

    Returns:
        points: NumPy array of shape (N, 2)
                Column 0 = time (seconds)
                Column 1 = normalized amplitude (-1 to 1)
    """

    with wave.open(file_path, "rb") as wav:
        sample_rate = wav.getframerate()
        num_frames = wav.getnframes()
        num_channels = wav.getnchannels()
        sample_width = wav.getsampwidth()

        audio_data = wav.readframes(num_frames)

    # Convert raw bytes into numerical samples
    if sample_width == 1:
        audio = np.frombuffer(audio_data, dtype=np.uint8)
        audio = (audio.astype(np.float32) - 128) / 128

    elif sample_width == 2:
        audio = np.frombuffer(audio_data, dtype=np.int16)
        audio = audio.astype(np.float32) / 32768

    elif sample_width == 4:
        audio = np.frombuffer(audio_data, dtype=np.int32)
        audio = audio.astype(np.float32) / 2147483648

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
    print(points[:10])

    # Plot waveform
    plt.plot(points[:, 0], points[:, 1])
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Audio Waveform")
    plt.show()
