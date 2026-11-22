import numpy as np

from vc3_codec.types_and_constants import Int64Array, Int64OrArray


def fivepoint_endpoint(
    f0: Int64OrArray,
    f1: Int64OrArray,
    f2: Int64OrArray,
    f3: Int64OrArray,
    f4: Int64OrArray,
) -> Int64OrArray:
    return (25*f4 - 48*f3 + 36*f2 - 16*f1 + 3*f0) // 12

def encode_residuals(audio: Int64Array) -> tuple[Int64Array, Int64Array]:
    n = len(audio)
    if n <= 5:
        # nothing to compress
        seed = np.zeros(5, dtype=np.int64)
        seed[:n] = audio
        return seed, np.empty(0, dtype=np.int64)
    seed = audio[:5].copy()
    # approximate derivative with 5-point endpoint formula
    f4 = audio[4:n-1]
    f3 = audio[3:n-2]
    f2 = audio[2:n-3]
    f1 = audio[1:n-4]
    f0 = audio[0:n-5]
    derivatives = fivepoint_endpoint(f0, f1, f2, f3, f4)
    # find residual between calculated derivative and real difference
    differences = audio[5:] - f4
    residuals = derivatives - differences
    return seed, residuals

def decode_residuals(seed: Int64Array, residuals: Int64Array) -> Int64Array:
    n = len(seed) + len(residuals)
    audio = np.empty(n, dtype=np.int64)
    audio[:len(seed)] = seed
    for i in range(5, n):
        # reconstruct original audio by reversing residual calculation
        f0, f1, f2, f3, f4 = audio[i-5], audio[i-4], audio[i-3], audio[i-2], audio[i-1]
        derivative = fivepoint_endpoint(f0, f1, f2, f3, f4)
        difference = derivative - residuals[i-5]
        audio[i] = f4 + difference
    return audio
