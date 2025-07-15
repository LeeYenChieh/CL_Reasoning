from openai import OpenAI
import json
from api import gpt_api_key
from tqdm import tqdm
import nums_from_string as nfs
from datasets import load_dataset
import string

client = OpenAI(api_key=gpt_api_key)
nums = 500
samples = 1
model = "gpt-4.1-mini-2025-04-14"
letters = list(string.ascii_lowercase)

def createPrompt(response1, response2):
    prompt = f'There is a problem \n' \
    f'--------------------------------------------------------------------------------------\n\n' \
    f'{response1["question"]}\n\n' \
    f'--------------------------------------------------------------------------------------\n' \
    f'有一個只會英文的人給出以下答案\n\n{response1["output"]["response"]} \n\n' \
    f'--------------------------------------------------------------------------------------\n' \
    f'有一個只會中文的人給出以下答案\n\n{response2["output"]["response"]} \n\n' \
    f'--------------------------------------------------------------------------------------\n' \
    f'匯總兩人的全程推理步驟與答案，**並列呈現**。\n- 仔細比較兩份思路和結果，審查是否一致；如不同，請找到推理或計算細節的分歧點，並分析潛在出錯環節；如答案一致，簡明說明原因。\n' \
    f'At the end of the output, provide the answer. The answer must be a single choice and only one English letter (a-e). You cannot output other letters.\n' \
    f'請嚴格遵守以下格式進行輸出\n' \
    f'比較答案\n' \
    f'{{比較過程、是否一致、若不一致時的分歧點與錯誤分析}}\n\n' \
    f'最終答案\n' \
    f'{{公認正確答案（僅一個英文字母(a-e)）}}\n'

    return prompt

def sendPromptToModel(prompt):

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    print(prompt)
    print("=" * 80)
    print(response.choices[0].message.content)

    return {
        "prompt": prompt,
        "response": response.choices[0].message.content
    }

def self_reflection(dataset):
    result = [{
        "model": model
    }]
    correctCnt = 0
    notSureCnt = 0

    pbar = tqdm(total=samples * nums)
    for i in range(nums * samples):
        prompt = createPrompt(dataset["data1"][i + 1], dataset["data2"][i + 1])

        response = sendPromptToModel(prompt)

        # check answer
        correct = False
        try:
            answer = dataset["data1"][i + 1]["answer"]
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
        print(f'correct：{correctCnt}/{i + 1}')
        print(f'notSure：{notSureCnt}/{i + 1}')

        result.append({"index": i, 
                        "question": prompt,
                        "output": response,
                        "answer": dataset["data1"][i + 1]["answer"],
                        "correct":correct,
        })
        pbar.update(1)
    with open(f'./MJLee/mathqa/result/experiment3.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    pbar.close()

    print(f'correct：{correctCnt}/{nums * samples}')
    print(f'notSure：{notSureCnt}/{nums * samples}')

def load_result(path1, path2):
    with open(path1, 'r') as f:
        data1 = json.load(f)
    with open(path2, 'r') as f:
        data2 = json.load(f)

    return {
        "data1": data1,
        "data2": data2
    }

def main():
    dataset = load_result(f'./MJLee/mathqa/result/experiment1.json', f'./MJLee/mathqa/result/experiment2.json')
    self_reflection(dataset)


if __name__ == '__main__':
    main()