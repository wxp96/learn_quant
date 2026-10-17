"""各节共用：选择示例、展示 OBBject、保存 CSV。"""
import argparse
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / "output"


def fetch(name, command, **params):
    """保留真实报错；某项下载失败时，让其他示例继续执行。"""
    print(f"\n--- {name} ---")
    try:
        response = command(**params)
        data = response.to_dataframe()
        print(f"Provider: {response.provider}；行数: {len(data)}")
        if response.warnings:
            print("接口警告：", response.warnings)
        if data.empty:
            raise ValueError("接口返回空表，请检查代码、日期范围或上游覆盖情况")
        print(data.tail().to_string(max_cols=12))
        OUTPUT.mkdir(parents=True, exist_ok=True)
        path = OUTPUT / f"{name}.csv"
        data.to_csv(path)
        print(f"已保存：{path}")
        return data
    except Exception as exc:
        print(f"获取失败 [{type(exc).__name__}]：{exc}")
        print("检查网络、API Key 和上游限制；未使用模拟数据替代。")
        return None


def run(examples):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--example", choices=["all", *examples], default=next(iter(examples)),
                        help="默认只运行第一项；all 运行本节全部示例")
    args = parser.parse_args()
    selected = examples if args.example == "all" else {args.example: examples[args.example]}
    for title, example in selected.items():
        print(f"\n>>> 示例：{title}")
        example()
