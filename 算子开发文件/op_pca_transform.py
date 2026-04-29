import numpy as np
import pandas as pd
from core_wrapper import operator_wrapper


@operator_wrapper
def process(df, target_cols, options, context):
    """算子：PCA 降维（基于 SVD）

    将多列信号矩阵投影到主成分空间，输出列命名为 pc1, pc2, ...
    options:
        n_components (int): 保留主成分数，默认取 min(列数, 样本数)。
    """
    data = df[target_cols].dropna().to_numpy(dtype=np.float64)
    if data.size == 0:
        return pd.DataFrame(), context

    n_samples, n_features = data.shape
    n_components = int(options.get("n_components", min(n_features, n_samples)))
    n_components = min(n_components, n_features, n_samples)

    centered = data - np.mean(data, axis=0, keepdims=True)
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    components = vt[:n_components].T  # [n_features, n_components]
    transformed = centered @ components  # [n_samples, n_components]

    col_names = [f"pc{i + 1}" for i in range(n_components)]
    result_df = pd.DataFrame(transformed, columns=col_names)

    # 保留非目标列（如时间戳列）
    other_cols = [c for c in df.columns if c not in target_cols]
    if other_cols:
        other_df = df[other_cols].reset_index(drop=True).iloc[:len(result_df)]
        result_df = pd.concat([other_df, result_df], axis=1)

    return result_df, context
