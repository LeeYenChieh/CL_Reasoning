from argparse import ArgumentParser

from Model.ModelType import MODEL_LIST
from Dataset.DatasetType import DATASET_LIST
from Strategy.StrategyType import STRATEGY_LIST

from MultiLabelTrainer.DataReader import DataReader
from MultiLabelTrainer.MultiLabelDataset import MultiLabelDataset
from MultiLabelTrainer.Metric import compute_metrics

from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
from transformers import TrainingArguments, Trainer

def parseArgs():
    parser = ArgumentParser()
    
    parser.add_argument("-m", "--model", nargs="+", choices=MODEL_LIST, help="choose your model")
    parser.add_argument("-d", "--dataset", nargs="+", choices=DATASET_LIST, help="choose your dataset")
    parser.add_argument("-s", "--strategy", nargs="+", choices=STRATEGY_LIST, help="choose your strategy")
    parser.add_argument("--dirpath", help="your dir path")
    parser.add_argument("--split", default=0.7, type=float, help="split train - val")
    parser.add_argument("--data nums", default=1000, type=int, help="total data nums")
    parser.add_argument("--maxlens", default=512, type=int, help="data max length")

    args = parser.parse_args()
    return args

def main():
    args = parseArgs()
    
    (train_texts, train_labels), (val_texts, val_labels) = DataReader(args.dirpath, args.model, args.dataset, args.strategy)
    model_name = "xlm-roberta-base"
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)
    train_dataset = MultiLabelDataset(train_texts, train_labels, tokenizer, args.maxlens)
    val_dataset = MultiLabelDataset(val_texts, val_labels, tokenizer, args.maxlens)
    
    model = XLMRobertaForSequenceClassification.from_pretrained(
        model_name, 
        num_labels=len(args.strategy), 
        problem_type="multi_label_classification" 
    )

    args = TrainingArguments(
        output_dir="xlm-roberta-multilabel-output",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=5,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f0.5_micro", # 多標籤通常看 F1-Micro

        logging_strategy="steps",
        logging_steps=10,  # 每 10 步紀錄一次 Training Loss (畫圖比較平滑)
        report_to="tensorboard"   # 先設 none，我們下面手動用 Matplotlib 畫圖
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    # 開始訓練
    trainer.train()


if __name__ == '__main__':
    main()