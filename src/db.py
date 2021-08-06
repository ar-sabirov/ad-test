import asyncio
import csv
from datetime import date
from typing import List, Optional

from sqlalchemy import Column, Date, Table, asc, desc, func
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.future import select
from sqlalchemy.sql.expression import text

from metrics import agg_metrics_map, metrics_map
from table import COLS_STR, METADATA, STATS, get_cols


async def inject_data(conn: AsyncConnection, table: Table) -> None:
    with open("../dataset.csv", "r") as fr:
        dr = csv.DictReader(fr)

        def convert(record):
            record["date"] = date.fromisoformat(record["date"])
            return record

        dr = [convert(r) for r in dr]

        await conn.execute(table.insert(), [i for i in dr])


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
        columns = [c.name for c in STATS.columns]
    cols = get_cols(STATS, columns)

    m_map = metrics_map
    if group_columns:
        m_map = agg_metrics_map
        cols = set(columns) - set(group_columns) - set(COLS_STR)
        cols = get_cols(STATS, cols)
        cols = [func.sum(c).label(c.name) for c in cols]
        group_columns = get_cols(STATS, group_columns)

    metrics = [m_map[m](STATS) for m in metrics]

    sel = select(*cols)
    sel = sel.add_columns(*group_columns)
    sel = sel.add_columns(*metrics)

    if date_to:
        sel = sel.where(STATS.c.date <= date_to)
    if date_from:
        sel = sel.where(STATS.c.date >= date_from)

    sel = sel.group_by(*group_columns)

    if order_by:
        ordering = desc if descending else asc
        sel = sel.order_by(ordering(text(order_by)))

    result = await conn.execute(sel)

    return result


async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(METADATA.create_all)
        await asyncio.gather(*[inject_data(conn, STATS)])
