from argparse import ArgumentParser
from Strategy.RunContext import RunContext

from Model.Model import Model
from Model.ModelFactory import ModelFactory
from Model.ModelType import MODEL_LIST

from Dataset.Dataset import Dataset
from Dataset.DatasetFactory import DatasetFactory
from Dataset.DatasetType import DATASET_LIST

from Strategy.StrategyType import STRATEGY_LIST, StrategyType
from Strategy.OnlyOneLanguage import OnlyOneLanguage
from Strategy.SelfReflection import SelfReflection
from Strategy.Repair import Repair
from Strategy.Challenge import Challenge
from Strategy.GetOneResult import GetOneOutput

from Log.Log import Log
from Log.OneAgentLog import OneAgentLog
from Log.TwoAgentLog import TwoAgentLog

from Test.TestContext import TestContext
from Test.TestEM import TestEM
from Test.PrintOne import PrintOne
from Test.TestCaseBase import TestCaseBase
from Test.TestType import TEST_LIST, TestType
from File.FileFactory import FileFactory

import json

def parseArgs():
    parser = ArgumentParser()
    parser.add_argument("--run", action="store_true", help="Run Experiment")
    parser.add_argument("--test", action="store_true", help="Test Experiment")

    parser.add_argument("-m", "--model", choices=MODEL_LIST, help="choose your model")
    parser.add_argument("--tempature", default=0, type=float, help="Tempature")

    parser.add_argument("-d", "--dataset", choices=DATASET_LIST, help="choose your dataset")
    parser.add_argument("--nums", help="Data Nums", default=-1, type=int)
    parser.add_argument("--sample", help="Data Sample", default=1, type=int)

    parser.add_argument("-s", "--strategy", choices=STRATEGY_LIST, help="choose your strategy")
    parser.add_argument("--repairpath", help="The file you need to repair")
    parser.add_argument("--datapath1", help="Two Result Path 1")
    parser.add_argument("--datapath2", help="Two Result Path 2")
    parser.add_argument("--threshold", type=int, default=3, help="Challenge Threshold 3")

    parser.add_argument("--dirpath", help="your dir path")
    parser.add_argument("--filepath", help="your file path")


    parser.add_argument("-t", "--testmode", choices=TEST_LIST, help="choose your test stratey")
    parser.add_argument("--testfile", help="The file need to be test")
    parser.add_argument("--testdir", help="The dir need to be test")
    parser.add_argument("--testmodel", choices=MODEL_LIST, nargs="+", help="The model you want to test")
    parser.add_argument("--testdataset", choices=DATASET_LIST, nargs="+", help="The dataset you want to test")
    parser.add_argument("--teststrategy", choices=STRATEGY_LIST, nargs="+", help="The strategy you want to test")

    args = parser.parse_args()
    return args

def runExperiment(args):
    model, dataset = None, None
    if args.model:
        modelFactory = ModelFactory()
        model: Model = modelFactory.buildModel(args.model, tempature=args.tempature)
    if args.dataset:
        datasetFactory = DatasetFactory()
        dataset: Dataset = datasetFactory.buildDataset(args.dataset, nums = args.nums, sample = args.sample)

    context = RunContext()
    if args.strategy == StrategyType.ONLYCHINESE or args.strategy == StrategyType.ONLYENGLISH or args.strategy == StrategyType.ONLYSPANISH:
        context.setStrategy(OnlyOneLanguage(model, dataset, OneAgentLog(), args.strategy))

    elif args.strategy == StrategyType.REPAIR:
        file = FileFactory().getFileByPath(args.repairpath)
        context.setStrategy(Repair(model, dataset, OneAgentLog(), file))

    elif args.strategy == StrategyType.SELFREFLECTION:
        dataFile = FileFactory().getFileByPath(args.datapath)
        context.setStrategy(SelfReflection(model, dataset, OneAgentLog(), dataFile))

    elif args.strategy == StrategyType.GETONEOUTPUT:
        context.setStrategy(GetOneOutput(model, dataset, Log()))

    elif args.strategy == StrategyType.CHALLENGE:
        dataFile1, dataFile2 = None, None
        if args.datapath1 and args.datapath2:
            fileFactory = FileFactory()
            dataFile1 = fileFactory.getFileByPath(args.datapath1)
            dataFile2 = fileFactory.getFileByPath(args.datapath2)
        context.setStrategy(Challenge(model, dataset, TwoAgentLog(), args.threshold, dataFile1, dataFile2))

    result = context.runExperiment()

    if not result:
        return
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
    if args.testfile:
        file = [fileFactory.getFileByPath(args.testfile)]
    else:
        file = fileFactory.getFileBySetting(args.testdir, args.testmodel, args.testdataset, args.teststrategy)

    context: TestContext = TestContext()
    if args.testmode == TestType.TESTEM:
        context.setTest(TestEM())
    elif args.testmode == TestType.PRINTONE:
        context.setTest(PrintOne())
    elif args.testmode == TestType.TESTCASE:
        context.setTest(TestCaseBase())
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
