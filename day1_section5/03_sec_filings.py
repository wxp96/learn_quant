"""5.3 SEC：年报、季报、重大事件、申报历史与原文披露。"""
from openbb import obb
from _common import fetch, run

SYMBOL = "AAPL"


def filings(form=None):
    params = dict(symbol=SYMBOL, limit=10)
    if form:
        params["form_type"] = form
    # 输出中的 report_url 可打开原始申报文件。
    fetch(f"sec_{form or 'history'}", obb.sec.company_filings, **params)


def risks():
    fetch("sec_risk_factors", obb.sec.risk_factors, symbol=SYMBOL)


def discussion():
    fetch("sec_management_discussion", obb.sec.management_discussion_analysis, symbol=SYMBOL)


if __name__ == "__main__":
    run({"annual": lambda: filings("10-K"), "quarterly": lambda: filings("10-Q"),
         "events": lambda: filings("8-K"), "history": filings,
         "risks": risks, "discussion": discussion})
