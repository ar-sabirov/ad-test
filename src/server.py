import asyncio
from datetime import date
from typing import Any, Dict, List, Optional

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import create_async_engine

from db import init_db, select_smth
from metrics import all_metrics
from table import COLS_STR, STATS

app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
asyncio.gather(init_db(engine))


def check_args(**kwargs: Dict[str, Any]) -> None:
    """Check query parameters to be valid 

    Raises:
        ValueError: Invalid query params
    """    
    col = kwargs.get("col")
    group_col = kwargs.get("group_col")
    metric = kwargs.get("metric")
    order_by = kwargs.get("order_by")

    all_cols = STATS.c.keys()
    if col and not all([c in all_cols for c in col]):
        msg = f"Invalid columns {col}, Must be one of: {all_cols}"
        raise ValueError(msg)

    if group_col and not all([gc in COLS_STR for gc in group_col]):
        msg = f"Invalid group columns {group_col}. Must be one of {COLS_STR}"
        raise ValueError(msg)

    if metric and not all([m in all_metrics for m in metric]):
        msg = f"Invalid metrics {metric}. Must be one of {all_metrics}"
        raise ValueError(msg)

    ordering_cols = all_cols + all_metrics
    if order_by and not (order_by in ordering_cols):
        msg = f"Invalid ordering {order_by}. Must be one of {ordering_cols}"
        raise ValueError(msg)


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
    except ValueError as e:
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
