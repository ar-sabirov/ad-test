import asyncio
from datetime import date
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import create_async_engine

from db import init_db, select_smth, stats, cols_str
from metrics import all_metrics

app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
asyncio.gather(init_db(engine))


def check_args(**kwargs):
    col = kwargs.get("col")
    group_col = kwargs.get("group_col")
    metric = kwargs.get("metric")
    order_by = kwargs.get("order_by")

    all_cols = stats.c.keys()
    if col:
        assert all(
            [c in all_cols for c in col]
        ), f"Invalid columns {col}, Must be one of: {all_cols}"
    if group_col:
        assert all(
            [gc in cols_str for gc in group_col]
        ), f"Invalid group columns {group_col}. Must be one of {cols_str}"
    if metric:
        assert all(
            [m in all_metrics for m in metric]
        ), f"Invalid metrics {metric}. Must be one of {all_metrics}"
    if order_by:
        ordering_cols = all_cols + all_metrics
        assert (
            order_by in ordering_cols
        ), f"Invalid ordering {order_by}. Must be one of {ordering_cols}"


@app.get("/")
async def query_data(
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    col: Optional[List[str]] = Query([]),
    group_col: Optional[List[str]] = Query([]),
    metric: Optional[List[str]] = Query([]),
    order_by: Optional[str] = None,
    descending: bool = True,
) -> HTMLResponse:
    try:
        check_args(**locals())
    except AssertionError as e:
        return HTMLResponse(str(e), status_code=400)

    async with engine.connect() as conn:
        result = await select_smth(
            conn=conn,
            descending=descending,
            group_columns=group_col,
            metrics=metric,
            columns=col,
            order_by=order_by,
            date_from=date_from,
            date_to=date_to,
        )

    df = pd.DataFrame(result, columns=result.keys())
    return HTMLResponse(df.to_html())
