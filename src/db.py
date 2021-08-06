import asyncio
import csv
from datetime import date
from typing import List, Optional

from sqlalchemy import (
    Column,
    Date,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    asc,
    desc,
    func,
)
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.future import select
from sqlalchemy.sql.expression import text

from metrics import metrics_map, agg_metrics_map
from table import stats, metadata

cols_str = ["date", "channel", "country", "os"]


async def inject_data(conn: AsyncConnection, table: Table):
    with open("../dataset.csv", "r") as fr:
        dr = csv.DictReader(fr)

        def convert(record):
            record["date"] = date.fromisoformat(record["date"])
            return record
        dr = [convert(r) for r in dr]

        await conn.execute(table.insert(), [i for i in dr])


def get_cols(table: Table, cols: List[str]) -> List[Column]:
    return [table.c.get(col) for col in cols]


async def select_smth(
    conn: AsyncConnection,
    descending: bool = True,
    group_columns: List[str] = [],
    metrics: List[str] = [],
    columns: Optional[List[str]] = None,
    order_by: Optional[str] = None,
    date_from: Optional[Date] = None,
    date_to: Optional[Date] = None,
):
    # take all columns if not given any
    if not columns:
        columns = [c.name for c in stats.columns]
    cols = get_cols(stats, columns)

    m_map = metrics_map
    if group_columns:
        m_map = agg_metrics_map
        cols = set(columns) - set(group_columns) - set(cols_str)
        cols = get_cols(stats, cols)
        cols = [func.sum(c).label(c.name) for c in cols]
        group_columns = get_cols(stats, group_columns)

    metrics = [m_map[m] for m in metrics]

    sel = select(*cols)
    sel = sel.add_columns(*group_columns)
    sel = sel.add_columns(*metrics)

    if date_to:
        sel = sel.where(stats.c.date <= date_to)
    if date_from:
        sel = sel.where(stats.c.date >= date_from)

    sel = sel.group_by(*group_columns)

    if order_by:
        ordering = desc if descending else asc
        sel = sel.order_by(ordering(text(order_by)))

    result = await conn.execute(sel)

    return result


async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
        await asyncio.gather(*[inject_data(conn, stats)])