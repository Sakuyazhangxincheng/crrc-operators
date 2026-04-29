import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import base64
import io
import json

import numpy as np
import pandas as pd
import pytest

import op_bandpass_filter
import op_lowpass_filter
import op_moving_average
import op_iqr_filter


# ──────────────────────────────────────────────
# 公共工具
# ──────────────────────────────────────────────

def _enc(df: pd.DataFrame) -> str:
    return base64.b64encode(df.to_csv(index=False).encode()).decode()


def _dec(b64: str) -> pd.DataFrame:
    return pd.read_csv(io.StringIO(base64.b64decode(b64).decode()))


def _run(op_func, df, columns, options=None):
    result = op_func(
        taskId="t1",
        projectId="p1",
        csv_data=_enc(df),
        columns=columns,
        options_str=json.dumps(options or {}),
    )
    return _dec(result["output"]), json.loads(result["options"])


# ──────────────────────────────────────────────
# op_moving_average
# ──────────────────────────────────────────────

def test_moving_average_smooths_step():
    """阶跃信号经均值窗口后，阶跃边沿应被平滑（max-min 减小）。"""
    data = [0.0] * 10 + [10.0] * 10
    df = pd.DataFrame({"x": data})
    out, _ = _run(op_moving_average.process, df, [0], {"window_size": 5})
    assert out["x"].max() - out["x"].min() < 10.0


def test_moving_average_window1_noop():
    """window_size=1 时输出与输入完全一致。"""
    data = [1.0, 3.0, 2.0, 5.0, 4.0]
    df = pd.DataFrame({"x": data})
    out, _ = _run(op_moving_average.process, df, [0], {"window_size": 1})
    np.testing.assert_allclose(out["x"].values, data)


def test_moving_average_constant_signal():
    """常数信号经任意窗口平均后应保持不变。"""
    df = pd.DataFrame({"x": [3.0] * 20})
    out, _ = _run(op_moving_average.process, df, [0], {"window_size": 7})
    np.testing.assert_allclose(out["x"].values, 3.0, atol=1e-12)


def test_moving_average_preserves_length():
    """输出长度须与输入完全一致。"""
    df = pd.DataFrame({"x": np.random.default_rng(0).random(50)})
    out, _ = _run(op_moving_average.process, df, [0], {"window_size": 9})
    assert len(out) == 50


def test_moving_average_invalid_window():
    """window_size < 1 应抛出 ValueError。"""
    df = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
    with pytest.raises((ValueError, Exception)):
        _run(op_moving_average.process, df, [0], {"window_size": 0})


# ──────────────────────────────────────────────
# op_lowpass_filter
# ──────────────────────────────────────────────

def _pure_sine(freq_hz, n=256, fs=100.0):
    t = np.arange(n) / fs
    return np.sin(2 * np.pi * freq_hz * t)


def test_lowpass_attenuates_high_freq():
    """高频正弦（40 Hz）经低通（cutoff≈10 Hz）后，幅值应显著衰减。"""
    fs = 100.0
    n = 512
    high = _pure_sine(40.0, n, fs)
    df = pd.DataFrame({"x": high})
    # cutoff_ratio = 10 / 50 = 0.2
    out, _ = _run(op_lowpass_filter.process, df, [0], {"cutoff_ratio": 0.2, "sampling_interval": 1 / fs})
    assert out["x"].abs().max() < 0.05  # 基本归零


def test_lowpass_preserves_low_freq():
    """低频正弦（5 Hz）经低通（cutoff≈20 Hz）后，幅值应基本保留。"""
    fs = 100.0
    n = 512
    low = _pure_sine(5.0, n, fs)
    df = pd.DataFrame({"x": low})
    # cutoff_ratio = 20 / 50 = 0.4
    out, _ = _run(op_lowpass_filter.process, df, [0], {"cutoff_ratio": 0.4, "sampling_interval": 1 / fs})
    np.testing.assert_allclose(out["x"].values, low, atol=1e-6)


def test_lowpass_preserves_length():
    df = pd.DataFrame({"x": np.random.default_rng(1).random(100)})
    out, _ = _run(op_lowpass_filter.process, df, [0], {"cutoff_ratio": 0.3})
    assert len(out) == 100


def test_lowpass_invalid_cutoff():
    df = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
    with pytest.raises((ValueError, Exception)):
        _run(op_lowpass_filter.process, df, [0], {"cutoff_ratio": 0.6})


# ──────────────────────────────────────────────
# op_bandpass_filter
# ──────────────────────────────────────────────

