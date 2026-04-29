# Session Log — Cursor / Codex / Claude Code 每次会话后追加记录

> 格式：`## YYYY-MM-DD HH:MM | Agent名`
> 然后 3-5 条要点：改动、结果、需要 Hermes 做什么

## 2026-04-28 18:20 | Cursor

- 改动：新建 `zxc-develop/` 目录（独立于 `算子开发文件/`）
- 第一批（3个信号算子）：`op_moving_average`, `op_lowpass_filter`, `op_bandpass_filter`
- 第二批（12个算子）：`op_iqr_filter`（信号）+ `image_utils.py`（图像公共工具）+ `op_gaussian_filtering`, `op_median_filtering`, `op_mean_filtering`, `op_gamma_correction`, `op_equalize_histogram`, `op_erode`, `op_dilation`, `op_opening`, `op_closing`, `op_canny_edge_detection`, `op_laplacian_edge_detection`（图像）
- 测试：`tests/test_new_operators.py` 共计约 35 个用例，涵盖全部算子
- 需要 Hermes：无；待 sakuya 在 WSL 终端 `cd zxc-develop && python -m pytest tests/ -v` 验证

