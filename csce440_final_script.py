import wave
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog


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


if __name__ == "__main__":

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
        exit()

    # Parse selected audio file
    points = wav_to_points(file_path, downsample=10)

    print("Number of points:", len(points))
    print(points[:10])

    # Plot waveform
    plt.plot(points[:, 0], points[:, 1])
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude (raw sample value)")
    plt.title("Audio Waveform")
    plt.show()
