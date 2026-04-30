import base64
import io
import json
from pathlib import Path

import pandas as pd

GLOBAL_CONTEXT = {}


def operator_wrapper(func):
    """
    符合《时序数据接口文档》的标准化算子包装器。
    与 算子开发文件/core_wrapper.py 保持同步。
    """

    def wrapper(taskId, projectId, csv_data=None, columns=None, options_str="{}", path=None):
        context_key = f"{projectId}_{taskId}"
        current_context = GLOBAL_CONTEXT.get(context_key, {})

        options = json.loads(options_str) if options_str else {}
        encoding = options.get("encoding", "utf-8")
        delimiter = options.get("delimiter", ",")
        has_header = options.get("has_header", True)
        header = 0 if has_header else None
        columns = columns or []

        try:
            if csv_data:
                csv_str = base64.b64decode(csv_data).decode(encoding)
                df = pd.read_csv(io.StringIO(csv_str), sep=delimiter, header=header)
            elif path:
                csv_path = Path(path)
                df = pd.read_csv(csv_path, sep=delimiter, encoding=encoding, header=header)
            else:
                raise ValueError("必须提供 csv_data 或 path 其中之一")
        except Exception as e:
            raise ValueError(f"CSV解码或解析失败: {e}")

        try:
            target_cols = [df.columns[i] for i in columns]
        except IndexError:
            raise IndexError("传入的 columns 序号超出了 CSV 的实际列数")

        runtime_context = dict(current_context)
        runtime_context["taskId"] = taskId
        runtime_context["projectId"] = projectId
        runtime_context["options"] = dict(options)

        processed_df, updated_context = func(df, target_cols, options, runtime_context)
        if updated_context is None:
            updated_context = runtime_context

        out_csv_str = processed_df.to_csv(index=False, sep=delimiter, header=has_header)
        output_b64 = base64.b64encode(out_csv_str.encode(encoding)).decode("utf-8")

        GLOBAL_CONTEXT[context_key] = updated_context

        return {"output": output_b64, "options": json.dumps(options)}

    return wrapper
