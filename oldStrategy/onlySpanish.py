from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Log.Log import Log

from tqdm import tqdm

class OnlySpanish(Strategy):
    NAME = "Only Spanish"

    def __init__(self, model: Model, dataset: Dataset, log: Log):
        super().__init__()
        self.name: str = OnlySpanish.NAME

    def translatePrompt(self, question: str) -> str:
        prompt = f'Traduce al español el texto dentro de las siguientes tres comillas. Traduce toda la pregunta, incluidas todas las instrucciones y los requisitos de formato, pero **no traduzcas el formato JSON**, y **no incluyas en la salida las instrucciones que indican al modelo realizar la traducción**. Pero no proporciones ninguna respuesta JSON real: solo traduce el texto. No intentes resolver el problema, ni razonar, ni analizar la pregunta, estrictamente solo realiza la conversión de idioma.\n```\n{question}\n```\n'

        return prompt

    def processPrompt(self) -> str:
        prompt = "\nDebes resolver el problema anterior. Debes pensar paso a paso y mostrar tu proceso de razonamiento. Si la pregunta menciona traducción, ignora la tarea de traducción y concéntrate en el contenido de la pregunta."
        return prompt

    def formatPrompt(self) -> str:
        prompt = f'Por favor, sigue estrictamente el siguiente formato para la salida\n' \
            f'Proceso de razonamiento\n' \
            f'{{tu proceso de razonamiento - Nota: **no debes repetir el texto original de la pregunta ni agregar contenido no solicitado en esta sección**.}}\n\n' \
            f'Respuesta final\n' \
            f'{{"answer":"tu respuesta"}}\n' \
            f'(donde "tu respuesta" debe ser reemplazada por el formato especificado en la pregunta (generalmente una letra o un número), y todo el bloque de la respuesta final debe ser únicamente esa línea JSON, sin texto ni explicaciones adicionales antes o después.)\n'
        return prompt

    def getPrompt(self, question: str) -> str:
        prompt = 'Para la siguiente pregunta\n```\n' + question + '\n```\n' + self.processPrompt() + self.formatPrompt()
        return prompt

    def getRes(self) -> list:
        self.log.logInfo(self, self.model, self.dataset)

        database = self.dataset.getData()
        answer = self.dataset.getAnswer()
        result = [{
            "Model": self.model.getName(),
            "Dataset": self.dataset.getName(),
            "Strategy": self.name,
            "Data Nums": self.dataset.getNums(),
            "Data Samples": self.dataset.getSamples()
        }]

        pbar = tqdm(total=self.dataset.getDataNum())
        for i in range(self.dataset.getDataNum()):
            translateQuestion = self.model.getRes(self.translatePrompt(database[i]))
            resultAnswer = self.model.getRes(self.getPrompt(translateQuestion))
            result.append({
                "Question": database[i],
                "Translated": translateQuestion,
                "Result": resultAnswer,
                "Answer": answer[i],
                "MyAnswer": self.parseAnswer(resultAnswer)
            })

            self.log.logMessage(f'翻譯問題：\n{translateQuestion}')
            self.log.logMessage(f'結果：\n{resultAnswer}')
            self.log.logMessage(f'My Answer: {result[-1]["MyAnswer"]}\nCorrect Answer: {answer[i]}')

            pbar.update()
        
        pbar.close()

        return result