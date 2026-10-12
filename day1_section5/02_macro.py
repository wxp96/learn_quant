"""5.2 宏观：通过 FRED series ID 获取美国及跨国指标。需要 FRED Key。"""
import os
from openbb import obb
from _common import fetch, run

# 也可预先在 OpenBB 用户配置中设置 fred_api_key；不打印凭证。
if os.getenv("FRED_API_KEY"):
    obb.user.credentials.fred_api_key = os.environ["FRED_API_KEY"]

# 各序列保留原始频率与单位，不将 GDP 季度值强行拼成月度值。
SERIES = {
    "gdp": ("GDP", "美国名义 GDP，季度，十亿美元，年率"),
    "cpi": ("CPIAUCSL", "CPI，月度，指数"),
    "pce": ("PCEPI", "PCE 价格指数，月度，指数"),
    "unemployment": ("UNRATE", "失业率，月度，百分比"),
    "payrolls": ("PAYEMS", "非农就业人数，月度，千人；并非新增人数"),
    "policy_rate": ("FEDFUNDS", "有效联邦基金利率，月度，百分比"),
    "treasury": ("DGS10", "10 年期国债收益率，日度，百分比"),
    "production": ("INDPRO", "工业生产，月度，指数"),
    "retail": ("RSAFS", "零售销售，月度，百万美元"),
    "china_gdp": ("MKTGDPCNA646NWDB", "中国 GDP，年度，现价美元；与美国季度年率口径不同"),
}


def download(name):
    symbol, description = SERIES[name]
    print(description)
    fetch(f"macro_{name}", obb.fred.economy.fred_series,
          symbol=symbol, start_date="2020-01-01")
    # 当前历史值可能已修订，不能直接当作历史时点已知值回测。


if __name__ == "__main__":
    run({name: lambda name=name: download(name) for name in SERIES})
