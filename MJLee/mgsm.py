import openai
import pandas as pd
import json
from tqdm import tqdm
from api import api_key
import nums_from_string as nfs

openai.api_key = api_key
dirs = ['mgsm_zh', 'mgsm_bn', 'mgsm_de', 'mgsm_es', 'mgsm_fr', 'mgsm_ja', 'mgsm_ru', 'mgsm_sw', 'mgsm_te', 'mgsm_th']
language = ['Chinese', 'Bengali', 'German', 'Spanish', 'French', 'Japanese', 'Russian', 'Swahili', 'Telugu', 'Thai']
nums = 250
lines = '\n' * 3
prompt = "\n請在輸出的最後輸出答案，最後的輸出只能有數字，數字必須為阿拉伯數字的格式" + lines

def translate_with_MGSM(dir, language, dir_from):
    df = pd.read_csv(f'./data/mgsm/{dir_from}.tsv', sep = '\t', nrows=nums, names=['question', 'answer'])
    df.to_json(f'./data/mgsm/{dir_from}_{nums}.json', index=False, indent=2)
    with open(f'./data/mgsm/{dir_from}_{nums}.json', 'r') as f:
        data_from = json.load(f)
    df = pd.read_csv(f'./data/mgsm/{dir}.tsv', sep = '\t', nrows=nums, names=['question', 'answer'])
    df.to_json(f'./data/mgsm/{dir}_{nums}.json', index=False, indent=2)
    with open(f'./data/mgsm/{dir}_{nums}.json', 'r') as f:
        data = json.load(f)
    
    cnt = 0
    result = []
    for i in tqdm(range(nums)):
        text_for_translate = f'There is a problem: \n"{lines + data_from["question"][str(i)] + prompt}".\n\n After translating it into {language}, the result is "{lines + data["question"][str(i)] + prompt}". Please check if this translation is correct and provide a version without any errors'
        response_for_translate = openai.ChatCompletion.create(
            model="gpt-4o-2024-08-06",
            messages=[{"role": "user", "content": text_for_translate}],
            temperature=0.2
        )
        text = ''.join(response_for_translate["choices"][0]["message"]["content"].split('\n')[1:-1]) + prompt
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": text}],
            temperature=0.2
        )
        correct = True
        try:
            correct = True if nfs.get_nums(str(data['answer'][str(i)]))[-1] == nfs.get_nums(response["choices"][0]["message"]["content"])[-1] else False
            if correct:
                cnt += 1
        except:
            print(response["choices"][0]["message"]["content"])
            correct = "True/False?"
        result.append({"index": i,
                        "data_from": data_from["question"][str(i)],
                        "output_translate": text,
                        "output": response["choices"][0]["message"]["content"],
                        "answer": data['answer'][str(i)],
                        "question": text,
                        "correct": correct
                    })
    with open(f'./MJLee/result/mgsm/gpt4o_{dir}_{nums}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f'{dir}：{cnt}/{nums}')
    return cnt

def main():
    result = []
    for i in range(len(dirs)):
        result.append(translate_with_MGSM(dirs[i], language[i], "mgsm_en"))
    print('-' * 30)
    for i in range(len(result)):
        print(f'{dirs[i]}：{result[i]}/{nums}')


if __name__ == '__main__':
    main()