import openai
import pandas as pd
import json
from tqdm import tqdm
from api import api_key
import nums_from_string as nfs
import logging

openai.api_key = api_key
dirs = ['mgsm_zh', 'mgsm_bn', 'mgsm_de', 'mgsm_es', 'mgsm_fr', 'mgsm_ja', 'mgsm_ru', 'mgsm_sw', 'mgsm_te', 'mgsm_th']
language = ['Chinese', 'Bengali', 'German', 'Spanish', 'French', 'Japanese', 'Russian', 'Swahili', 'Telugu', 'Thai']
nums = 250
prompt = "\nOutput the final answer at the last of your response. " \
        "If the answer is a number, please output the number only. Arabic numerals only." \
prompt_to_output_arabic_number = "(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)"

logging.basicConfig(
    filename='result/mgsm_translation_eval.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def handle_dir(dir, language, dir_from):
    df = pd.read_csv(f'../data/mgsm/{dir_from}.tsv', sep = '\t', nrows=nums, names=['question', 'answer'])
    df.to_json(f'../data/mgsm/{dir_from}_{nums}.json', index=False, indent=2)
    with open(f'../data/mgsm/{dir_from}_{nums}.json', 'r') as f:
        data = json.load(f)
    
    cnt = 0
    result = []
    for i in tqdm(range(nums)):
        text_for_translate = f'Please translate "{data['question'][str(i)]}" + and "{prompt}" into {language}. After translation, you should concat the two sentences together.' \
            f'Please make sure the translation is accurate and fluent. It should have the same meaning with the original sentence.' \
            f'You should be very careful about the grammar. Check the translated sentence again after you finish the translation. DO NOT MAKE ANY MISTAKE!' \
            f'Please do not output any other content. ' \
            f'Please do not output the answer. ' \

        response_for_translate = openai.ChatCompletion.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": text_for_translate}],
        )
        text = response_for_translate["choices"][0]["message"]["content"] + prompt_to_output_arabic_number
        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": text}],
        )
        correct = True
        try:
            correct = True if nfs.get_nums(str(data['answer'][str(i)]))[-1] == nfs.get_nums(response["choices"][0]["message"]["content"])[-1] else False
            if correct:
                cnt += 1
        except:
            logging.error(f"Failed to extract number from response: {response['choices'][0]['message']['content']}")
            correct = "True/False?"
        result.append({"index": i, 
                        "output_translate": response_for_translate["choices"][0]["message"]["content"],
                        "output": response["choices"][0]["message"]["content"],
                        "answer": data['answer'][str(i)],
                        "question": text,
                        "correct": correct
                    })
    with open(f'../HowardLiu/result/mgsm/gpt_{dir}_{nums}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    logging.info(f'{dir}：{cnt}/{nums}')
    return cnt



def main():
    result = []
    for i in range(len(dirs)):
        result.append(handle_dir(dirs[i], language[i], "mgsm_en"))
    logging.info('-' * 30)
    for i in range(len(result)):
        logging.info(f'{dir}：{result[i]}/{nums}')


if __name__ == '__main__':
    main()