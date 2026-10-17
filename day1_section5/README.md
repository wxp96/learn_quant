# Day 1 第五部分：六类数据获取练习

适用于项目现有 OpenBB 5 环境。每节一个 Python 文件；`_common.py` 负责选择示例、展示数据和保存 CSV。

从项目根目录运行：

```bash
.venv/bin/python day1_section5/01_prices.py
.venv/bin/python day1_section5/01_prices.py --example compare
.venv/bin/python day1_section5/04_factors.py --example 5_factors
```

默认只运行该节第一项。`--help` 查看选项，`--example all` 获取该节所有示例。导入脚本不会自动下载数据。

| 小节 | 文件 | `--example` 选项 | 凭证 |
|---|---|---|---|
| 5.1 行情 | `01_prices.py` | prices、compare、index | 无 |
| 5.2 宏观 | `02_macro.py` | gdp、cpi、pce、unemployment、payrolls、policy_rate、treasury、production、retail、china_gdp | FRED Key |
| 5.3 公司披露 | `03_sec_filings.py` | annual、quarterly、events、history、risks、discussion | 无 |
| 5.4 因子 | `04_factors.py` | 3_factors、5_factors、momentum、st_reversal、lt_reversal、portfolios | 无 |
| 5.5 衍生品 | `05_derivatives.py` | options、index_options、vix、crypto、positioning | 无，CFTC token 可选 |
| 5.6 能源 | `06_energy.py` | balance、production、stocks、oil_stocks、gas_stocks、positioning | EIA 两项库存需 Key，JODI 无需 |

FRED 和 EIA 可使用已有 OpenBB 用户配置，也可在终端安全输入环境变量：

```bash
read -rsp 'FRED Key: ' FRED_API_KEY
export FRED_API_KEY
# EIA 同理，将变量改为 EIA_API_KEY
```

脚本不会自动读取 `.env`。不要把真实 Key 写进代码或提交到仓库。

成功下载后，原始表保存在本目录的 `output/`，行情指标和比较结果也会保存。该目录已被项目 `.gitignore` 忽略。错误会显示原因，空表不会当作成功；运行 all 时其他示例继续执行，请逐项查看输出。

学习时依次观察：调用参数 → OBBject 的 provider / warnings → DataFrame 列名、日期、单位 → CSV。5.1 额外展示收益率、波动率、均线和动量；5.4 展示百分数换算与市场总收益。这里只演示回归所需数据的获取，不实现完整因子回归。

宏观数据保留各自频率，跨国比较前需要统一口径；历史值可能被修订。行情不默认视为含分红复权价，均线示例也不包含成本与完整回测。衍生品当前快照不能替代历史期权链。CFTC 统计日不等于公布日。JODI 首次下载可能较慢，不同流量与库存单位不能直接相加。

接口与参数以本地安装版本的 `命令.__doc__` 为准，另可查看 [OpenBB V5 官方参考](https://docs.openbb.co/odp/python/reference)。这些示例选择代表性数据源，不逐一遍历所有 Provider。

## 多标的动量回测

在 `01_prices.py` 顶部修改 `SYMBOLS`，例如 `["AAPL", "MSFT", "SPY"]`，然后运行：

```bash
.venv/bin/python day1_section5/01_prices.py --example momentum
```

规则：昨日收盘价相对 20 个交易日前上涨，则今日开盘全仓持有；否则今日开盘清仓。这里使用 `momentum`，与 `prices()` 中的双均线信号是两种规则。可修改 `MOMENTUM_DAYS`、`INITIAL_CASH`、`COST_BPS`。将 `USE_CACHED_PRICES` 改为 `True` 可优先使用已有行情，注意本地缓存不会自动更新。

两种策略都从动量预热结束后的第一天开盘开始；买入持有在该日开盘买入并持有到样本末尾。动量策略按昨日持仓计算隔夜收益，按开盘调仓后的持仓计算日内收益；每次买卖扣除设定成本。期末按收盘市值计价，不强制卖出。假设可交易零碎股，空仓资金无利息，不计税、不含分红。原始开收盘价若没有一致的拆股调整，拆股会扭曲结果；这是价格收益教学回测。

输出：`output/<symbol>_momentum_backtest.csv` 保存每日动量、仓位、收益和资金曲线；`output/momentum_summary.csv` 保存各标的累计收益、收益差、最大回撤、交易次数及期末资金。收益差是两个累计收益之差，不是回归 Alpha。收益字段 0.10 表示 10%。不同标的数据覆盖不同可能导致回测起止日不同，应查看汇总日期。

### 价格与 20 日均线比较

```bash
.venv/bin/python day1_section5/01_prices.py --example ma
```

昨日收盘价 > 昨日 20 日收盘均价，则今日开盘持仓；否则空仓。均线包含信号日自身及前 19 个交易日的收盘价。周期沿用 `MOMENTUM_DAYS`，成本与动量策略一致。为比较三种结果，均线策略也从动量预热结束后的同一天开始。输出 `ma_summary.csv` 和 `<symbol>_ma_backtest.csv`；原动量输出保留。逐日表新增 `moving_average`、`previous_ma` 列，可核对仓位信号。
