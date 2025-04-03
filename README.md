# culture_alignment
## data
### introduction
- MGSM
- MMMLU
- XCOPA

### Download
```bash
cd data
bash DOWNLOAD.sh
```

## MJLee
### introduction
- code for yielding output and do self reflection
- you **should** build a new dir for your code

### result
- put your output

### experiment.txt
- put your experiment result

### usage
```bash
pip install -r ./requirments.txt # suggestion: use python venv or conda
cd MJLee
touch api.py
echo "api_key = '{your openai api key}'" >> api.py
```

### reference
[openai api key](https://platform.openai.com/api-keys)
[openai api](https://platform.openai.com/docs/api-reference/introduction)

## SOP
1. MJLee is an example. You should build a new dir for your experiment
2. choose your model
3. yield output with different language for finding problem wrong in one language but correct in another(You could use different prompt at this step)
4. find all problem we need(Manual confirmation, or you can write a code)
5. do self reflection for those problem(you **should** use different prompt at this step)
6. record your experiment result