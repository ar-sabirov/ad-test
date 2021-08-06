from sqlalchemy import Table, func


def agg_cpi(table: Table):
    """CPI to use in aggregation queries
    """    
    return (func.sum(table.c.spend) / func.sum(table.c.installs)).label("CPI")


def cpi(table: Table):
    """cpi = spend / installs
    """    
    return (table.c.spend / table.c.installs).label("CPI")


all_metrics = {"cpi"}
metrics_map = {"cpi": cpi}
agg_metrics_map = {"cpi": agg_cpi}
