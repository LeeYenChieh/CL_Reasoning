"""
test_em_legacy.py — 計算舊版 (2025-11 世代) 結果檔的 Exact Match

為什麼需要獨立腳本:
  舊檔與現行 pipeline 不相容, 無法走 File / FileFactory / TestEM 那條路
    1. metadata 是扁平字串  {"Model": "Deepseek", "Dataset": "MMLU", "Strategy": "Challenge"}
       -> DatasetConfig.from_dict("MMLU") 會 AttributeError
    2. records 完全沒有 "id" 欄位
       -> File.records_map 會是空的, TestEM 會靜默回傳 accuracy 0.0
  本腳本直接讀 JSON, 不碰任何現有程式碼, 也不會改寫原始檔案。

比對邏輯:
  Dataset 家族中只有 MGSM 覆寫 compareTwoAnswer, 而 MGSM 不在這批資料裡,
  因此一律使用基底類別的 str(Answer) == str(MyAnswer)。

除了 EM 之外也一併輸出 Times (辯論回合數) 的統計 — 同語言辯論常常兩個 agent
一開始就同意 (Times=0, 根本沒辯), 比較同語言 vs 跨語言時必須控制這個「觸發率」,
否則會把「跨語言更常觸發辯論」誤讀成「跨語言本身比較好」。

另外計算 c = P(至少一個 agent 答對 | 兩者不一致):
  Times>0 恰好等價於「兩個 agent 初始答案不一致」(Challenge 只在初始不同時才進辯論迴圈),
  而 AnswerRecord1[0] / AnswerRecord2[0] 是兩者的初始答案。
  c 是辯論在分歧子集上的天花板 — 就算裁判完美, 最多也只能到 c。

用法:
    python3 test_em_legacy.py result/tempature1/challenge_EN result/tempature1/challenge_CN
    python3 test_em_legacy.py result/tempature1                    # 遞迴, 含 baseline 與各子目錄
    python3 test_em_legacy.py result/tempature1 --csv legacy_em.csv
"""

import csv
import json
import os
import sys
from argparse import ArgumentParser


def parse_name(path):
    """從檔名解析 (model, dataset, strategy)。

    舊檔命名: '{Model}_{Dataset}_{Strategy}.json'
    model / dataset / strategy 內可能有空格與連字號, 但都沒有底線,
    例如 'GPT 4.1 mini_CMB-Exam_Challenge.json' -> 3 段。
    """
    stem = os.path.splitext(os.path.basename(path))[0]
    parts = stem.split("_")
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    return stem, "?", "?"


def condition_of(path, strategy):
    """實驗條件: challenge 子目錄用目錄名 (challenge_EN / challenge_CN / challenge_CNEN),
    直接放在上層的 baseline 檔用檔名裡的 strategy (Only English / Only Chinese)。"""
    parent = os.path.basename(os.path.dirname(os.path.abspath(path)))
    if parent.startswith("challenge"):
        return parent
    return strategy


def evaluate(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list) or len(data) < 2:
        raise ValueError("檔案為空或不是 [metadata, record...] 格式")

    records = data[1:]
    model, dataset, strategy = parse_name(path)

    total = len(records)
    correct = 0
    empty = 0
    # Times=0 代表兩個 agent 一開始就同意, 沒有真的辯論
    n_no_debate = n_debate = 0
    c_no_debate = c_debate = 0
    has_times = False
    # c = P(至少一個 agent 答對 | 兩者不一致)
    n_disagree = n_recoverable = 0

    for r in records:
        ans = str(r.get("Answer", ""))
        my = str(r.get("MyAnswer", ""))
        ok = (ans == my)

        if ok:
            correct += 1
        if my.strip() in ("", "None", "null"):
            empty += 1

        times = r.get("Times")
        if times is not None:
            has_times = True
            if times > 0:
                n_debate += 1
                c_debate += ok
                # Times>0 <=> 兩個 agent 初始答案不一致 (Challenge 只在初始不同時才進辯論迴圈)
                # AnswerRecord[0] 是各自的初始答案
                r1 = r.get("AnswerRecord1") or []
                r2 = r.get("AnswerRecord2") or []
                inits = [str(rec[0]) for rec in (r1, r2) if rec]
                if inits:
                    n_disagree += 1
                    if any(x == ans for x in inits):
                        n_recoverable += 1
            else:
                n_no_debate += 1
                c_no_debate += ok

    return {
        "file": os.path.basename(path),
        "path": path,
        "model": model,
        "dataset": dataset,
        "strategy": strategy,
        "condition": condition_of(path, strategy),
        "n": total,
        "correct": correct,
        "accuracy": correct / total if total else 0.0,
        "empty_myanswer": empty,
        "has_times": has_times,
        "n_debate": n_debate,
        "n_no_debate": n_no_debate,
        # 觸發率: 實際發生辯論的題目比例
        "debate_rate": n_debate / total if (has_times and total) else None,
        # 分層 EM: 有辯 vs 沒辯
        "acc_debate": c_debate / n_debate if n_debate else None,
        "acc_no_debate": c_no_debate / n_no_debate if n_no_debate else None,
        # c = P(至少一個 agent 答對 | 兩者不一致) — 辯論在分歧子集上的天花板
        "n_disagree": n_disagree,
        "c_recoverable": n_recoverable / n_disagree if n_disagree else None,
        # 回收率: 在 [隨機挑一邊, 完美裁判] 之間的位置。
        # 不一致 => 至多一個 agent 答對, 所以隨機挑一邊的期望正確率是 c/2, 那才是下限。
        #   recovery = (acc - c/2) / (c - c/2) = 2*acc/c - 1
        "recovery": (2 * (c_debate / n_debate) / (n_recoverable / n_disagree) - 1)
                    if (n_debate and n_disagree and n_recoverable) else None,
    }


