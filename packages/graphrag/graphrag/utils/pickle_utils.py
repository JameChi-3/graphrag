# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""使用 pickle 保存和恢复 Python 对象。"""

import pickle
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


def pickle_save(obj: Any, file_path: str | Path) -> None:
    """将对象保存到二进制文件，自动创建父目录；文件已存在时覆盖。"""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as file:
        pickle.dump(obj, file, protocol=pickle.HIGHEST_PROTOCOL)


def pickle_load(file_path: str | Path) -> Any:
    """从可信的 pickle 文件恢复对象；读取或反序列化失败时抛出异常。"""
    with Path(file_path).open("rb") as file:
        return pickle.load(file)  # noqa: S301 - 仅加载来自可信来源的文件。


if __name__ == "__main__":
    # 示例：保存包含中文的字典，再从文件恢复；退出后自动清理临时文件。
    data = {"name": "知识图谱", "entities": ["实体 A", "实体 B"], "count": 2}
    with TemporaryDirectory() as temp_dir:
        example_path = Path(temp_dir) / "example.pkl"
        print(example_path)
        pickle_save(data, example_path)
        restored_data = pickle_load(example_path)
        print(restored_data)  # noqa: T201 - 展示示例的恢复结果。
