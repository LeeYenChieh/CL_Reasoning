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
    parser.add_argument("-m", "--model", help="choose your model")
    parser.add_argument("-d", "--dataset", help="choose your dataset")
    parser.add_argument("-s", "--strategy", help="choose your strategy")
    parser.add_argument("--dirpath", help="your dir path")
    parser.add_argument("--filepath", help="your file path")

    parser.add_argument("--test", action="store_true", help="Run Experiment")
    args = parser.parse_args()
    return args

def runExperiment(args):
    modeFactory = ModelFactory()
    model: Model = modeFactory.buildModel(args.model)
    datasetFactory = DatasetFactory()
    dataset: Dataset = datasetFactory.buildDataset(args.dataset)

    context = Context()
    context.setStrategy(args.strategy)
    result = context.runExperiment(model, dataset)

    if args.dirpath:
        with open(f'{args.dirpath}/{model.getName()}_{dataset.getName()}_{context.getStrategyName()}.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    elif args.filepath:
        with open(f'{args.filepath}', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

def main():
    args = parseArgs()
    print(args.run)
    if args.run:
        print("Run Experiment Prepare")
        runExperiment(args)

if __name__ == 'main':
    main()
