# OpenBB Day 1：基本概念与常用数据源

> 适用环境：OpenBB 5.0.0、Python 3.13  
> 学习目标：知道 OpenBB 是什么、Provider 是什么、可以从哪里取什么数据，以及怎样查找和使用函数。

## 1. OpenBB 是什么？

OpenBB 可以理解为一个统一的金融数据工具箱。它本身通常不生产或托管金融数据，而是通过不同的数据连接器访问政府机构、交易所、监管机构和研究数据库。

使用者面对的是相对统一的 Python 调用方式：

```python
from openbb import obb
```

然后根据数据来源调用相应命名空间：

```python
obb.famafrench.factors(...)
obb.cboe.equity.historical(...)
obb.sec.company_filings(...)
```

可以把 OpenBB 想象成一个商场：

- `obb` 是商场入口；
- Provider 是不同的店铺或供货商；
- command/function 是店铺提供的具体服务；
- `OBBject` 是统一包装后的商品；
- DataFrame 是拆开包装后便于分析的数据表。

## 2. OpenBB 5 的重要版本差异

你现在使用的是 **OpenBB 5**。V5 中，每个数据源都有自己的命名空间：

```python
# OpenBB 5
obb.cboe.equity.historical(...)
obb.nasdaq.equity.historical(...)
obb.fred.economy.fred_series(...)
```

网上不少教程针对 OpenBB 4，可能出现：

```python
# 旧版教程中常见，V5 中不要直接照搬
obb.equity.price.historical(..., provider="yfinance")
```

V5 已不再提供 `openbb-yfinance`、`openbb-fmp`、`openbb-intrinio` 等旧版官方 Provider 包。因此，遇到教程代码无法运行时，第一件事是确认教程对应的 OpenBB 大版本。

## 3. Provider、Namespace 和 Command

### 3.1 Provider

Provider 是实际数据来源的连接器，例如：

- `famafrench`：Kenneth French Data Library；
- `fred`：圣路易斯联储 FRED；
- `sec`：美国 SEC EDGAR；
- `cboe`：芝加哥期权交易所 Cboe。

Provider 决定：

- 数据来自哪里；
- 有哪些字段和历史范围；
- 是否需要 API Key；
- 请求频率和使用条款；
- 数据是否实时、延迟或经过修订。

OpenBB 只是连接器，数据质量、覆盖范围和限流规则最终由上游数据源决定。

### 3.2 Namespace

Namespace 是 `obb` 下的入口。例如安装 `openbb-fred` 后，会出现：

```python
obb.fred
```

安装 `openbb-sec` 后，会出现：

```python
obb.sec
```

查看当前环境的顶层入口：

```python
print([name for name in dir(obb) if not name.startswith("_")])
```

### 3.3 Command / Function

Command 是实际执行的功能，例如：

```python
obb.famafrench.factors(...)
```

其中：

- `famafrench` 是命名空间；
- `factors` 是 command/function；
- `region`、`factor`、`frequency` 是参数。

## 4. 当前常见 Provider 速查表

下面按学习用途分类。是否需要凭证以 OpenBB V5 官方文档为准。

| Namespace | 数据来源 | 主要数据 | API Key |
|---|---|---|---|
| `obb.famafrench` | Kenneth French Data Library | 三因子、五因子、动量、反转、投资组合收益 | 不需要 |
| `obb.cboe` | Cboe | 延迟股票行情、指数、期货、期权数据 | 不需要 |
| `obb.nasdaq` | Nasdaq 公共网站 | 美国、北欧、波罗的海市场公开数据 | 不需要 |
| `obb.tmx` | TMX | 加拿大市场数据，属于非官方连接方式 | 不需要 |
| `obb.deribit` | Deribit | 加密货币期权、期货等衍生品市场数据 | 不需要 |
| `obb.fred` | 圣路易斯联储 FRED | 利率、GDP、通胀、就业等宏观时间序列 | 需要免费 Key |
| `obb.bls` | 美国劳工统计局 | CPI、就业、工资、生产率等劳动力与物价数据 | Key 可选 |
| `obb.federal_reserve` | 美联储系统 | 美联储、FOMC、地区联储公开资料 | 不需要 |
| `obb.ecb` | 欧洲央行 | 欧元区利率、货币、通胀、金融统计 | 不需要 |
| `obb.imf` | 国际货币基金组织 | 国家宏观、国际收支、财政和全球经济数据 | 不需要 |
| `obb.oecd` | OECD | 各国经济、人口、就业和政策指标 | 不需要 |
| `obb.eia` | 美国能源信息署 | 石油、天然气、电力、能源价格和库存 | 需要免费 Key |
| `obb.jodi` | JODI | 全球石油与天然气供需数据库 | 不需要 |
| `obb.sec` | SEC EDGAR | 上市公司申报、财务披露和监管文件 | 不需要 |
| `obb.finra` | FINRA | 美国证券市场监管与交易相关公开数据 | 不需要 |
| `obb.cftc` | CFTC / DTCC | COT 持仓报告、掉期数据 | Key 可选 |
| `obb.ustreasury` | 美国财政部 | 国债、利率、财政相关数据 | 不需要 |
| `obb.uscongress` | 美国国会与 GovInfo | 法案、国会记录和政府文件 | Key 可选 |
| `obb.usda` | 美国农业部 | 农业市场和政府公开数据 | 不需要 |

