from argparse import ArgumentParser
from RunContext import RunContext

from Model.Model import Model
from Model.ModelFactory import ModelFactory
from Model.ModelType import MODEL_LIST
from Dataset.Dataset import Dataset
from Dataset.DatasetFactory import DatasetFactory
from Dataset.DatasetType import DATASET_LIST

from Strategy.StrategyType import STRATEGY_LIST

from TestContext import TestContext
from Test.TestType import TEST_LIST
from File.FileFactory import FileFactory

import json

def parseArgs():
    parser = ArgumentParser()
    parser.add_argument("--run", action="store_true", help="Run Experiment")
    parser.add_argument("--test", action="store_true", help="Test Experiment")

    parser.add_argument("-m", "--model", choices=MODEL_LIST, help="choose your model")
    parser.add_argument("-d", "--dataset", choices=DATASET_LIST, help="choose your dataset")
    parser.add_argument("-s", "--strategy", choices=STRATEGY_LIST, help="choose your strategy")
    parser.add_argument("--datapath1", help="multi agent response 1")
    parser.add_argument("--datapath2", help="multi agent response 2")
    parser.add_argument("--nums", help="Data Nums", type=int)
    parser.add_argument("--dirpath", help="your dir path")
    parser.add_argument("--filepath", help="your file path")

    parser.add_argument("-t", "--testmode", choices=TEST_LIST, help="choose your test stratey")
    parser.add_argument("--testfile", help="The file need to be test")
    parser.add_argument("--testmodel", choices=MODEL_LIST, nargs="+", help="The model you want to test")
    parser.add_argument("--testdataset", choices=DATASET_LIST, nargs="+", help="The dataset you want to test")
    parser.add_argument("--teststrategy", choices=STRATEGY_LIST, nargs="+", help="The strategy you want to test")

    args = parser.parse_args()
    return args

def runExperiment(args):
    modelFactory = ModelFactory()
    model: Model = modelFactory.buildModel(args.model)
    datasetFactory = DatasetFactory()
    dataset: Dataset = datasetFactory.buildDataset(args.dataset, nums = args.nums) if args.nums else datasetFactory.buildDataset(args.dataset)

    context = RunContext()
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

def textExperiment(args):
    fileFactory: FileFactory = FileFactory()
    test_models = args.testmodel
    if not test_models and args.model:
        test_models = [args.model]
    if args.testfile:
        file = [fileFactory.getFileByPath(args.testfile)]
    else:
        file = fileFactory.getFileBySetting(args.testmodel, args.testdataset, args.teststrategy)
    context: TestContext = TestContext()
    context.setTest(args.testmode)
    context.runTest(file)

def main():
    args = parseArgs()
    if args.run:
        print("Run Experiment Prepare")
        runExperiment(args)
    if args.test:
        print("Test Performance")
        textExperiment(args)

if __name__ == '__main__':
    main()
