from argparse import ArgumentParser
import itertools
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from Strategy.RunContext import RunContext

from Model.Model import Model
from Model.ModelConfig import ModelConfig
from Model.ModelFactory import ModelFactory
from Model.ModelType import MODEL_STR_LIST, ModelType

from Dataset.Dataset import Dataset
from Dataset.DatasetConfig import DatasetConfig
from Dataset.DatasetFactory import DatasetFactory
from Dataset.DatasetType import DatasetType

from Strategy.StrategyConfig import StrategyConfig
from Strategy.OnlyOneLanguage import OnlyOneLanguage

from Log.NoLog import NoLog
from Log.OneAgentLog import OneAgentLog

# Datasets that have the rewrite / prompt-variant pipeline wired (see Dataset/*.py).
ACTIVE_DATASETS = ["mmlu", "mathqa", "truthfulqa", "commonsenseqa"]
PROMPT_STYLES = ["cot", "short_cot", "direct"]


def parseArgs():
    parser = ArgumentParser(description="Experiments 2-4 - rewritten English question + prompt style")
    parser.add_argument("--log", action="store_true", help="Enable terminal logging")

    parser.add_argument("-m", "--model", choices=MODEL_STR_LIST, required=True, nargs="+", help="Choose your model(s)")
    parser.add_argument("--temperature", default=0.0, type=float, help="Model temperature setting")

    parser.add_argument("-d", "--dataset", choices=ACTIVE_DATASETS, required=True, nargs="+", help="Choose your dataset(s)")
    parser.add_argument("--nums", help="Data Nums to evaluate (-1 for all)", default=-1, type=int)
    parser.add_argument("--sample", help="Data Sample multiplier", default=1, type=int)

    parser.add_argument("--prompt-style", dest="prompt_style", choices=PROMPT_STYLES, default="cot",
                        help="cot = current baseline CoT (Exp 2), short_cot = brief CoT (Exp 3), direct = no CoT (Exp 4)")

    parser.add_argument("--dirpath", help="Directory to save results (default: result/english_<prompt_style>)", default=None)
    parser.add_argument("-w", "--workers", type=int, default=None,
                        help="Max concurrent threads/workers (default: one per task, i.e. full fan-out)")

    return parser.parse_args()


def runExperiment(model_name, dataset_name, args, dirpath):
    log = OneAgentLog() if args.log else NoLog()

    model: Model = ModelFactory().buildModel(
        ModelType(model_name),
        ModelConfig.from_dict({"modelType": model_name, "temperature": args.temperature}),
    )

    dataset: Dataset = DatasetFactory().buildDataset(
        DatasetType(dataset_name),
        DatasetConfig.from_dict({
            "datasetType": dataset_name,
            "nums": args.nums,
            "sample": args.sample,
            "language": "english",
            "useRewrite": True,   # pull the paraphrase from Data/rewritten/<dataset>_english.json
        }),
    )

    if not model or not dataset:
        print(f"Error: Failed to build {model_name} or {dataset_name}.")
        return

    strategy_config = StrategyConfig.from_dict({
        "strategyType": "onelanguage",
        "languages": ["english"],
        "promptStyle": args.prompt_style,
    })
    strategy = OnlyOneLanguage(strategy_config, model, dataset, log)

    context = RunContext()
    context.setStrategy(strategy)
    result = context.runExperiment()

    if not result:
        print(f"Experiment {model_name} - {dataset_name} ({args.prompt_style}) yielded no results.")
        return

    os.makedirs(dirpath, exist_ok=True)
    # Same filename convention as run_baseline_multithread.py; the experiment is identified
    # by the directory name and by the metadata (promptStyle + Dataset.useRewrite).
    path = os.path.join(dirpath, f"{model_name}_{dataset_name}_onelanguage_english.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"🎉 Success! Results saved to: {path}")


def main():
    args = parseArgs()
    dirpath = args.dirpath or os.path.join("result", f"english_{args.prompt_style}")

    tasks = list(itertools.product(args.model, args.dataset))
    workers = args.workers if args.workers is not None else len(tasks)
    workers = max(1, workers)

    print("🚀 Preparing rewritten-English evaluation (Experiments 2-4)...")
    print(f"Models: {args.model}")
    print(f"Datasets: {args.dataset}")
    print(f"Prompt style: {args.prompt_style}")
    print(f"Output dir: {dirpath}")
    print(f"Total tasks: {len(tasks)} | Concurrent workers: {workers}\n")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(runExperiment, m, d, args, dirpath) for m, d in tasks]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"❌ A job generated an exception: {e}")

    print("\n✅ All experiments finished!")


if __name__ == "__main__":
    main()
