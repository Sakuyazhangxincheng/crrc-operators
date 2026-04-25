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

import op_detrend
import op_feature_band_energy
import op_feature_crest_factor
import op_feature_dominant_frequency
import op_feature_kurtosis
import op_feature_rms
import op_fill_missing
import op_fixed_time_window
import op_hanning_window
import op_linear_interpolate
import op_sliding_window
import op_timestamp_alignment
from core_wrapper import operator_wrapper


def _encode_df_to_b64(df: pd.DataFrame) -> str:
    csv_text = df.to_csv(index=False)
    return base64.b64encode(csv_text.encode("utf-8")).decode("utf-8")


def _decode_b64_to_df(payload_b64: str) -> pd.DataFrame:
    csv_text = base64.b64decode(payload_b64).decode("utf-8")
    return pd.read_csv(io.StringIO(csv_text))


def _run_operator(op_func, df: pd.DataFrame, columns, options=None):
    result = op_func(
        taskId="test-task",
        projectId="test-project",
        csv_data=_encode_df_to_b64(df),
        columns=columns,
        options_str=json.dumps(options or {}),
    )
    out_df = _decode_b64_to_df(result["output"])
    out_options = json.loads(result["options"])
    return out_df, out_options


def _make_test_image_b64(width=10, height=8) -> str:
    import cv2

    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[..., 0] = 32
    img[..., 1] = 128
    img[..., 2] = 224
    ok, buf = cv2.imencode(".jpg", img)
    assert ok
    return base64.b64encode(buf.tobytes()).decode("utf-8")


def _decode_image_b64(img_b64: str, flags=None):
    import cv2

    if flags is None:
        flags = cv2.IMREAD_UNCHANGED

    img_data = base64.b64decode(img_b64)
    arr = np.frombuffer(img_data, dtype=np.uint8)
    return cv2.imdecode(arr, flags)


def test_op_fill_missing_ffill():
    df = pd.DataFrame({"x": [1.0, np.nan, np.nan, 4.0]})
    out_df, _ = _run_operator(op_fill_missing.process, df, [0], {"method": "ffill"})
    assert out_df["x"].tolist() == [1.0, 1.0, 1.0, 4.0]


def test_op_linear_interpolate():
    df = pd.DataFrame({"x": [np.nan, 1.0, np.nan, 3.0, np.nan]})
    out_df, _ = _run_operator(op_linear_interpolate.process, df, [0], {})
    np.testing.assert_allclose(out_df["x"].values, np.array([1.0, 1.0, 2.0, 3.0, 3.0]))


def test_op_detrend_linear():
    x = np.arange(20, dtype=float)
    df = pd.DataFrame({"sig": 2.5 * x + 3.0})
    out_df, _ = _run_operator(op_detrend.process, df, [0], {"type": "linear"})
    y = out_df["sig"].to_numpy()
    slope, _ = np.polyfit(np.arange(len(y)), y, 1)
    assert abs(slope) < 1e-10
    assert abs(y.mean()) < 1e-10


def test_op_fixed_time_window():
    df = pd.DataFrame(
        {
            "ts": [
                "2026-03-25 10:00:00",
                "2026-03-25 10:01:00",
                "2026-03-25 10:02:00",
                "2026-03-25 10:03:00",
            ],
            "v": [1, 2, 3, 4],
        }
    )
    out_df, _ = _run_operator(
        op_fixed_time_window.process, df, [1], {"time_col_index": 0, "freq": "2min"}
    )
    assert out_df["window_id"].tolist() == [1, 2, 3, 4]


def test_op_sliding_window():
    df = pd.DataFrame({"v": [10, 20, 30, 40, 50]})
    out_df, _ = _run_operator(
        op_sliding_window.process, df, [0], {"window_size": 3, "step_size": 2}
    )
    assert out_df["v"].tolist() == [10, 20, 30, 30, 40, 50]
    assert out_df["window_id"].tolist() == [1, 1, 1, 2, 2, 2]


def test_op_timestamp_alignment():
    df = pd.DataFrame(
        {
            "ts": ["2026-03-25 10:00:00.000", "2026-03-25 10:00:00.200"],
            "v": [1.0, 3.0],
        }
    )
    out_df, _ = _run_operator(
        op_timestamp_alignment.process, df, [1], {"time_col_index": 0, "freq": "100ms"}
    )
    assert len(out_df) == 3
    assert pd.isna(out_df.loc[1, "v"])
    assert out_df.loc[0, "v"] == 1.0
    assert out_df.loc[2, "v"] == 3.0


def test_op_hanning_window():
    df = pd.DataFrame({"x": [1.0, 1.0, 1.0, 1.0]})
    out_df, _ = _run_operator(op_hanning_window.process, df, [0], {})
    np.testing.assert_allclose(out_df["x"].to_numpy(), np.hanning(4), rtol=1e-7, atol=1e-7)


def test_op_feature_rms():
    df = pd.DataFrame({"x": [3.0, 4.0]})
    out_df, _ = _run_operator(op_feature_rms.process, df, [0], {})
    expected = np.sqrt((3.0**2 + 4.0**2) / 2.0)
    assert abs(out_df.loc[0, "x_RMS"] - expected) < 1e-12


