"""5.4 因子与资产定价：三/五因子、动量、反转与特征组合收益。"""
from openbb import obb
from _common import OUTPUT, fetch, run


def factors(factor):
    data = fetch(f"ff_{factor}", obb.famafrench.factors, region="america",
                 factor=factor, frequency="monthly", start_date="2020-01-01")
    if data is not None and "mkt_rf" in data.columns:
        # 原始 2.5 表示 2.5%；市场总收益 = 市场超额收益 + 无风险收益。
        returns = data[["mkt_rf", "rf"]].dropna().sort_index() / 100
        market = returns["mkt_rf"] + returns["rf"]
        print(f"月均市场风险溢价：{returns['mkt_rf'].mean():.2%}")
        print(f"市场总收益区间复利：{(1 + market).prod() - 1:.2%}")
        returns.to_csv(OUTPUT / f"ff_{factor}_decimal.csv")
    # 回归时：因变量为资产收益减 rf，自变量为匹配日期/频率的因子。


def portfolios():
    fetch("ff_size_portfolios", obb.famafrench.us_portfolio_returns,
          portfolio="portfolios_formed_on_me", measure="value", frequency="monthly",
          start_date="2020-01-01")


if __name__ == "__main__":
    examples = {factor: lambda factor=factor: factors(factor)
                for factor in ["3_factors", "5_factors", "momentum", "st_reversal", "lt_reversal"]}
    run({**examples, "portfolios": portfolios})
