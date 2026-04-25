import numpy as np


def bandpass_filter(input, low_ratio, high_ratio):
    """Band-pass filter in frequency domain for 1-D real signal.

    Args:
        input (list): 1-D signal.
        low_ratio (float): Lower cutoff in (0, 0.5).
        high_ratio (float): Upper cutoff in (low_ratio, 0.5).

    Returns:
        list: Filtered signal with same length as input.
    """
    signal = np.array(input, dtype=np.float64)
    n = signal.size
    if n == 0:
        return []

    low_ratio = float(low_ratio)
    high_ratio = float(high_ratio)
    if not (0 < low_ratio < high_ratio < 0.5):
        raise ValueError("require 0 < low_ratio < high_ratio < 0.5")
    if not np.all(np.isfinite(signal)):
        raise ValueError("input contains non-finite values")

    # FFT -> keep in-band bins -> IFFT.
    spectrum = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n, d=1.0)
    keep = (freqs >= low_ratio) & (freqs <= high_ratio)
    spectrum[~keep] = 0
    output = np.fft.irfft(spectrum, n=n)
    return output.tolist()