def test_op_feature_kurtosis():
    data = np.array([1.0, 2.0, 3.0, 7.0, 10.0])
    df = pd.DataFrame({"x": data})
    out_df, _ = _run_operator(op_feature_kurtosis.process, df, [0], {})
    expected = pd.Series(data).kurt()
    assert abs(out_df.loc[0, "x_Kurtosis"] - expected) < 1e-12


def test_op_feature_crest_factor():
    data = np.array([0.0, 1.0, 0.0, -1.0])
    df = pd.DataFrame({"x": data})
    out_df, _ = _run_operator(op_feature_crest_factor.process, df, [0], {})
    expected = np.max(np.abs(data)) / np.sqrt(np.mean(np.square(data)))
    assert abs(out_df.loc[0, "x_CrestFactor"] - expected) < 1e-12


def test_op_feature_dominant_frequency():
    fs = 100.0
    n = 200
    t = np.arange(n) / fs
    freq = 5.0
    x = np.sin(2 * np.pi * freq * t)
    df = pd.DataFrame({"x": x})
    out_df, _ = _run_operator(
        op_feature_dominant_frequency.process, df, [0], {"sampling_rate": fs}
    )
    assert abs(out_df.loc[0, "x_DomFreq"] - freq) < 0.2


def test_op_feature_band_energy():
    fs = 100.0
    n = 200
    t = np.arange(n) / fs
    x = np.sin(2 * np.pi * 5.0 * t)
    df = pd.DataFrame({"x": x})
    near_df, _ = _run_operator(
        op_feature_band_energy.process,
        df,
        [0],
        {"sampling_rate": fs, "f_min": 4.0, "f_max": 6.0},
    )
    far_df, _ = _run_operator(
        op_feature_band_energy.process,
        df,
        [0],
        {"sampling_rate": fs, "f_min": 20.0, "f_max": 30.0},
    )
    assert near_df.loc[0, "x_BandEnergy"] > far_df.loc[0, "x_BandEnergy"]


def test_op_image_gray_convert():
    import pytest

    pytest.importorskip("cv2")
    import op_image_gray_convert

    b64 = _make_test_image_b64()
    df = pd.DataFrame({"img": [b64]})
    out_df, _ = _run_operator(op_image_gray_convert.process, df, [0], {})
    out_img = _decode_image_b64(out_df.loc[0, "img"])
    assert out_img is not None
    assert len(out_img.shape) == 2


def test_op_image_resize():
    import pytest

    pytest.importorskip("cv2")
    import op_image_resize

    b64 = _make_test_image_b64(width=20, height=12)
    df = pd.DataFrame({"img": [b64]})
    out_df, _ = _run_operator(
        op_image_resize.process, df, [0], {"width": 7, "height": 5}
    )
    out_img = _decode_image_b64(out_df.loc[0, "img"])
    assert out_img is not None
    assert out_img.shape[1] == 7
    assert out_img.shape[0] == 5





def test_wrapper_supports_has_header_false():
    df = pd.DataFrame({"x": [1.0, 2.0], "y": [3.0, 4.0]})
    csv_no_header = df.to_csv(index=False, header=False)
    csv_data = base64.b64encode(csv_no_header.encode("utf-8")).decode("utf-8")
    result = op_linear_interpolate.process(
        taskId="header-task",
        projectId="header-project",
        csv_data=csv_data,
        columns=[0, 1],
        options_str=json.dumps({"has_header": False}),
    )
    csv_text = base64.b64decode(result["output"]).decode("utf-8")
    out_df = pd.read_csv(io.StringIO(csv_text), header=None)
    np.testing.assert_allclose(
        out_df.to_numpy(dtype=float), np.array([[1.0, 3.0], [2.0, 4.0]])
    )


def test_wrapper_supports_path_input():
    csv_path = ROOT / "tests" / "_path_input.csv"
    csv_path.write_text("a,b\n1,2\n3,4\n", encoding="utf-8")
    try:
        result = op_fill_missing.process(
            taskId="path-task",
            projectId="path-project",
            path=str(csv_path),
            columns=[0, 1],
            options_str=json.dumps({}),
        )
        out_df = _decode_b64_to_df(result["output"])
        assert out_df.shape == (2, 2)
        assert out_df["a"].tolist() == [1, 3]
        assert out_df["b"].tolist() == [2, 4]
    finally:
        if csv_path.exists():
            csv_path.unlink()


def test_wrapper_injects_context_fields():
    @operator_wrapper
    def _ctx_op(df, target_cols, options, context):
        assert context["taskId"] == "ctx-task"
        assert context["projectId"] == "ctx-project"
        assert context["options"]["custom"] == 123
        context["seen"] = True
        return df, context

    df = pd.DataFrame({"v": [1, 2, 3]})
    _ctx_op(
        taskId="ctx-task",
        projectId="ctx-project",
        csv_data=_encode_df_to_b64(df),
        columns=[0],
        options_str=json.dumps({"custom": 123}),
    )



