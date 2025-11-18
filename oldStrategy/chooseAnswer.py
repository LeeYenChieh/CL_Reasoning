from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Log.Log import Log

from tqdm import tqdm
import json

class ChooseAnswer(Strategy):
    NAME = "Choose Answer"
    def __init__(self):
        super().__init__()
        self.name: str = ChooseAnswer.NAME
    
    def chooseOnePromptCN(self, chinese_question, chinese_answer, english_answer):
        prompt = f'對於以下問題\n```\n{chinese_question}\n```\n有一個中文答案跟一個英文答案，分別是\n```\n{chinese_answer}\n```\n以及\n```\n{english_answer}\n```\n\n' \
            f'任務（必須**依序**完成）\n：' \
                f'1) **整理題目中所有必須遵守的指令**（例如：輸出格式、JSON 結構、需/不可進行的推理步驟、答案型式限制等），以條列式清楚列出。\n' \
                f'2) 先**一步一步**檢查題目確保自己有完全理解題目\n' \
                f'3) **檢查兩個答案的推理正確性與是否遵守第1步列出的指令**，對每一個答案明確指出：\n' \
                    f'- 推理是否正確（步驟需逐步呈現、數學運算要逐位/逐步計算並標示單位，逐步計算、推理，單位正確），\n' \
                    f'- 是否遵守格式要求，\n' \
                    f'- 優點（哪裡做得對）與缺點（哪裡出錯或違規）。\n' \
                f'4) **比較兩個答案的差異**，說明哪一個更符合題目要求（包含題意理解、推理正確性、答案正確性、格式遵守、以及是否照題目指示在最後要以 JSON 回答等）。\n' \
                f'5) **選出最終答案**：\n' \
                f'- 若僅有一個答案「題意理解正確、推理過程正確、答案正確」，直接選取該答案；\n' \
                f'- 若兩者皆有缺陷，選擇「缺陷較少者」並說明理由；\n' \
                f'- 最終答案必須遵守題目要求的格式，且輸出必須遵守題目要求的 JSON 結構。\n' \
                f'嚴格輸出格式（**務必完全符合**，不能加任何多餘文字或額外標記）：\n' \
                    f'推理過程\n' \
                    f'{{你的推理過程 — 包含第1~5步的完整內容與計算、推理過程。注意：**不得重述題目原文或在此加入題目未要求的內容**。數學計算要逐步列出並標示單位。}}\n' \
                    f'最終答案\n' \
                    f'{{"answer":"your answer"}}\n' \
                    f'（其中 "your answer" 應該且必須被取代為題目指定的格式(格式通常是一個英文字母或數字)，整個最終答案區塊只能是那一行 JSON，前後不能有其他文字或說明。）\n' \
                f'額外規定與注意事項（請遵守）：\n' \
                    f'- 推理過程必須包含：從題目擷取出的「必遵指令清單」、對兩個答案的逐條檢驗（含數學驗算、推理過程）、兩者比較、以及最終選擇的理由。\n' \
                    f'- **不得重述原題內容**；可以引用或摘錄答案中重要句子作為檢驗依據，但不要把題目原文再貼回輸出。\n' \
                    f'- 若題目要求最終以 JSON 回答（如上），你在「最終答案」區塊**只**能輸出那行 JSON；任何附註都必須放在「推理過程」區塊內。\n' \
                    f'- 若計算結果與選項皆不相符，仍須在「推理過程」中清楚呈現完整運算與判斷標準，並根據「選擇原則」（完全合規者優先；若皆有缺陷，選擇缺陷較少者）做出最終選擇。\n' \
                    f'- 不可提出要補充資料的要求；收到輸入後即刻依現有資訊完成任務。\n' \
                    f'- 所有推理、算術演算請逐步列出，並標明單位（例如：km/h → m/s、秒→小時等必要換算步驟要顯示）。\n' \
                f'現在請以此格式執行評估。\n'
        return prompt

    def chooseOnePromptEN(self, english_question, chinese_answer, english_answer):
        prompt = f'For the following question\n```\n{english_question}\n```\nThere is a Chinese answer and an English answer, respectively\n```\n{chinese_answer}\n```\nand\n```\n{english_answer}\n```\n\n' \
            f'Tasks (must be completed **in order**)\n:' \
                f'1) **List all the instructions that must be followed in the question** (e.g., output format, JSON structure, reasoning steps required/not required, answer format restrictions, etc.), clearly listed in bullet points.\n' \
                f'2) First **check the question step by step** to ensure you have fully understood it.\n' \
                f'3) **Check the correctness of the reasoning of the two answers and whether they comply with the instructions listed in step 1**. For each answer, clearly point out:\n' \
                    f'- Whether the reasoning is correct (steps must be shown step by step, arithmetic must be calculated digit by digit/step by step and units must be indicated, step-by-step calculation and reasoning, units correct),\n' \
                    f'- Whether it complies with the language and format requirements,\n' \
                    f'- Advantages (what is done correctly) and disadvantages (where it goes wrong or violates the rules).\n' \
                f'4) **Compare the two answers** and explain which one better meets the question requirements (including understanding of the question, correctness of reasoning, correctness of answer, compliance with format, and whether it follows the instruction to give the final answer in JSON, etc.).\n' \
                f'5) **Select the final answer**:\n' \
                f'- If only one answer has “correct understanding of the question, correct reasoning process, correct answer,” directly select that answer;\n' \
                f'- If both have flaws, select the one with “fewer flaws” and explain why;\n' \
                f'- The final answer must comply with the required format of the question, and the output must follow the required JSON structure.\n' \
                f'Strict output format (**must be fully complied with**, no extra text or marks allowed):\n' \
                    f'Reasoning process\n' \
                    f'{{Your reasoning process — including the complete content and calculations/reasoning process of steps 1–5. Note: **Do not restate the original question text or add content not required by the question**. Mathematical calculations must be shown step by step and with units.}}\n' \
                    f'Final answer\n' \
                    f'{{"answer":"your answer"}}\n' \
                    f'(Where "your answer" must and should strictly follow the rules(Usually a English letter or a number) required in the question. The entire final answer block must only be that one line of JSON, with no extra text or explanation before or after.)\n' \
                f'Additional rules and notes (must be followed):\n' \
                    f'- The reasoning process must include: the “must-follow instruction list” extracted from the question, a step-by-step check of both answers (including mathematical verification, reasoning process), comparison of the two, and the reason for the final choice.\n' \
                    f'- **Do not restate the original question text**; you may quote or extract key sentences from the answers as evidence, but do not paste the original question back into the output.\n' \
                    f'- If the question requires the final answer in JSON (as above), then in the “Final answer” block you can **only** output that line of JSON; any notes must be placed in the “Reasoning process” block.\n' \
                    f'- If the calculation result does not match any options, you must still clearly show the complete calculation and judgment criteria in the “Reasoning process,” and select the final answer based on the “selection principle” (fully compliant answers take priority; if both have flaws, choose the one with fewer flaws).\n' \
                    f'- Do not request additional information; once inputs are received, immediately complete the task with the available information.\n' \
                    f'- All reasoning and arithmetic must be shown step by step, with units (e.g., km/h → m/s, seconds → hours, etc. All necessary conversions must be shown).\n' \
                f'Now please perform the evaluation in this format.\n'
        return prompt
    
    def getPrompt(self, chinese_question, english_question, chinese_answer, english_answer, betterLanguage):
        if len(chinese_answer) > 2048:
            chinese_answer = chinese_answer[0:2048] + '一直重複運算，結束輸出'
        if len(english_answer) > 2048:
            english_answer = english_answer[0:2048] + 'repeatlt compute the same thing, end the output'
        prompt = self.chooseOnePromptCN(chinese_question, chinese_answer, english_answer)
        if betterLanguage == 'CN':
            prompt = self.chooseOnePromptEN(english_question, chinese_answer, english_answer)
        return prompt
    
    def getRes(self, model: Model, dataset: Dataset, log: Log, dataPath1: str=None, dataPath2: str=None, betterLanguage: str='EN') -> list:
        if dataPath1 == None or dataPath2 == None:
            print("Use default file(onlyChinese and onlyEnglish output file)!")
            from Strategy.onlyChinese import OnlyChinese
            from Strategy.onlyEnglish import OnlyEnglish
            dataPath1 = f'result/{model.getName()}_{dataset.getName()}_{OnlyChinese.NAME}.json'
            dataPath2 = f'result/{model.getName()}_{dataset.getName()}_{OnlyEnglish.NAME}.json'

        log.logInfo(self, model, dataset, dataPath1, dataPath2)

        try:
            with open(dataPath1, 'r') as f:
                data1 = json.load(f)
            with open(dataPath2, 'r') as f:
                data2 = json.load(f)
        except:
            log.logMessage(f'\nRead File Error!')
            return []

        if data1[0]["Data Nums"] != dataset.getNums() or data1[0]["Data Samples"] != dataset.getSamples() or data2[0]["Data Nums"] != dataset.getNums() or data2[0]["Data Samples"] != dataset.getSamples():
            log.logMessage(f'\nNums or Samples of Data in path1 or path2 doesn\'t match your setting!')
            return []

        result = [{
            "Model": model.getName(),
            "Dataset": dataset.getName(),
            "Strategy": self.name,
            "Data Nums": dataset.getNums(),
            "Data Samples": dataset.getSamples()
        }]

        pbar = tqdm(total=dataset.getDataNum())
        for i in range(dataset.getDataNum()):
            chinese_question, english_question, chinese_result, english_result = data1[i + 1]["Translated"], data2[i + 1]["Translated"], data1[i + 1]["Result"], data2[i + 1]["Result"]
            chinese_answer, english_answer = data1[i + 1]["MyAnswer"], data2[i + 1]["MyAnswer"]
            correct_answer = data2[i + 1]["Answer"]

            prompt = ""
            resultOutput = ""
            myAnswer = ""

            if dataset.compareTwoAnswer(chinese_answer, english_answer):
                myAnswer = chinese_answer
                # log.logMessage(f'問題：{chinese_question}')
                # log.logMessage(f'結果：兩個Agent有相同結果！')

            else:
                prompt = self.getPrompt(chinese_question, english_question, chinese_result, english_result, betterLanguage)
                resultOutput = model.getRes(prompt)
                myAnswer = self.parseAnswer(resultOutput)
                log.logMessage(f'問題：{chinese_question}')
                log.logMessage(f'Prompt：{prompt}')
                log.logMessage(f'結果：{resultOutput}')
                log.logMessage(f'My Answer: {myAnswer}\nCorrect Answer: {correct_answer}')

            result.append({
                "English Question": english_question,
                "Chinese Question": chinese_question,
                "Prompt": prompt,
                "Result": resultOutput,
                "Answer": correct_answer,
                "MyAnswer": myAnswer
            })

            pbar.update()
        
        pbar.close()

        return result