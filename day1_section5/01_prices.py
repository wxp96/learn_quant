"""5.1 股票与指数行情：历史价格、收益率、波动率、比较与均线。"""
import pandas as pd
from _common import OUTPUT, fetch, run
from openbb import obb

START = "2024-01-01"
# 在这里添加你想研究的股票或 ETF，每个 symbol 独立回测。
SYMBOLS = ["AAPL", "SPY", "QQQ"]
MOMENTUM_DAYS = 20
INITIAL_CASH = 10_000
COST_BPS = 5  # 每次买入/卖出的手续费与滑点假设，5 基点 = 0.05%；可改为 0。
USE_CACHED_PRICES = False  # True：优先读取 output 中已下载的行情，方便反复练习。


def prices():
    # ETF 也使用 equity.historical；close 不能默认视为含分红复权价。
    data = fetch("aapl_prices", obb.cboe.equity.historical,
                 symbol="AAPL", start_date=START, interval="1d")
    if data is None:
        return
    data = data.sort_index()
    close = pd.to_numeric(data["close"], errors="coerce")
    data["return"] = close.pct_change(fill_method=None)
    data["ma20"] = close.rolling(20).mean()
    data["ma60"] = close.rolling(60).mean()
    data["momentum20"] = close.pct_change(20, fill_method=None)
    # 今天的收盘信号只能供之后交易使用，shift(1) 避免同日使用未来信息。
    data["previous_signal"] = (data["ma20"] > data["ma60"]).shift(1)
    print(data.tail())
    print(f"日收益率年化波动率：{data['return'].std() * 252**0.5:.2%}")
    data.to_csv(OUTPUT / "aapl_indicators.csv")


def compare():
    series = []
    for symbol in ["SPY", "QQQ"]:
        data = fetch(f"{symbol.lower()}_prices", obb.cboe.equity.historical,
                     symbol=symbol, start_date=START)
        if data is not None:
            # 上游可能重复返回同一天的记录；日期索引唯一才能按日合并。
            original_rows = len(data)
            date_name = data.index.name or "index"
            data = data.reset_index().drop_duplicates().set_index(date_name)
            if len(data) < original_rows:
                print(f"{symbol}：移除 {original_rows - len(data)} 条完全重复记录")
            if data.index.has_duplicates:
                raise ValueError(f"{symbol} 同一日期存在不同记录，请检查原始 CSV")
            series.append(data["close"].sort_index().rename(symbol))
    if len(series) == 2:
        aligned = pd.concat(series, axis=1).dropna()
        if not aligned.empty:
            normalized = aligned / aligned.iloc[0] * 100
            print("共同起点设为 100，比较价格变化（不含分红）：")
            print(normalized.tail())
            normalized.to_csv(OUTPUT / "etf_comparison.csv")


def index():
    fetch("vix_index", obb.cboe.index.historical, symbol="VIX", start_date=START)


