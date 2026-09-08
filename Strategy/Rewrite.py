from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Strategy.StrategyConfig import StrategyConfig
from Log.Log import Log
from Strategy.PromptAbstractFactory.PromptRewriteFactory import PromptRewriteFactory

from tqdm import tqdm


class Rewrite(Strategy):
    """
    Experiment 1: paraphrase every question stem with a single fixed "rewriter" model.

    Structurally identical to Strategy.Translate, but instead of translating into another
    language it rewords the English stem while keeping numbers / names / units / answer
    options verbatim. The output file ([meta, {id, Question, Rewritten}, ...]) is later
    consumed by Dataset._apply_rewrite() during the Experiment 2-4 evaluation runs.
    """
    def __init__(self, config: StrategyConfig, model: Model, dataset: Dataset, log: Log):
        super().__init__(config)

        self.model: Model = model
        self.dataset: Dataset = dataset
        self.log: Log = log

        # Prevents IndexError if config.languages is not provided.
        if self.config.languages:
            self.config.displayName += f" ({self.config.languages[0]})"
        else:
            self.config.displayName += " (english)"

    def getPrompt(self, question: str) -> str:
        """Constructs the rewrite prompt using the Factory pattern."""
        target_lang = self.config.languages[0] if self.config.languages else "english"
        return PromptRewriteFactory().getPrompt(target_lang, question)

    def getRes(self) -> list:
        """Executes the rewrite loop over the dataset and tracks progress."""
        self.log.logInfo(self, self.model, self.dataset)

        database = self.dataset.getData()
        result = [{
            "Model": self.model.config.to_dict(),
            "Dataset": self.dataset.config.to_dict(),
            "Strategy": self.config.to_dict()
        }]

        pbar = tqdm(total=self.dataset.config.dataNums)
        for data in database:
            rewritten_question = self.model.getRes(self.getPrompt(data["question"]))

            result.append({
                "id": data.get("id", "N/A"),
                "Question": data.get("question", ""),
                "Rewritten": rewritten_question
            })

            self.log.logMessage(f'改寫問題 (Rewritten)：\n{rewritten_question}')

            pbar.update()

        pbar.close()

        return result

    @staticmethod
    def getTokenLens(model: Model, data):
        """Calculate token usage for the rewritten text."""
        return model.getTokenLens(data.get("Rewritten", ""))
