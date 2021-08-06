from sqlalchemy import func


def agg_cpi(table):
    return (func.sum(table.c.spend) / func.sum(table.c.installs)).label("CPI")


def cpi(table):
    return (table.c.spend / table.c.installs).label("CPI")


all_metrics = ["cpi"]
metrics_map = {"cpi": cpi}
agg_metrics_map = {"cpi": agg_cpi}
