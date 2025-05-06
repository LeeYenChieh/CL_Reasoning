import openai
import json
from api import api_key
from tqdm import tqdm
import nums_from_string as nfs
from datasets import load_dataset

textWithoutProblem = f'Please translate it into Chinese and English. During the translation, continuously compare the translation with the original problem to ensure accuracy. Do not attempt to solve the problem during the translation process; only focus on translation.\n' \
f'After completing the translations, treat the two problems as separate problems and solve them in their respective languages. For example, solve the Chinese problem in Chinese, the English problem in English, and so on.\n' \
f'You are now going to simulate two AI assistants, each operating in a different language: a Chinese assistant and an English assistant must independently think and solve the problem based solely on the version of the question written in their respective language. Please simulate the behavior of the two assistants one by one, ensuring complete independence between them. \n' \
f'When solving a problem in one language, please ignore all your previous answers to this question. Think about it again from scratch and answer it as if you\'re seeing it for the first time. Do not refer to the answers in other languages. For example, do not refer to the English versions when solving the Chinese problem. Likewise, when solving the English problem, do not reference other versions.\n' \
f'You must think during the problem-solving process; do not simply output the number without a solving process. At the end of each solution, output only the final answer, and the final answer must be in Arabic numeral format (0, 1, 2, 3, 4, 5, 6, 7, 8, 9).\n' \
f'Once all two language versions are solved, compare the answers and processes to see if they are the same or different. If they differ, identify the incorrect process and answer. If they are the same, ensure the process and answer are correct.\n' \
f'After comparison, confirm one final correct answer. At the very end of the output, only the final answer should be shown, and it must be in Arabic numeral format (0, 1, 2, 3, 4, 5, 6, 7, 8, 9).\n'

outputFormat = f'You must strictly follow the output format below.\n' \
f'Format:\n' \
f'Chinese Problem\n' \
f'{{Chinese Problem}}\n\n' \
f'English Problem\n' \
f'{{English Problem}}\n\n' \
f'Chinese Answer\n' \
f'{{Chinese Answer}}\n' \
f'{{Chinese Final Answer}}\n\n' \
f'English Answer\n' \
f'{{English Answer}}\n' \
f'{{English Final Answer}}\n\n' \
f'Compare Answer\n' \
f'{{Compare Answer}}\n\n' \
f'Final Answer\n' \
f'{{Final Answer}}'

openai.api_key = api_key
nums = 50

def self_reflection(dataset):
    result = []
    cnt = 0
    for i in tqdm(range(nums)):
        problem = f'There is a Paragraphs: {dataset[i]["passage"]}.\n' \
        f'Answer questions based on the article \n' \
        f'Question: {dataset[i]["question"]}'
        text = f'There is a problem:\n\n{problem}\n\n{textWithoutProblem + outputFormat}'
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": text}],
            temperature=0.2
        )
        print(response["choices"][0]["message"]["content"])
        correct = True if int(dataset[i]["answers_spans"]["spans"][0]) == nfs.get_nums(response["choices"][0]["message"]["content"])[-1] else False
        if correct:
            cnt += 1
        result.append({"index": i, 
                        "question": text,
                        "output": response["choices"][0]["message"]["content"],
                        "answer": int(dataset[i]["answers_spans"]["spans"][0]),
                        "correct":correct,
        })
    with open(f'./MJLee/drop/result/experiment1.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f'total：{cnt}/{nums}')

def get_nums_dataset(dataset):
    newDataset = []
    idx = 0
    while len(newDataset) < nums:
        if dataset[idx]["answers_spans"]["types"][0] == "number":
            newDataset.append(dataset[idx])
        idx += 1
    return newDataset

def main():
    dataset = load_dataset("drop", split="validation")
    numsDataset = get_nums_dataset(dataset)

    self_reflection(numsDataset)
    

if __name__ == '__main__':
    main()