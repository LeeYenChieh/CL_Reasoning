from File.FileFactory import FileFactory
from File.File import File
from Strategy.StrategyType import STRATEGY_TO_NAME, STRATEGY_LIST
from Dataset.DatasetType import get_dataset_map, DATASET_LIST
from Model.ModelType import MODEL_LIST

class DataReader():
    def __init__(self, dir: str="", model: list=None, dataset: list=None, strategy: list=None):
        self.dir = dir

        if model == None:
            model = MODEL_LIST
        if dataset == None:
            dataset = DATASET_LIST
        if strategy == None:
            strategy = STRATEGY_LIST
        self.model = model
        self.dataset = dataset
        self.strategy = strategy
        
        self.strategy_map = {STRATEGY_TO_NAME[s]: i for i, s in enumerate(self.strategy)}


    def getDataset(self, nums: int=1000, split: float=0.8):
        """
        回傳:
        (train_texts, train_labels), (val_texts, val_labels)
        labels 格式為 List[List[int]], 例如 [[1, 0, 1], [0, 0, 1]]
        """

        factory = FileFactory()
        train_texts, train_labels = [], []
        val_texts, val_labels = [], []

        for m in self.model:
            for d in self.dataset:
                files: list[File] = factory.getFileBySetting(self.dir, [m], [d], self.strategy)

                if len(files) != len(self.strategy):
                    print(f"Warning: Model {m} on Dataset {d} missing strategy files. Skipping.")
                    continue
                
                realnums = nums
                for f in files:
                    if realnums > f.getDataNums():
                        realnums = f.getDataNums()
                        print(f'{m} {d} datanums = {realnums}')
                
                train_nums = int(realnums * split)
                temp_texts, temp_labels = [], []
                for idx in range(realnums):
                    one_label = [None] * len(self.strategy)
                    for f in files:
                        item = f.getData()[idx]
                        temp_texts.append(item.get("Translated"))
                        one_label[self.strategy_map[f.getStrategyName()]] = 1 if get_dataset_map()[f.getDatasetName()].compareTwoAnswer(item.get("Answer"), item.get("MyAnswer")) else 0
                    temp_labels += [one_label] * len(files)
                
                train_texts += temp_texts[0:len(self.strategy) * train_nums]
                train_labels += temp_labels[0:len(self.strategy) * train_nums]
                val_texts += temp_texts[len(self.strategy) * train_nums:]
                val_labels += temp_labels[len(self.strategy) * train_nums:]
        
        return (train_texts, train_labels), (val_texts, val_labels)

