import openai
import pandas as pd
import json
from tqdm import tqdm
from api import api_key
import nums_from_string as nfs

import re
def get_nums(text):
    try:
        # 提取所有整數或小數（負數也可）
        return re.findall(r'-?\d+\.?\d*', text)
    except Exception:
        return []
    
def smart_load(filepath, nrows=None):
    questions = []
    answers = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if nrows is not None and i >= nrows:
                break

            line = line.strip()
            if not line:
                continue

            tokens = line.split()
            if len(tokens) < 2:
                print(f"[!] 太短無法處理，第 {i+1} 行：{line}")
                questions.append(line)
                answers.append(None)
                continue

            # 把最後一個 token 當作答案來源，剩下的組成 question
            last_token = tokens[-1]
            question_part = ' '.join(tokens[:-1])

            # 從最後一段擷取出數字（可包含負數、小數）
            nums = re.findall(r'-?\d*\.?\d+', last_token)
            answer = nums[-1] if nums else None  # 如果找不到數字，就放 None

            questions.append(question_part)
            answers.append(answer)

    return pd.DataFrame({'question': questions, 'answer': answers})
#
openai.api_key = api_key
dirs = ['mgsm_zh']
#dirs = ['mgsm_gg_zh', 'mgsm_gg_bn', 'mgsm_gg_de', 'mgsm_gg_es', 'mgsm_gg_fr', 'mgsm_gg_ja', 'mgsm_gg_ru', 'mgsm_gg_sw', 'mgsm_gg_te', 'mgsm_gg_th']
language = ['Chinese', 'Bengali', 'German', 'Spanish', 'French', 'Japanese', 'Russian', 'Swahili', 'Telugu', 'Thai']
nums = 250
preprompt = "You are a middle school math teacher. Please explain the following problem in detail, including all the solution steps and verifications, and only keep numbers in the final output."
# prompt = "\n請在輸出的最後輸出答案，最後的輸出只能有數字"

def handle_dir(dir, language, dir_from):
    #df = pd.read_csv(f'./data/mgsm/{dir_from}.tsv', sep = '\t', nrows=nums, header=None, names=['question', 'answer'])
    df = smart_load(f'./data/mgsm/{dir_from}.tsv', nrows=nums)
    df.to_json(f'./data/mgsm/{dir_from}_{nums}.json', index=False, indent=2)
    with open(f'./data/mgsm/{dir_from}_{nums}.json', 'r') as f:
        data = json.load(f)
    #print(data)
    cnt = 0
    result = []
    for i in tqdm(range(nums)):
        '''text_for_translate = f'Please translate "{data['question'][str(i)]}" into {language} language.'
        response_for_translate = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": text_for_translate}],
            temperature=0.2
        )'''
        # text = response_for_translate["choices"][0]["message"]["content"] + prompt
        text = preprompt + data['question'][str(i)]# + prompt
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": text}],
            temperature=0.2
        )
        correct = True
        #print(str(data['answer'][str(i)]))
        try:
            correct = True if get_nums(str(data['answer'][str(i)]))[-1] == get_nums(response["choices"][0]["message"]["content"])[-1] else False
            if correct:
                cnt += 1
        except:
            #print("except")
            #print(response["choices"][0]["message"]["content"])
            correct = "True/False?"
        result.append({"index": i, 
                        # "output_translate": response_for_translate["choices"][0]["message"]["content"],
                        "output": response["choices"][0]["message"]["content"],
                        "answer": data['answer'][str(i)],
                        "question": text,
                        "correct": correct
                    })
    with open(f'./KomaLi/result/mgsm/gpt_{dir}_{nums}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f'{dir}：{cnt}/{nums}')
    return cnt



def main():
    result = []
    for i in range(len(dirs)):
        result.append(handle_dir(dirs[i], language[i], dirs[i]))
    print('-' * 30)
    for i in range(len(result)):
        print(f'{dirs[i]}：{result[i]}/{nums}')


if __name__ == '__main__':
    main()