### 新手最值得先学的五个

1. `famafrench`：无需 Key，适合学习因子、收益率和组合分析。
2. `cboe`：了解股票、指数、期权和市场波动率数据。
3. `fred`：宏观量化研究的重要入口，但需要申请免费 Key。
4. `sec`：研究美股公司财报和监管文件。
5. `bls`：研究美国通胀和就业，无 Key 也能使用但额度较低。

## 5. 数据类别和典型用途

### 5.1 股票与指数行情

可先探索：

```python
obb.cboe.equity
obb.cboe.index
obb.nasdaq.equity
obb.tmx
```

用途包括：

- 获取历史价格；
- 计算收益率和波动率；
- 比较不同资产；
- 构建简单均线或动量策略。

需要注意，免费公开数据可能延迟，覆盖范围也不一定等同于专业行情终端。

### 5.2 宏观经济

常用来源：

```python
obb.fred
obb.bls
obb.ecb
obb.imf
obb.oecd
```

典型数据：

- GDP；
- CPI/PCE 通胀；
- 失业率和非农就业；
- 政策利率和国债收益率；
- 工业生产、零售销售；
- 国家间经济指标。

宏观数据经常会被修订。量化回测时要特别警惕“今天看到的历史数据”和“当时真正可见的数据”可能不同。

### 5.3 公司基本面与监管文件

主要入口：

```python
obb.sec
```

典型用途：

- 查询 10-K 年报和 10-Q 季报；
- 查询 8-K 重大事件；
- 查询公司申报历史；
- 研究管理层披露与风险因素。

SEC 文件是研究美国上市公司的重要一手资料，但原始文档不等于已经清洗好的标准化财务数据库。

### 5.4 因子与资产定价

主要入口：

```python
obb.famafrench
```

典型数据：

- 三因子：市场、规模、价值；
- 五因子：再加入盈利能力和投资风格；
- 动量因子；
- 长短期反转；
- 按市值、估值等特征划分的组合收益。

这些数据适合学习：

- 市场风险溢价；
- 因子暴露；
- 组合收益来源；
- CAPM 和多因子回归。

### 5.5 期货、期权与持仓

主要入口：

```python
obb.cboe.options
obb.cboe.futures
obb.deribit
obb.cftc
```

典型用途：

- 期权链和隐含波动率；
- 指数期权与波动率产品；
- 加密货币衍生品；
- CFTC 交易者持仓报告。

这一类数据涉及到期日、执行价、看涨/看跌、合约乘数等概念，建议放到后续学习。

### 5.6 能源与商品

主要入口：

```python
obb.eia
obb.jodi
obb.cftc
```

典型用途：

- 原油和天然气库存；
- 能源产量、消费和进出口；
- 商品期货持仓；
- 供需变化研究。

## 6. OpenBB 返回的 OBBject

大部分 OpenBB command 返回 `OBBject`，而不是直接返回 DataFrame：

```python
response = obb.famafrench.factors(
    region="america",
    factor="3_factors",
    frequency="monthly",
)
```

常用属性：

```python
response.results    # 结构化结果
response.provider   # 实际使用的数据提供方
response.warnings   # 请求过程中的警告
response.extra      # 元数据等附加信息
```

转换为 DataFrame：

```python
df = response.to_dataframe()
```

为什么不直接返回 DataFrame？因为统一包装可以同时携带：

- 数据结果；
- Provider 信息；
- 警告；
- 查询元数据；
- 图表对象；
- REST API 所需的序列化结构。

## 7. 如何探索一个陌生 Provider

### 方法一：使用 `dir`

```python
print([x for x in dir(obb.cboe) if not x.startswith("_")])
print([x for x in dir(obb.cboe.equity) if not x.startswith("_")])
```

这种方式适合快速发现当前安装环境中真实存在的命令。

### 方法二：查看内置文档

```python
print(obb.famafrench.factors.__doc__)
```

在 IPython 或 Jupyter 中：

```python
obb.famafrench.factors?
```

### 方法三：查看函数签名

```python
import inspect

print(inspect.signature(obb.famafrench.factors))
```

### 方法四：阅读官方 API Reference

官方 Reference 会列出：

- 参数名与类型；
- 默认值；
- Provider 特有参数；
- 返回字段；
- 调用示例。

建议顺序是：先看签名，再看文档示例，最后只请求一小段数据。

## 8. API Key 是什么？

API Key 是数据提供方用来识别请求者的凭证。它不是 OpenBB 密码，而是上游数据源发放的访问令牌。

