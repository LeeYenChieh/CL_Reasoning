import os
import random
from collections import Counter
from File.File import File

LANGUAGES = ["english", "chinese", "japanese", "spanish", "russian"]
MODELS = ["deepseek", "gpt4omini", "gemini", "qwen"]
DATASETS = ["commonsenseqa", "mmlu", "mathqa", "truthfulqa"]

for m in MODELS:
    for d in DATASETS:
        files: list[File] = []
        
        # 1. 安全讀取檔案 (防呆: 檢查檔案是否存在)
        for l in LANGUAGES:
            filepath = f"result/baseline/{m}_{d}_onelanguage_{l}.json"
            if os.path.exists(filepath):
                try:
                    files.append(File(filepath))
                except Exception as e:
                    print(f"⚠️ 檔案讀取失敗 [{filepath}]: {e}")
            else:
                print(f"⚠️ 找不到檔案: {filepath}")
        
        # 如果這個組合沒有成功讀取到任何檔案，直接跳過
        if not files:
            print(f"⏭️ 略過 {m} - {d} (無有效檔案)\n")
            continue
            
        # 以第一個成功讀取的檔案作為基準題庫
        q_ids = files[0].records_map.keys()
        total = len(q_ids)
        cnt = 0

        # 防呆: 避免 ZeroDivisionError
        if total == 0:
            print(f"⏭️ 略過 {m} - {d} (題數為 0)\n")
            continue

        for q_id in q_ids:
            votes = []
            correct_ans = None
            
            # 收集所有語言對這一題的預測結果
            for f in files:
                record = f.getRecordById(q_id)
                
                if record is not None:
                    my_ans = record.get("MyAnswer")
                    ans = record.get("Answer")
                    
                    # 收集該語言的預測答案 (選票)
                    if my_ans is not None:
                        votes.append(my_ans)
                        
                    # 取得 Ground Truth (每一種語言檔案裡正確答案應該都一樣，取一次即可)
                    if ans is not None and correct_ans is None:
                        correct_ans = ans
            
            # 2. 進行多數決 Voting (包含平手時的隨機處理)
            if votes and correct_ans is not None:
                vote_counts = Counter(votes)
                
                # 找出最高票數是多少 (例如最高是 2 票)
                max_votes = max(vote_counts.values())
                
                # 找出所有得到最高票數的答案 (可能會有一個或多個)
                top_answers = [ans for ans, count in vote_counts.items() if count == max_votes]
                
                # 🎯 從最高票的答案清單中「隨機」挑選一個作為最終答案
                majority_ans = random.choice(top_answers)
                
                # 3. 如果最終選出的答案等於正確答案，才算答對
                if majority_ans == correct_ans:
                    cnt += 1
        
        # 4. 輸出結果
        print(f'[{m}] ---- [{d}] ----')
        print(f'答對題數: {cnt} / {total}')
        print(f'Voting 準確率: {cnt / total * 100:.2f}%\n')