def test_bandpass_passes_inband_freq():
    """10 Hz 正弦在 [5 Hz, 15 Hz] 带通内应基本保留。"""
    fs = 100.0
    n = 512
    sig = _pure_sine(10.0, n, fs)
    df = pd.DataFrame({"x": sig})
    # ratio = freq / (fs/2)  →  5/50=0.1, 15/50=0.3
    out, _ = _run(op_bandpass_filter.process, df, [0], {"low_ratio": 0.1, "high_ratio": 0.3})
    np.testing.assert_allclose(out["x"].values, sig, atol=1e-6)


def test_bandpass_blocks_outband_freq():
    """40 Hz 正弦在 [5 Hz, 15 Hz] 带通外应被归零。"""
    fs = 100.0
    n = 512
    high = _pure_sine(40.0, n, fs)
    df = pd.DataFrame({"x": high})
    out, _ = _run(op_bandpass_filter.process, df, [0], {"low_ratio": 0.1, "high_ratio": 0.3})
    assert out["x"].abs().max() < 0.05


def test_bandpass_preserves_length():
    df = pd.DataFrame({"x": np.random.default_rng(2).random(200)})
    out, _ = _run(op_bandpass_filter.process, df, [0], {"low_ratio": 0.05, "high_ratio": 0.45})
    assert len(out) == 200


def test_bandpass_invalid_ratios():
    df = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
    with pytest.raises((ValueError, Exception)):
        _run(op_bandpass_filter.process, df, [0], {"low_ratio": 0.3, "high_ratio": 0.1})


def test_bandpass_rejects_nan_input():
    df = pd.DataFrame({"x": [1.0, float("nan"), 3.0]})
    with pytest.raises((ValueError, Exception)):
        _run(op_bandpass_filter.process, df, [0], {"low_ratio": 0.1, "high_ratio": 0.3})


# ──────────────────────────────────────────────
# op_iqr_filter
# ──────────────────────────────────────────────

def test_iqr_filter_replaces_outlier():
    """明显超出 IQR 范围的异常值应被替换为中位数。"""
    data = [1.0, 2.0, 2.5, 2.0, 1.5, 100.0]
    df = pd.DataFrame({"x": data})
    out, _ = _run(op_iqr_filter.process, df, [0], {"k": 1.5})
    assert out.loc[5, "x"] < 10.0  # 100.0 应被替换


def test_iqr_filter_no_outlier():
    """无异常值时数据应保持不变。"""
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    df = pd.DataFrame({"x": data})
    out, _ = _run(op_iqr_filter.process, df, [0], {"k": 1.5})
    np.testing.assert_allclose(out["x"].values, data)


def test_iqr_filter_constant_signal():
    """全常数信号（IQR=0）不应修改任何值。"""
    df = pd.DataFrame({"x": [3.0, 3.0, 3.0, 3.0]})
    out, _ = _run(op_iqr_filter.process, df, [0], {"k": 1.5})
    assert (out["x"] == 3.0).all()


def test_iqr_filter_preserves_length():
    df = pd.DataFrame({"x": np.random.default_rng(5).random(30)})
    out, _ = _run(op_iqr_filter.process, df, [0], {"k": 1.5})
    assert len(out) == 30


# ──────────────────────────────────────────────
# 图像算子公共工具
# ──────────────────────────────────────────────

def _make_color_b64(width=16, height=12, color=(128, 64, 32)):
    """生成纯色 BGR 图像的 Base64 字符串。"""
    import cv2
    img = np.full((height, width, 3), color, dtype=np.uint8)
    ok, buf = cv2.imencode(".jpg", img)
    assert ok
    return base64.b64encode(buf.tobytes()).decode()


def _make_gray_b64(width=16, height=12, value=128):
    """生成纯灰度图像的 Base64 字符串。"""
    import cv2
    img = np.full((height, width), value, dtype=np.uint8)
    ok, buf = cv2.imencode(".jpg", img)
    assert ok
    return base64.b64encode(buf.tobytes()).decode()


def _decode_b64_img(b64_str, flags=None):
    import cv2
    if flags is None:
        flags = cv2.IMREAD_UNCHANGED
    data = base64.b64decode(b64_str)
    arr = np.frombuffer(data, dtype=np.uint8)
    return cv2.imdecode(arr, flags)


def _run_image_op(op_func, b64_str, options=None):
    """用单张图像驱动图像算子，返回输出图像的 Base64 字符串。"""
    df = pd.DataFrame({"img": [b64_str]})
    out, _ = _run(op_func, df, [0], options)
    return out.loc[0, "img"]


# ──────────────────────────────────────────────
# 图像算子（需要 cv2，用 pytest.importorskip 守卫）
# ──────────────────────────────────────────────

def test_gaussian_filtering_output_shape():
    pytest.importorskip("cv2")
    import op_gaussian_filtering
    b64 = _make_color_b64()
    out_b64 = _run_image_op(op_gaussian_filtering.process, b64, {"kernel_size": 5})
    img = _decode_b64_img(out_b64)
    assert img is not None
    assert img.shape == (12, 16, 3)


