import numpy as np


def iqr_filter(input, k):
    """Use IQR rule to detect outliers and replace them by median.

    Args:
        input (list): 1D numeric signal.
        k (float): IQR factor, usually 1.5.

    Returns:
        list: Filtered signal with same length as input.
    """
    # Convert to float64 for stable quantile computation
    signal = np.array(input, dtype=np.float64)
    if signal.size == 0:
        return []

    k = float(k)
    if not np.isfinite(k):
        raise ValueError("k must be a finite number")
    if k < 0:
        raise ValueError("k must be >= 0")

    # Compute quartiles and IQR
    q1 = np.percentile(signal, 25)
    q3 = np.percentile(signal, 75)
    iqr = q3 - q1
    median = np.median(signal)

    # If all values are identical (or nearly so), nothing to filter
    if iqr == 0:
        return signal.tolist()

    lower = q1 - k * iqr
    upper = q3 + k * iqr

    # Replace outliers with robust center (median)
    output = signal.copy()
    mask = (signal < lower) | (signal > upper)
    output[mask] = median
    return output.tolist()
