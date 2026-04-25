import numpy as np


def three_sigma_filter(input, sigma):
    """Use 3-sigma rule to detect outliers and replace them by mean.

    Args:
        input (list): 1D numeric signal.
        sigma (float): Sigma factor, usually 3.

    Returns:
        list: Filtered signal with same length as input.
    """
    # Convert to float64 for stable statistics
    signal = np.array(input, dtype=np.float64)
    if signal.size == 0:
        return []

    sigma = float(sigma)
    if not np.isfinite(sigma):
        raise ValueError("sigma must be a finite number")
    if sigma < 0:
        raise ValueError("sigma must be >= 0")

    # Compute robustly with population std
    mean = np.mean(signal)
    std = np.std(signal)
    if std == 0:
        return signal.tolist()

    # 3-sigma interval
    lower = mean - sigma * std
    upper = mean + sigma * std

    # Replace outliers by mean value
    output = signal.copy()
    mask = (signal < lower) | (signal > upper)
    output[mask] = mean
    return output.tolist()
