import numpy as np


def pca_transform(input, n_components):
    """对样本矩阵执行 PCA 降维（基于 SVD 实现）。

    Args:
        input (list | list[list]): 输入样本。推荐二维形状 [n_samples, n_features]。
        n_components (int): 保留主成分个数，必须大于等于 1。

    Returns:
        list[list]: 降维后的样本矩阵，形状为 [n_samples, n_components]。
    """
    data = np.array(input, dtype=np.float64)
    if data.size == 0:
        return []
    if not np.all(np.isfinite(data)):
        raise ValueError("input contains NaN or Inf")

    # 兼容一维输入：视为单特征样本序列
    if data.ndim == 1:
        data = data.reshape(-1, 1)
    elif data.ndim != 2:
        raise ValueError("input must be 1D or 2D")

    n_components = int(n_components)
    if n_components < 1:
        raise ValueError("n_components must be >= 1")

    n_samples, n_features = data.shape
    if n_samples == 0 or n_features == 0:
        return []

    # 主成分数量不超过特征维度
    n_components = min(n_components, n_features)

    # 去中心化
    centered = data - np.mean(data, axis=0, keepdims=True)

    # SVD 分解：centered = U * S * Vt
    # Vt 的前 n_components 行对应主方向
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    components = vt[:n_components].T  # [n_features, n_components]

    # 投影到主成分子空间
    transformed = centered @ components  # [n_samples, n_components]
    return transformed.tolist()
