from argparse import ArgumentParser
from Context import Context

from Model.Model import Model
from Model.ModelFactory import ModelFactory
from Dataset.Dataset import Dataset
from Dataset.DatasetFactory import DatasetFactory

import json

def parseArgs():
    parser = ArgumentParser()
    parser.add_argument("--run", action="store_true", help="Run Experiment")
    parser.add_argument("-m", "--model", choices=['gpt4.1mini', 'gpt4omini', 'deepseek', 'gemini', 'gemma'], help="choose your model")
    parser.add_argument("-d", "--dataset", choices=['mathqa', 'commenseqa', 'mgsm', 'mmlu', 'truthfulqa', 'xcopa'], help="choose your dataset")
    parser.add_argument("-s", "--strategy", choices=["onlyChinese", "onlyEnglish", "multiAgent"], help="choose your strategy")
    parser.add_argument("--datapath1", help="multi agent response 1")
    parser.add_argument("--datapath2", help="multi agent response 2")
    parser.add_argument("--nums", help="Data Nums", type=int)
    parser.add_argument("--dirpath", help="your dir path")
    parser.add_argument("--filepath", help="your file path")

    parser.add_argument("--test", action="store_true", help="Run Experiment")
    args = parser.parse_args()
    return args

def runExperiment(args):
    modelFactory = ModelFactory()
    model: Model = modelFactory.buildModel(args.model)
    datasetFactory = DatasetFactory()
    dataset: Dataset = datasetFactory.buildDataset(args.dataset, nums = args.nums) if args.nums else datasetFactory.buildDataset(args.dataset)

    context = Context()
    context.setStrategy(args.strategy)
    result = context.runExperiment(model, dataset)

    path = ""
    if args.dirpath:
        path = f'{args.dirpath}/{model.getName()}_{dataset.getName()}_{context.getStrategyName()}.json'
    elif args.filepath:
        path = f'{args.filepath}'
    else:
        path = f'{model.getName()}_{dataset.getName()}_{context.getStrategyName()}.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def main():
    args = parseArgs()
    if args.run:
        print("Run Experiment Prepare")
        runExperiment(args)

if __name__ == '__main__':
    main()
