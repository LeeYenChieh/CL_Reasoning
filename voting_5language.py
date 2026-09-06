import os
import random
from collections import Counter
from File.File import File

LANGUAGES = ["english", "chinese", "japanese", "spanish", "russian"]
MODELS = ["deepseek", "gpt4omini", "gemini", "qwen"]
DATASETS = ["commonsenseqa", "mmlu", "mathqa", "truthfulqa"]

OUTPUT_DIR = "result/voting"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for m in MODELS:
    for d in DATASETS:
        files: list[File] = []

        for l in LANGUAGES:
            filepath = f"result/baseline/{m}_{d}_onelanguage_{l}.json"
            if os.path.exists(filepath):
                try:
                    files.append(File(filepath))
                except Exception as e:
                    print(f"⚠️ 檔案讀取失敗 [{filepath}]: {e}")
            else:
                print(f"⚠️ 找不到檔案: {filepath}")

        if not files:
            print(f"⏭️ 略過 {m} - {d} (無有效檔案)")
            continue

        q_ids = list(files[0].records_map.keys())
        total = len(q_ids)

        if total == 0:
            print(f"⏭️ 略過 {m} - {d} (題數為 0)")
            continue

        cnt = 0
        voted_records = []

        for q_id in q_ids:
            votes = []
            correct_ans = None
            base_record = files[0].getRecordById(q_id) or {}

            for f in files:
                record = f.getRecordById(q_id)
                if record is not None:
                    my_ans = record.get("MyAnswer")
                    ans = record.get("Answer")
                    if my_ans is not None:
                        votes.append(my_ans)
                    if ans is not None and correct_ans is None:
                        correct_ans = ans

            majority_ans = None
            if votes:
                vote_counts = Counter(votes)
                max_votes = max(vote_counts.values())
                top_answers = [a for a, c in vote_counts.items() if c == max_votes]
                majority_ans = random.choice(top_answers)

            if majority_ans is not None and correct_ans is not None and majority_ans == correct_ans:
                cnt += 1

            voted_records.append({
                "id": q_id,
                "Answer": correct_ans,
                "MyAnswer": majority_ans,
            })

        accuracy = cnt / total

        # 沿用 baseline 的 Model/Dataset metadata，Strategy 改為 voting
        ref_meta = files[0].metadata
        metadata = {
            "Model": ref_meta.get("Model", {}),
            "Dataset": ref_meta.get("Dataset", {}),
            "Strategy": {
                "strategyType": "voting_5language",
                "displayName": "5-Language Voting",
                "languages": ["Voting"],
            },
            "ExactMatch_Correct": cnt,
            "ExactMatch_Total": total,
            "ExactMatch_Accuracy": round(accuracy, 4),
        }

        output = [metadata] + sorted(voted_records, key=lambda r: r["id"])
        out_path = os.path.join(OUTPUT_DIR, f"{m}_{d}_voting_5language.json")
        import json
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

        print(f"[{m}] [{d}]  {cnt} / {total}  ({accuracy * 100:.2f}%)  → {out_path}")
