import numpy as np


def lowpass_filter(input, cutoff_ratio, sampling_interval=1.0):
    """Frequency-domain low-pass filter for 1D signals.

    Args:
        input (list): 1D time-domain signal.
        cutoff_ratio (float): Normalized cutoff in (0, 0.5).
        sampling_interval (float, optional): Sample spacing (default 1.0).

    Returns:
        list: Filtered signal with same length as input.
    """
    # Ensure numeric and stable dtype
    signal = np.array(input, dtype=np.float64)
    n = signal.size
    if n == 0:
        return []

    cutoff_ratio = float(cutoff_ratio)
    if not np.isfinite(cutoff_ratio) or cutoff_ratio <= 0 or cutoff_ratio >= 0.5:
        raise ValueError("cutoff_ratio must be in (0, 0.5)")

    sampling_interval = float(sampling_interval)
    if not np.isfinite(sampling_interval) or sampling_interval <= 0:
        raise ValueError("sampling_interval must be > 0")

    # Transform to frequency domain
    spectrum = np.fft.rfft(signal)

    # Keep low-frequency bins only; zero out high-frequency bins
    freqs = np.fft.rfftfreq(n, d=sampling_interval)
    nyquist = 0.5 / sampling_interval
    cutoff_hz = cutoff_ratio * nyquist
    spectrum[freqs > cutoff_hz] = 0

    # Transform back to time domain
    output = np.fft.irfft(spectrum, n=n)
    return output.tolist()