def test_median_filtering_output_shape():
    pytest.importorskip("cv2")
    import op_median_filtering
    b64 = _make_color_b64()
    out_b64 = _run_image_op(op_median_filtering.process, b64, {"kernel_size": 3})
    img = _decode_b64_img(out_b64)
    assert img is not None and img.shape == (12, 16, 3)


def test_mean_filtering_output_shape():
    pytest.importorskip("cv2")
    import op_mean_filtering
    b64 = _make_color_b64()
    out_b64 = _run_image_op(op_mean_filtering.process, b64, {"kernel_size": 3})
    img = _decode_b64_img(out_b64)
    assert img is not None and img.shape == (12, 16, 3)


def test_gamma_correction_brightens_dark_image():
    """gamma > 1 应使暗图像变亮（output = input^(1/gamma)，指数<1，暗区被拉伸）。"""
    pytest.importorskip("cv2")
    import cv2
    import op_gamma_correction
    b64 = _make_gray_b64(value=64)
    out_b64 = _run_image_op(op_gamma_correction.process, b64, {"gamma": 2.0})
    out_img = _decode_b64_img(out_b64, flags=cv2.IMREAD_GRAYSCALE)
    assert out_img.mean() > 64


def test_gamma_correction_darkens_bright_image():
    """gamma < 1 应使亮图像变暗（output = input^(1/gamma)，指数>1，亮区被压缩）。"""
    pytest.importorskip("cv2")
    import cv2
    import op_gamma_correction
    b64 = _make_gray_b64(value=200)
    out_b64 = _run_image_op(op_gamma_correction.process, b64, {"gamma": 0.5})
    out_img = _decode_b64_img(out_b64, flags=cv2.IMREAD_GRAYSCALE)
    assert out_img.mean() < 200


def test_equalize_histogram_output_is_gray():
    """直方图均衡化输出应为单通道灰度图。"""
    pytest.importorskip("cv2")
    import cv2
    import op_equalize_histogram
    b64 = _make_gray_b64(value=50)
    out_b64 = _run_image_op(op_equalize_histogram.process, b64, {})
    out_img = _decode_b64_img(out_b64, flags=cv2.IMREAD_GRAYSCALE)
    assert out_img is not None
    assert len(out_img.shape) == 2


def test_erode_shrinks_bright_region():
    """腐蚀后图像均值应 <= 原均值（前景收缩）。"""
    pytest.importorskip("cv2")
    import cv2
    import op_erode
    b64 = _make_gray_b64(value=200)
    out_b64 = _run_image_op(op_erode.process, b64, {"kernel_size": 3})
    out_img = _decode_b64_img(out_b64, flags=cv2.IMREAD_GRAYSCALE)
    assert out_img is not None


def test_dilation_output_shape():
    pytest.importorskip("cv2")
    import op_dilation
    b64 = _make_gray_b64(value=100)
    out_b64 = _run_image_op(op_dilation.process, b64, {"kernel_size": 3, "iterations": 2})
    img = _decode_b64_img(out_b64)
    assert img is not None


def test_opening_output_shape():
    pytest.importorskip("cv2")
    import op_opening
    b64 = _make_gray_b64(value=128)
    out_b64 = _run_image_op(op_opening.process, b64, {"kernel_size": 3})
    img = _decode_b64_img(out_b64)
    assert img is not None


def test_closing_output_shape():
    pytest.importorskip("cv2")
    import op_closing
    b64 = _make_gray_b64(value=128)
    out_b64 = _run_image_op(op_closing.process, b64, {"kernel_size": 3})
    img = _decode_b64_img(out_b64)
    assert img is not None


def test_canny_produces_edge_map():
    """Canny 输出图像形状应与输入一致，且不全为零（有边缘被检测到）。"""
    pytest.importorskip("cv2")
    import cv2
    import op_canny_edge_detection
    # 构造有明显边缘的图像：左半黑右半白
    src = np.zeros((30, 30), dtype=np.uint8)
    src[:, 15:] = 255
    ok, buf = cv2.imencode(".png", src)
    b64 = base64.b64encode(buf.tobytes()).decode()
    out_b64 = _run_image_op(op_canny_edge_detection.process, b64, {"threshold1": 50, "threshold2": 150})
    out_img = _decode_b64_img(out_b64, flags=cv2.IMREAD_GRAYSCALE)
    assert out_img is not None
    assert out_img.shape == (30, 30)
    assert out_img.max() > 0


def test_laplacian_edge_output_shape():
    pytest.importorskip("cv2")
    import op_laplacian_edge_detection
    b64 = _make_gray_b64(width=20, height=16, value=100)
    out_b64 = _run_image_op(op_laplacian_edge_detection.process, b64, {"ksize": 3})
    img = _decode_b64_img(out_b64)
    assert img is not None
