from openai import OpenAI
import json
from api import gpt_api_key
from tqdm import tqdm
import nums_from_string as nfs
from datasets import load_dataset

client = OpenAI(api_key=gpt_api_key)
nums = 500
model = "gpt-4o-mini-2024-07-18"

def self_reflection(dataset):
    result = [{
        "model": model
    }]
    cnt = 0
    for i in tqdm(range(nums)):
        problem = f'There is a Problem: \n{dataset[i]["question"]}.\n' \
        f'And there are four choices\n' \
        f'A: {dataset[i]["mc1_targets"]["choices"][0]}\n' \
        f'B: {dataset[i]["mc1_targets"]["choices"][1]}\n' \
        f'C: {dataset[i]["mc1_targets"]["choices"][2]}\n' \
        f'D: {dataset[i]["mc1_targets"]["choices"][3]}\n' \
        f'Please choose a choice based on the question' \
        f'At the end of the output, provide the answer. The answer must be a single choice and only one English letter (A/B/C/D).'

        translateProblem = client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[{"role": "user", "content": f'請將以下問題翻譯成中文，不啟動推理、分析，也不添加任何註解，嚴格只進行語言轉換\n\n{problem}'}],
            temperature=0.2
        )

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": translateProblem.choices[0].message.content}],
            temperature=0.2
        )
        print(translateProblem.choices[0].message.content)
        print("=" * 40)
        print(response.choices[0].message.content)
        correct = True if int(dataset[i]["answers_spans"]["spans"][0]) == nfs.get_nums(response.choices[0].message.content)[-1] else False
        if correct:
            cnt += 1
        result.append({"index": i, 
                        "question": problem,
                        "output": response.choices[0].message.content,
                        "answer": int(dataset[i]["answers_spans"]["spans"][0]),
                        "correct":correct,
        })
    with open(f'./MJLee/truthfulqa/result/experiment2.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f'total：{cnt}/{nums}')

def main():
    dataset = load_dataset("truthfulqa/truthful_qa", "multiple_choice", split="validation")

    self_reflection(dataset)
    

if __name__ == '__main__':
    main()