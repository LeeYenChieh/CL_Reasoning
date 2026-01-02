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
                

                batch_texts, batch_labels = [], []
                batch_lack_texts, batch_lack_labels = [], []
                for idx in range(nums):
                    temp_texts = []
                    temp_label = [None] * len(self.strategy)
                    for f in files:
                        if f.getDataNums() < nums:
                            temp_label[self.strategy_map[f.getStrategyName()]] = -1
                            continue
                        item = f.getData()[idx]
                        temp_texts.append(item.get("Translated"))
                        temp_label[self.strategy_map[f.getStrategyName()]] = 1 if get_dataset_map()[f.getDatasetName()].compareTwoAnswer(item.get("Answer"), item.get("MyAnswer")) else 0
                    if -1 not in temp_label and temp_label != [1] * len(files):
                        batch_texts += temp_texts
                        batch_labels += [temp_label] * len(files)
                    if -1 in temp_label and 0 not in temp_label:
                        batch_lack_texts += temp_texts
                        batch_lack_labels += temp_label * len(temp_texts)
                
                batch_train_size = int(len(batch_texts) * split)
                lack_train_size = int(len(batch_lack_texts) * split)

                train_texts += batch_texts[0:batch_train_size]
                train_labels += batch_labels[0:batch_train_size]
                val_texts += batch_texts[batch_train_size:]
                val_labels += batch_labels[batch_train_size:]
                train_texts += batch_lack_texts[0:lack_train_size]
                train_labels += batch_lack_labels[0:lack_train_size]
                val_texts += batch_lack_texts[lack_train_size:]
                val_labels += batch_lack_labels[lack_train_size:]
        
        return (train_texts, train_labels), (val_texts, val_labels)