def collect_paths(inputs):
    paths = []
    for item in inputs:
        if os.path.isdir(item):
            for root, _, files in os.walk(item):
                paths.extend(os.path.join(root, f) for f in files if f.endswith(".json"))
        elif os.path.isfile(item):
            paths.append(item)
        else:
            print(f"[warn] 找不到: {item}")
    return sorted(set(paths))


def fmt_pct(x, width=7):
    return f"{x:>{width}.2%}" if x is not None else " " * (width - 1) + "-"


def print_detail(rows):
    print("\n📋 逐檔明細")
    print(f"{'condition':<15} {'model':<15} {'dataset':<12} {'n':>6} {'EM':>8} "
          f"{'觸發率':>8} {'不一致':>7} {'c':>8} {'EM|有辯':>9} {'回收率':>8}")
    print("-" * 108)
    for r in rows:
        print(f"{r['condition']:<15} {r['model']:<15} {r['dataset']:<12} {r['n']:>6} "
              f"{fmt_pct(r['accuracy'], 8)} {fmt_pct(r['debate_rate'], 8)} "
              f"{r['n_disagree']:>7} {fmt_pct(r['c_recoverable'], 8)} "
              f"{fmt_pct(r['acc_debate'], 9)} {fmt_pct(r['recovery'], 8)}")


def print_pivot(rows, value_key, title, note=""):
    """Row = (model, dataset), Column = condition。"""
    conditions = sorted({r["condition"] for r in rows})
    keys = sorted({(r["model"], r["dataset"]) for r in rows})
    table = {(r["model"], r["dataset"], r["condition"]): r[value_key] for r in rows}

    print(f"\n📊 {title}")
    if note:
        print(f"   {note}")
    head = f"{'model':<16} {'dataset':<12}" + "".join(f"{c:>18}" for c in conditions)
    print(head)
    print("-" * len(head))
    for model, dataset in keys:
        line = f"{model:<16} {dataset:<12}"
        for c in conditions:
            line += fmt_pct(table.get((model, dataset, c)), 18)
        print(line)


def main():
    parser = ArgumentParser(description="計算舊版結果檔的 Exact Match (不改寫原始檔案)")
    parser.add_argument("inputs", nargs="+", help="要掃描的目錄或檔案 (目錄會遞迴)")
    parser.add_argument("--csv", help="把逐檔明細另存成 CSV")
    args = parser.parse_args()

    paths = collect_paths(args.inputs)
    if not paths:
        print("❌ 沒有找到任何 JSON 檔案")
        sys.exit(1)

    print(f"🔍 找到 {len(paths)} 個 JSON 檔案，開始計算 Exact Match...")

    rows = []
    for p in paths:
        try:
            rows.append(evaluate(p))
        except Exception as e:
            print(f"⚠️  略過 {p}: {e}")

    if not rows:
        print("❌ 沒有任何檔案成功解析")
        sys.exit(1)

    rows.sort(key=lambda r: (r["condition"], r["dataset"], r["model"]))

    print_detail(rows)
    print_pivot(rows, "accuracy", "Exact Match 準確率  (row = model × dataset, col = 條件)")
    if any(r["has_times"] for r in rows):
        print_pivot(rows, "debate_rate", "辯論觸發率 (Times > 0 的題目比例)",
                    note="同語言 vs 跨語言比較時必須控制這一項")
        print_pivot(rows, "c_recoverable",
                    "c = P(至少一個 agent 答對 | 兩者不一致)",
                    note="辯論在分歧子集上的天花板：完美的裁判最多能到這個數字")
        print_pivot(rows, "acc_debate", "EM | 有實際辯論的子集",
                    note="⚠️ 各條件辯論的是不同題目子集，跨條件比較會有選擇效應")
        print_pivot(rows, "recovery", "回收率 = (EM|有辯 − c/2) ÷ (c − c/2)",
                    note="0% = 等同隨機挑一邊(c/2)，100% = 完美裁判(c)")

    if args.csv:
        fields = ["condition", "model", "dataset", "strategy", "n", "correct", "accuracy",
                  "empty_myanswer", "n_debate", "n_no_debate", "debate_rate",
                  "n_disagree", "c_recoverable", "acc_debate", "recovery",
                  "acc_no_debate", "file"]
        with open(args.csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        print(f"\n💾 明細已匯出至: {args.csv}")


if __name__ == "__main__":
    main()
