import os
import json
import itertools
import concurrent.futures

# 替換為你專案實際的 import 路徑
from File.File import File
from Log.NoLog import NoLog
from Model.ModelFactory import ModelFactory
from Model.ModelType import ModelType
from Dataset.DatasetFactory import DatasetFactory
from Dataset.DatasetType import DatasetType
from Strategy.StrategyConfig import StrategyConfig
from Strategy.SelfReflection import SelfReflection

# ==========================================
# ⚙️ 執行參數設定 (Configuration)
# ==========================================
MODELS = ["gpt4omini", "qwen", "gemini", "deepseek"]            # 替換為你的 ModelType 名稱
DATASETS = ["mmlu", "mathqa", "truthfulqa", "commonsenseqa"]              # 替換為你的 DatasetType 名稱
LANGUAGES = ["english", "chinese"]         # 替換為你要跑的語言

BASELINE_DIR = "result/baseline"           # Baseline 檔案所在的資料夾
OUTPUT_DIR = "result/self_reflection"      # 執行完 Self-Reflection 要存檔的資料夾
MAX_WORKERS = 32                            # 同時執行的最大 Thread 數量 (建議依照 API Rate Limit 調整)

def run_single_reflection(model_name, dataset_name, lang):
    """
    執行單一 (Model, Dataset, Language) 組合的 Self-Reflection 任務。
    """
    # 1. 確認 Baseline 檔案是否存在
    # 假設 Baseline 檔案命名規則為: model_dataset_language.json
    baseline_filename = f"{model_name}_{dataset_name}_onelanguage_{lang}.json"
    baseline_path = os.path.join(BASELINE_DIR, baseline_filename)
    
    if not os.path.exists(baseline_path):
        return f"❌ Skip: 找不到 Baseline 檔案 -> {baseline_path}"

    # 2. 確認是否已經跑過 (避免中斷後重跑浪費 API)
    output_path = os.path.join(OUTPUT_DIR, baseline_filename)
    if os.path.exists(output_path):
        return f"⏩ Skip: 已經執行過並存在 -> {output_path}"

    try:
        # 3. 建立 Log 物件
        # (請依照你 Log.py 實際的初始化方式修改，這裡假設可以傳入檔名或不傳參數)
        log = NoLog() 

        # 4. 載入 Baseline File 物件
        baseline_file = File(baseline_path)

        # 5. 從 Baseline File 中提取 Config 並實例化 Model 與 Dataset
        model_config = baseline_file.getModelConfig()
        dataset_config = baseline_file.getDatasetConfig()

        # 透過 Factory 建立對應的實體
        model = ModelFactory().buildModel(ModelType(model_config.modelType), model_config)
        dataset = DatasetFactory().buildDataset(DatasetType(dataset_config.datasetType), dataset_config)

        # 6. 建立 Self-Reflection 的 StrategyConfig
        strategy_config = StrategyConfig(
            strategyType="selfreflection",
            languages=[lang]
        )

        # 7. 實例化 SelfReflection 策略並執行
        reflection_strategy = SelfReflection(strategy_config, model, dataset, log, baseline_file)
        results = reflection_strategy.getRes()

        # 8. 將結果存成 JSON 檔案
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        return f"✅ Success: {model_name} - {dataset_name} - {lang} (共 {len(results)-1} 筆)"

    except Exception as e:
        return f"❌ Error 發生於 ({model_name}, {dataset_name}, {lang}): {str(e)}"

def main():
    # 使用 itertools.product 產生所有可能的組合
    combinations = list(itertools.product(MODELS, DATASETS, LANGUAGES))
    print(f"🚀 準備啟動 Self-Reflection 多執行緒任務，共計 {len(combinations)} 組...")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 啟動 ThreadPoolExecutor
    # ⚠️ 注意：因為 SelfReflection 內部有 tqdm 進度條，多 Thread 併發時終端機畫面可能會有些交錯 (是正常現象)
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任務
        futures = [
            executor.submit(run_single_reflection, m, d, l)
            for m, d, l in combinations
        ]

        # 當有任務完成時，立刻印出結果狀態
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
            
    print("\n🎉 所有 Self-Reflection 任務執行完畢！")

if __name__ == "__main__":
    main()