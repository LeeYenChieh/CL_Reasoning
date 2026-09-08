from argparse import ArgumentParser
import itertools
import json
import os
import sys
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
from Strategy.Rewrite import Rewrite

from Log.NoLog import NoLog
from Log.OneAgentLog import OneAgentLog

# Datasets that have the rewrite / prompt-variant pipeline wired (see Dataset/*.py).
ACTIVE_DATASETS = ["mmlu", "mathqa", "truthfulqa", "commonsenseqa"]


def parseArgs():
    parser = ArgumentParser(description="Experiment 1 - English question rewrite (paraphrase) generator")
    parser.add_argument("--log", action="store_true", help="Enable terminal logging")

    # A single fixed rewriter model produces one paraphrase file per dataset.
    parser.add_argument("-m", "--model", choices=MODEL_STR_LIST, required=True, help="The fixed rewriter model")
    parser.add_argument("--temperature", default=0.0, type=float, help="Model temperature setting")

    parser.add_argument("-d", "--dataset", choices=ACTIVE_DATASETS, required=True, nargs="+", help="Dataset(s) to rewrite")
    parser.add_argument("--nums", help="Data Nums to rewrite (-1 for all; use the SAME value you will evaluate with)",
                        default=-1, type=int)
    parser.add_argument("--sample", help="Data Sample multiplier", default=1, type=int)

    parser.add_argument("--dirpath", help="Directory to save the rewrite files", default="Data/rewritten")
    parser.add_argument("-w", "--workers", type=int, default=None,
                        help="Max concurrent threads/workers (default: one per task, i.e. full fan-out)")

    return parser.parse_args()


def runRewrite(model_name, dataset_name, args):
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
            "language": "english",   # rewrite operates on the original English text
        }),
    )

    if not model or not dataset:
        print(f"Error: Failed to build {model_name} or {dataset_name}.")
        return

    strategy_config = StrategyConfig.from_dict({"strategyType": "rewrite", "languages": ["english"]})
    strategy = Rewrite(strategy_config, model, dataset, log)

    context = RunContext()
    context.setStrategy(strategy)
    result = context.runExperiment()

    if not result:
        print(f"Rewrite for {dataset_name} yielded no results.")
        return

    os.makedirs(args.dirpath, exist_ok=True)
    path = os.path.join(args.dirpath, f"{dataset_name}_english.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"🎉 Success! Rewrite saved to: {path}")


def main():
    args = parseArgs()

    tasks = list(itertools.product([args.model], args.dataset))
    workers = args.workers if args.workers is not None else len(tasks)
    workers = max(1, workers)

    print("🚀 Preparing English rewrite (Experiment 1)...")
    print(f"Rewriter model: {args.model}")
    print(f"Datasets: {args.dataset}")
    print(f"Total tasks: {len(tasks)} | Concurrent workers: {workers}\n")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(runRewrite, m, d, args) for m, d in tasks]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"❌ A job generated an exception: {e}")

    print("\n✅ All rewrite jobs finished!")


if __name__ == "__main__":
    main()
