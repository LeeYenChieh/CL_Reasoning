from openai import OpenAI
import json
from api import gpt_api_key
from tqdm import tqdm
import nums_from_string as nfs
from datasets import load_dataset
import string

developerPrompt = f'這邊有一個問題，你要用以下幾個階段去回答問題\n' \
    f'1. 翻譯階段\n' \
    f'請將以下文字翻譯成中文以及英文，請不要嘗試解決問題，不要推理、分析題目，也不添加任何註解，嚴格只進行語言轉換，不能輸出任何關於答案以及過程的資訊，只要輸出原本題目的翻譯就好\n' \
    f'2. 答題階段\n' \
    f'請分別回答中文問題以及英文問題，在回答中文問題時不能參考英文問題與英文問題的答案，在回答英文問題時不能參考中文問題與中文問題的答案' \
    f'3. 比較與檢查\n' \
    f'匯總兩人的全程推理步驟與答案，**並列呈現**。\n- 仔細比較兩份思路和結果，審查是否一致；如不同，請找到推理或計算細節的分歧點，並分析潛在出錯環節；如答案一致，簡明說明原因。\n' \
    f'4. 輸出格式規範\n\n' \
    f'中文問題與選項\n' \
    f'{{翻譯後的中文問題與選項}}\n\n' \
    f'英文問題與選項\n' \
    f'{{翻譯後的英文問題與選項}}\n\n' \
    f'—————————————\n' \
    f'中文問題的推理過程\n' \
    f'{{你的中文問題的推理過程}}\n\n' \
    f'中文問題的答案\n' \
    f'{{你的中文問題的答案(只能是一個英文字母)}}\n' \
    f'—————————————\n' \
    f'英文問題的推理過程\n' \
    f'{{你的英文問題的推理過程}}\n\n' \
    f'英文問題的答案\n' \
    f'{{你的英文問題的答案(只能是一個英文字母)}}\n' \
    f'—————————————\n' \
    f'比較答案\n' \
    f'{{比較過程、是否一致、若不一致時的分歧點與錯誤分析}}\n\n' \
    f'最終答案\n' \
    f'{{公認正確答案（僅一個英文字母(a-e)）}}\n'

client = OpenAI(api_key=gpt_api_key)
nums = 2900
samples = 3
model = "gpt-4.1-mini-2025-04-14"
letters = list(string.ascii_lowercase)

def createPrompt(question, choices):
    prompt = f'There is a Problem: \n{question}.\n' \
    f'And there are 5 choices\n' \
    f'{choices}\n' \
    f'Please choose a choice based on the question\n' \
    f'At the end of the output, provide the answer. The answer must be a single choice and only one English letter (a-e). You cannot output other letters.\n' \
    f'你必須嚴格按照格式進行輸出\n'

    return prompt

def sendPromptToModel(prompt):
    translateProblem = client.chat.completions.create(
        model="gpt-4.1-2025-04-14",
        messages=[{"role": "user", "content": f'請將以下文字翻譯成中文，請不要嘗試解決問題，不要推理、分析題目，也不添加任何註解，嚴格只進行語言轉換，不能輸出任何關於答案以及過程的資訊，只要輸出原本題目的翻譯就好\n\n"{prompt}"'}],
        temperature=0
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": developerPrompt + '\n' * 2 + translateProblem.choices[0].message.content}],
        max_tokens=1024,
        temperature=0
    )

    print(prompt)
    print("=" * 80)
    print(translateProblem.choices[0].message.content)
    print("=" * 80)
    print(response.choices[0].message.content)

    return {
        "prompt": prompt,
        "translate": translateProblem.choices[0].message.content,
        "response": response.choices[0].message.content
    }

def self_reflection(dataset):
    result = [{
        "model": model
    }]
    correctCnt = 0
    notSureCnt = 0

    pbar = tqdm(total=samples * nums)
    for i in range(nums):
        prompt = createPrompt(dataset[i]["Problem"], dataset[i]["options"])

        for j in range(samples):
            response = sendPromptToModel(prompt)

            # check answer
            correct = False
            try:
                answer = dataset[i]["correct"]
                output = response["response"].split('\n')[-1][-1]
                if output not in letters:
                    raise TypeError()
                if answer == output:
                    correct = True
                    correctCnt += 1
            except:
                correct = "true/false"
                notSureCnt += 1
            print(correct)
            print(f'correct：{correctCnt}/{i * samples + j + 1}')
            print(f'notSure：{notSureCnt}/{i * samples + j + 1}')

            result.append({"index": i * samples + j, 
                            "question": prompt,
                            "output": response,
                            "answer": dataset[i]["correct"],
                            "correct":correct,
            })
            pbar.update(1)
    with open(f'./MJLee/mathqa/result/experiment8.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    pbar.close()

    print(f'correct：{correctCnt}/{nums * samples}')
    print(f'notSure：{notSureCnt}/{nums * samples}')

def load_dataset(json_path):
    with open(f'./MJLee/mathqa/{json_path}', 'r') as f:
        data = json.load(f)
    return data[0:nums]

def main():
    dataset = load_dataset("test.json")
    self_reflection(dataset)

if __name__ == '__main__':
    main()