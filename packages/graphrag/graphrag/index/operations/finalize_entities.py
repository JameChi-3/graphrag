# Copyright (C) 2026 Microsoft
# Licensed under the MIT License

"""Stream-finalize entity rows into an output Table."""

from typing import Any
from uuid import uuid4

from graphrag_storage.tables.table import Table

from graphrag.data_model.schemas import ENTITIES_FINAL_COLUMNS


async def finalize_entities(
    entities_table: Table,
    degree_map: dict[str, int],
) -> list[dict[str, Any]]:
    """Read entity rows, enrich with degree, and write back.

    Streams through the entities table, deduplicates by title,
    assigns degree from the pre-computed degree map, and writes
    each finalized row back to the same table (safe when using
    truncate=True, which reads from the original and writes to
    a temp file).

    Args
    ----
        entities_table: Table
            Opened table for both reading input and writing output.
        degree_map: dict[str, int]
            Pre-computed mapping of entity title to node degree.

    Returns
    -------
        list[dict[str, Any]]
            Sample of up to 5 entity rows for logging.
    
    读取实体行，通过度值进行补充，然后写回原表。

    逐行处理实体表，按标题去重，从预计算的度映射中获取度值，
    并将每条处理后的行写回同一张表（当使用 truncate=True 时更安全，因为该方式从原表读取数据并写入临时文件）。

    参数
    ----
        entities_table: 表
            用于读取输入和写入输出的表。
        degree_map: dict[str, int]
            预计算的实体标题与节点度值的映射表。

    返回
    -------
        list[dict[str, Any]]
            最多5条实体行的样本数据，用于记录。
    """
    sample_rows: list[dict[str, Any]] = []
    seen_titles: set[str] = set()
    human_readable_id = 0

    async for row in entities_table:
        title = row.get("title")
        if not title or title in seen_titles:
            continue
        seen_titles.add(title)
        row["degree"] = degree_map.get(title, 0)
        row["human_readable_id"] = human_readable_id
        row["id"] = str(uuid4())
        human_readable_id += 1
        out = {col: row.get(col) for col in ENTITIES_FINAL_COLUMNS}
        await entities_table.write(out)
        if len(sample_rows) < 5:
            sample_rows.append(out)

    return sample_rows
