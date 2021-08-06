from typing import List

from sqlalchemy import Column, Date, Float, Integer, MetaData, String, Table

COLS_STR = {"date", "channel", "country", "os"}
METADATA = MetaData()
STATS = Table(
    "stats",
    METADATA,
    Column("date", Date, nullable=False),
    Column("channel", String(30), nullable=False),
    Column("country", String(2), nullable=False),
    Column("os", String(7), nullable=False),
    Column("impressions", Integer(), nullable=False),
    Column("clicks", Integer(), nullable=False),
    Column("installs", Integer(), nullable=False),
    Column("spend", Float(), nullable=False),
    Column("revenue", Float(), nullable=False),
)


def get_cols(table: Table, cols: List[str]) -> List[Column]:
    return [table.c.get(col) for col in cols]
