import sys

import numpy as np

from vc3_codec.compression import compress, decompress
from vc3_codec.numerical_analysis import decode_residuals, encode_residuals
from vc3_codec.vc3 import read_vc3, write_vc3
from vc3_codec.wav import read_wav, write_wav


def wav_to_vc3(source: str, destination: str):
    header, audios = read_wav(source)
    seeds = np.empty((header.n_channels, 5), dtype=np.int64)
    residualss = []
    for i in range(header.n_channels):
        seed, residuals = encode_residuals(audios[:, i])
        seeds[i] = seed
        residualss.append(residuals)
    residualss = np.concatenate(residualss)
    packed = compress(residualss, header.samp_width)
    write_vc3(destination, header, seeds, packed)

def vc3_to_wav(source: str, destination: str):
    result = read_vc3(source)
    if result is None:
        return
    header, seeds, packed = result
    residualss = decompress(packed, header.samp_width)
    n_residual = max(header.n_frames - 5, 0)
    audios = np.empty((header.n_frames, header.n_channels), dtype=np.int64)
    for i in range(header.n_channels):
        residuals = residualss[i*n_residual : (i+1)*n_residual]
        audios[:, i] = decode_residuals(seeds[i], residuals)[:header.n_frames]
    write_wav(destination, header, audios)

def encode():
    if len(sys.argv) != 3:
        print("bad args; need input.wav output.vc3")
        return
    wav_to_vc3(sys.argv[1], sys.argv[2])

def decode():
    if len(sys.argv) != 3:
        print("bad args; need input.vc3 output.wav")
        return
    vc3_to_wav(sys.argv[1], sys.argv[2])
