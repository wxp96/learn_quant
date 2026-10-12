"""5.5 衍生品：期权链/IV、VIX 期货、BTC 期货、CFTC 持仓。"""
from openbb import obb
from _common import fetch, run


def options():
    # 完整链包含多个到期日、执行价与看涨/看跌合约；关注 IV 和 Greeks 字段。
    # 保留接口原始 IV 单位，阅读字段文档后再决定是否乘以 100。
    fetch("aapl_options", obb.cboe.options.chains, symbol="AAPL")


def index_options():
    fetch("spx_options", obb.cboe.options.chains, symbol="SPX")


def vix():
    fetch("vix_futures", obb.cboe.futures.curve, symbol="VX_EOD")


def crypto():
    fetch("btc_futures", obb.deribit.futures.curve, symbol="BTC")


def positioning():
    # 黄金 COMEX 合约代码；持仓统计日不等于报告公布日。
    fetch("gold_cot", obb.cftc.cot, code="088691", report_type="legacy",
          futures_only=True, measure="positions", limit=8)


if __name__ == "__main__":
    run({"options": options, "index_options": index_options,
         "vix": vix, "crypto": crypto, "positioning": positioning})
