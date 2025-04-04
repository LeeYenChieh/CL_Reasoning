import openai
import pandas as pd
import json
from tqdm import tqdm
from api import api_key
import nums_from_string as nfs

openai.api_key = api_key
dirs = ['mgsm_bn', 'mgsm_de', 'mgsm_es', 'mgsm_fr', 'mgsm_ja', 'mgsm_ru', 'mgsm_sw', 'mgsm_te', 'mgsm_th']
nums = 250
prompt = "\n請在輸出的最後輸出答案，最後的輸出只能有數字"

def handle_dir(dir):
    df = pd.read_csv(f'./data/mgsm/{dir}.tsv', sep = '\t', nrows=nums, names=['question', 'answer'])
    df.to_json(f'./data/mgsm/{dir}_{nums}.json', index=False, indent=2)
    with open(f'./data/mgsm/{dir}_{nums}.json', 'r') as f:
        data = json.load(f)
    
    cnt = 0
    result = []
    for i in tqdm(range(nums)):
        text = data['question'][str(i)] + prompt
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": text}],
            temperature=0.2
        )
        correct = True if nfs.get_nums(str(data['answer'][str(i)]))[-1] == nfs.get_nums(response["choices"][0]["message"]["content"])[-1] else False
        if correct:
            cnt += 1
        result.append({"index": i, 
                        "output": response["choices"][0]["message"]["content"],
                        "answer": data['answer'][str(i)],
                        "question": text,
                        "correct": correct
                    })
    with open(f'./MJLee/result/mgsm/{dir}_{nums}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return cnt



def main():
    result = []
    for dir in dirs:
        result.append(handle_dir(dir))
    for i in range(len(result)):
        print(f'{dirs[i]}：{result[i]}/{nums}')


if __name__ == '__main__':
    main()