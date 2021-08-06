from table import stats
from sqlalchemy import func

def agg_cpi():
    return (func.sum(stats.c.spend) / func.sum(stats.c.installs)).label("CPI")

def cpi():
    return (stats.c.spend / stats.c.installs).label("CPI")

all_metrics = ['cpi']
metrics_map = {"cpi": cpi()}
agg_metrics_map = {"cpi": agg_cpi()}



