"""OpenBB + 量化学习 Day 1。

运行方式：.venv/bin/python demo1.py
本例使用无需 API Key 的 Fama-French 三因子月度数据。
"""

from importlib.metadata import version

import pandas as pd
from openbb import obb


def print_title(title: str) -> None:
    """打印清晰的小节标题。"""
    print(f"\n{'=' * 12} {title} {'=' * 12}")


def example_1_check_installation() -> None:
    """示例 1：确认 OpenBB 已安装并完成初始化。"""
    print_title("示例 1：检查安装")
    print(f"OpenBB 版本：{version('openbb')}")
    print(f"OpenBB 应用对象：{type(obb).__name__}")


def example_2_download_data() -> pd.DataFrame:
    """示例 2：通过 OpenBB 获取公开的 Fama-French 三因子数据。"""
    print_title("示例 2：获取金融数据")

    response = obb.famafrench.factors(
        region="america",       # 美国市场
        factor="3_factors",     # 市场、规模、价值三个因子
        frequency="monthly",    # 月度数据
        start_date="2024-01-01",
    )

    # OpenBB 返回 OBBject；可转换成最常用的 pandas DataFrame。
    data = response.to_dataframe()
    print(f"数据提供方：{response.provider}")
    print(f"数据行数：{len(data)}")
    print("\n最近 5 个月的数据（单位：%）：")
    print(data.tail())
    return data


def example_3_understand_dataframe(data: pd.DataFrame) -> None:
    """示例 3：认识量化研究最常用的数据结构 DataFrame。"""
    print_title("示例 3：认识 DataFrame")
    print(f"列名：{list(data.columns)}")
    print(f"日期范围：{data.index.min()} 至 {data.index.max()}")
    print("是否有缺失值：")
    print(data.isna().sum())
    print("""
字段含义：
  mkt_rf = 市场收益率 - 无风险利率（市场风险溢价）
  smb    = 小市值股票收益 - 大市值股票收益
  hml    = 价值股收益 - 成长股收益
  rf     = 无风险利率
""")


def example_4_basic_quant_analysis(data: pd.DataFrame) -> None:
    """示例 4：计算平均收益、波动率和累计收益。"""
    print_title("示例 4：第一次量化计算")

    # 原始值 2.5 代表 2.5%，计算前需除以 100。
    market_excess_return = data["mkt_rf"].dropna() / 100
    monthly_mean = market_excess_return.mean()

    # 月度指标年化：收益乘 12；波动率乘 sqrt(12)。
    annualized_return = monthly_mean * 12
    annualized_volatility = market_excess_return.std() * (12**0.5)
    sharpe_ratio = annualized_return / annualized_volatility

    # 累计收益使用复利，不能简单把每月收益相加。
    cumulative_return = (1 + market_excess_return).prod() - 1

    print(f"月均市场超额收益：{monthly_mean:.2%}")
    print(f"近似年化超额收益：{annualized_return:.2%}")
    print(f"年化波动率：      {annualized_volatility:.2%}")
    print(f"简化夏普比率：    {sharpe_ratio:.2f}")
    print(f"区间累计超额收益：{cumulative_return:.2%}")


def main() -> None:
    """按顺序运行第一天的四个示例。"""
    example_1_check_installation()

    try:
        data = example_2_download_data()
    except Exception as exc:
        print(f"\n数据下载失败：{exc}")
        print("请检查网络连接后重试；安装检查仍然有效。")
        return

    example_3_understand_dataframe(data)
    example_4_basic_quant_analysis(data)

    print_title("Day 1 完成")
    print("你已经完成：获取数据 → 查看数据 → 清洗数据 → 计算量化指标。")


if __name__ == "__main__":
    main()
