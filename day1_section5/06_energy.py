"""5.6 能源与商品：EIA 库存、JODI 供需、原油期货持仓。"""
import os
from openbb import obb
from _common import fetch, run

if os.getenv("EIA_API_KEY"):
    obb.user.credentials.eia_api_key = os.environ["EIA_API_KEY"]


def oil_stocks():
    # 商业原油库存，不包含战略石油储备 SPR；查看返回的单位字段。
    fetch("eia_oil_stocks", obb.eia.petroleum.stocks.weekly_stocks,
          product="crude_oil", process="ending_stocks_excluding_spr", region="us",
          start_date="2024-01-01", sort="desc", limit=52)


def gas_stocks():
    fetch("eia_gas_stocks",
          obb.eia.natural_gas.storage.weekly_working_gas_in_underground_storage,
          series="weekly_lower_48_states_natural_gas_working_underground",
          start_date="2024-01-01", sort="desc", limit=52)


def balance():
    # 无需 Key。产量、进口、出口、炼厂活动等流量用千桶/日表示。
    # JODI 首次可能下载较大的源表；库存水平另用 kbbl（千桶）。
    fetch("jodi_us_oil_balance", obb.jodi.oil.balance,
          country="US", product="crude_oil", unit="kbd", start_date="2024-01-01")


def production():
    fetch("jodi_oil_production", obb.jodi.oil.production,
          country="US,SA", product="crude_oil", unit="kbd", start_date="2024-01-01")


def stocks():
    fetch("jodi_oil_stocks", obb.jodi.oil.stocks,
          country="US", product="crude_oil", unit="kbbl", start_date="2024-01-01")


def positioning():
    # NYMEX WTI 原油；managed_money_* 列可用于研究资金持仓。
    fetch("wti_cot", obb.cftc.cot, code="067651", report_type="disaggregated",
          futures_only=True, measure="positions", limit=8)


if __name__ == "__main__":
    run({"balance": balance, "production": production, "stocks": stocks,
         "oil_stocks": oil_stocks, "gas_stocks": gas_stocks, "positioning": positioning})
