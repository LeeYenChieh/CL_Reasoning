import openai
import pandas as pd
import json
from tqdm import tqdm
from api import api_key

openai.api_key = api_key
dirs = ['mgsm_en', 'mgsm_zh', 'mgsm_th']
nums = 1


def handle_dir(dir):
    df = pd.read_csv(f'./data/mgsm/{dir}.tsv', sep = '\t', nrows=nums, names=['question', 'answer'])
    df.to_json(f'./data/mgsm/{dir}_{nums}.json', index=False, indent=2)
    with open(f'./data/mgsm/{dir}_{nums}.json', 'r') as f:
        data = json.load(f)
    
    result = []
    for i in tqdm(range(nums)):
        text = data['question'][str(i)]
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": text}],
        )
        result.append({"index": i, 
                        "output": response["choices"][0]["message"]["content"],
                        "answer": data['answer'][str(i)],
                        "question": text
                    })
    if dir == 'mgsm_en':
        with open(f'./result/mgsm/{dir}_{nums}.json', 'w') as f:
            json.dump(result, f, indent=2)
    else:
        with open(f'./result/mgsm/{dir}_{nums}.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)



def main():
    for dir in dirs:
        handle_dir(dir)


if __name__ == '__main__':
    main()