需要 Key 的典型来源：

- FRED：`fred_api_key`；
- EIA：`eia_api_key`；
- BLS：`bls_api_key`，可选；
- Congress.gov：`congress_gov_api_key`，可选；
- CFTC：`cftc_app_token`，可选。

原则：

- 不要把 Key 直接写进 Git 仓库；
- 不要把 Key 放在公开截图或聊天记录中；
- 优先使用 OpenBB 用户配置或环境变量；
- `.env` 文件必须加入 `.gitignore`。

Day 1 可以继续使用无需 Key 的 `famafrench`，等学习 FRED 时再配置凭证。

## 9. 一个标准的数据分析流程

以后大部分量化练习都会重复下面的流程：

```text
明确问题
  ↓
选择数据源和字段
  ↓
用 OpenBB 获取数据
  ↓
检查日期、单位、缺失值和重复值
  ↓
转换为 DataFrame
  ↓
计算收益率、波动率或指标
  ↓
可视化并解释结果
  ↓
检查前视偏差、幸存者偏差和交易成本
```

OpenBB 主要帮助完成“获取和标准化数据”，不会自动替你保证研究结论正确。

## 10. 新手常见误区

### 误区一：能下载数据就等于能用于实盘

公开数据可能延迟、修订、缺失或存在使用限制。研究、回测和实盘对数据质量的要求不同。

### 误区二：把百分数当成小数

Fama-French 数据中的 `2.5` 通常表示 `2.5%`。参与复利计算前需要：

```python
returns = data["mkt_rf"] / 100
```

### 误区三：直接相加收益率

多期累计收益通常使用复利：

```python
cumulative_return = (1 + returns).prod() - 1
```

### 误区四：忽略频率

日度、月度和年度数据不能直接混算。年化公式也取决于频率：

```python
# 月度收益率
annual_return_approx = monthly_returns.mean() * 12
annual_volatility = monthly_returns.std() * (12**0.5)
```

### 误区五：把相关关系当成因果关系

某个因子过去有效，不代表它必然导致未来收益，也不代表它会一直有效。

### 误区六：照抄旧版教程

看到 `obb.equity` 或 `provider="yfinance"` 时，先确认教程是否针对 OpenBB V4。

## 11. Day 1 建议动手练习

### 练习 A：探索命名空间

```python
from openbb import obb

print([x for x in dir(obb) if not x.startswith("_")])
print([x for x in dir(obb.famafrench) if not x.startswith("_")])
```

目标：理解“安装什么扩展，就出现什么入口”。

### 练习 B：修改三因子参数

把 `demo1.py` 中的频率改为日度：

```python
frequency="daily"
```

观察：

- 行数发生了什么变化？
- 波动率年化还可以乘 `sqrt(12)` 吗？
- 日度数据应该使用多少个交易日年化？

提示：美股通常使用约 `252` 个交易日。

### 练习 C：比较地区

```python
america = obb.famafrench.factors(region="america", factor="3_factors")
europe = obb.famafrench.factors(region="europe", factor="3_factors")
```

目标：比较两个市场的平均市场风险溢价和波动率。

### 练习 D：查看元数据

```python
response = obb.famafrench.factors()
print(response.provider)
print(response.extra)
```

目标：养成检查数据来源和元数据的习惯。

## 12. 后续学习路线

建议按照下面的顺序继续：

1. **Day 2：Pandas 与收益率**  
   索引、筛选、缺失值、简单收益率、对数收益率和复利。
2. **Day 3：行情与可视化**  
   使用 Cboe/Nasdaq 数据，绘制价格、收益率和回撤曲线。
3. **Day 4：风险指标**  
   波动率、最大回撤、夏普比率和相关系数。
4. **Day 5：宏观数据**  
   配置 FRED Key，研究利率、通胀和就业。
5. **Day 6：因子模型**  
   CAPM、Fama-French 回归、Alpha 和 Beta。
6. **Day 7：第一次小型回测**  
   均线或动量策略，并加入交易成本和基准比较。

## 13. 官方资料

- [OpenBB V5 Python 文档](https://docs.openbb.co/odp/python)
- [OpenBB V5 Provider 列表](https://docs.openbb.co/odp/python/extensions/providers)
- [OpenBB V5 架构](https://docs.openbb.co/odp/python/concepts/architecture)
- [OBBject 与核心概念](https://docs.openbb.co/odp/python/concepts)
- [Fama-French factors 函数文档](https://docs.openbb.co/odp/python/reference/famafrench/factors)
- [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)

---

## 问题与补充记录

后续提问时，可以把新的解释和示例继续补充在这里。

### 待讨论

- [ ] OpenBB 与直接调用数据源 API 有什么区别？
- [ ] OBBject 和 DataFrame 应该分别在什么时候使用？
- [ ] 如何申请和配置 FRED API Key？
- [ ] 如何获取一只 ETF 的历史价格？
- [ ] 如何判断一个数据源能不能用于回测？