def backtest_momentum(data, lookback=MOMENTUM_DAYS, cost_bps=COST_BPS):
    """昨日动量 > 0，今日开盘全仓；否则今日开盘空仓。不做空、不加杠杆。"""
    if lookback < 1 or not 0 <= cost_bps < 10_000:
        raise ValueError("动量周期必须为正数，交易成本必须在 [0, 10000) 基点内")
    data = data.copy()
    data.index = pd.to_datetime(data.index)
    date_name = data.index.name or "date"
    data.index.name = date_name
    data = data.reset_index().drop_duplicates().set_index(date_name).sort_index()
    if data.index.has_duplicates:
        raise ValueError("同一天存在不同记录，请先检查原始行情")
    for column in ["open", "close"]:
        data[column] = pd.to_numeric(data[column], errors="raise")
        if data[column].isna().any() or (data[column] <= 0).any():
            raise ValueError(f"{column} 包含缺失值或非正价格，不能直接回测")

    data["momentum"] = data["close"].pct_change(lookback, fill_method=None)
    data["previous_momentum"] = data["momentum"].shift(1)
    data["previous_close"] = data["close"].shift(1)
    # 等待完整的动量窗口；两种策略都从同一天开盘开始，保证比较起点一致。
    data = data.loc[data["previous_momentum"].notna()].copy()
    if data.empty:
        raise ValueError(f"至少需要 {lookback + 2} 行行情")
    data["position"] = (data["previous_momentum"] > 0).astype(int)
    data["previous_position"] = data["position"].shift(1, fill_value=0)
    data["turnover"] = (data["position"] - data["previous_position"]).abs()
    data["overnight_return"] = data["open"] / data["previous_close"] - 1
    data["intraday_return"] = data["close"] / data["open"] - 1
    cost = cost_bps / 10_000
    # 昨日持仓承担隔夜涨跌 → 今日开盘调仓并扣成本 → 今日持仓承担日内涨跌。
    # 卖出当天仍承担卖出之前的隔夜收益，不能简单 position * close.pct_change()。
    data["strategy_return"] = (
        (1 + data["previous_position"] * data["overnight_return"])
        * (1 - data["turnover"] * cost)
        * (1 + data["position"] * data["intraday_return"])
        - 1
    )
    data["buy_hold_return"] = data["close"].pct_change(fill_method=None)
    data.iloc[0, data.columns.get_loc("buy_hold_return")] = (
        (1 - cost) * data["close"].iloc[0] / data["open"].iloc[0] - 1
    )
    for name in ["strategy", "buy_hold"]:
        data[f"{name}_equity"] = INITIAL_CASH * (1 + data[f"{name}_return"]).cumprod()
    return data


def momentum_compare():
    """批量比较动量择时与买入持有，保存逐日明细和汇总。"""
    rows = []
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for symbol in SYMBOLS:
        try:
            cache = OUTPUT / f"{symbol.lower()}_prices.csv"
            if USE_CACHED_PRICES and cache.exists():
                print(f"读取本地行情：{cache}（不会更新最新日期）")
                data = pd.read_csv(cache, index_col=0)
            else:
                data = fetch(f"{symbol.lower()}_prices", obb.cboe.equity.historical,
                             symbol=symbol, start_date=START, interval="1d")
            if data is None:
                continue
            data.index = pd.to_datetime(data.index)
            data = data.loc[data.index >= pd.Timestamp(START)]
            result = backtest_momentum(data)
            result.to_csv(OUTPUT / f"{symbol.lower()}_momentum_backtest.csv")
            row = {"symbol": symbol, "start": result.index[0].date(),
                   "end": result.index[-1].date(), "days": len(result),
                   "trades": int(result["turnover"].sum()),
                   "holding_fraction": result["position"].mean()}
            for name in ["strategy", "buy_hold"]:
                equity = result[f"{name}_equity"]
                # 初始资金也参与峰值计算，避免忽略第一天的亏损。
                peak = equity.cummax().clip(lower=INITIAL_CASH)
                row[f"{name}_return"] = equity.iloc[-1] / INITIAL_CASH - 1
                row[f"{name}_max_drawdown"] = (equity / peak - 1).min()
                row[f"{name}_final_value"] = equity.iloc[-1]
            row["excess_return"] = row["strategy_return"] - row["buy_hold_return"]
            rows.append(row)
            print(f"{symbol}：动量 {row['strategy_return']:.2%}，"
                  f"买入持有 {row['buy_hold_return']:.2%}，"
                  f"收益差 {row['excess_return']:.2%}，买卖合计 {row['trades']} 次")
        except (ValueError, KeyError) as exc:
            print(f"{symbol} 回测失败：{exc}")
    if rows:
        summary = pd.DataFrame(rows)
        summary.to_csv(OUTPUT / "momentum_summary.csv", index=False)
        print("汇总已保存：", OUTPUT / "momentum_summary.csv")
        print("收益列为小数；各标的独立计算，并非组合收益。")


if __name__ == "__main__":
    run({"prices": prices, "compare": compare, "index": index,
         "momentum": momentum_compare})
