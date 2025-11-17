#!/bin/bash

python3 ./main.py --run -m gpt4.1mini -d mathqa  -s onlyEnglish --nums 3000
python3 ./main.py --run -m gpt4.1mini -d commenseqa -s onlyEnglish --nums 6000
python3 ./main.py --run -m gpt4.1mini -d mmlu -s onlyEnglish --nums 6000
python3 ./main.py --run -m gpt4.1mini -d truthfulqa -s onlyEnglish --nums 6000

python3 ./main.py --run -m deepseek -d mathqa  -s onlyEnglish --nums 3000
python3 ./main.py --run -m deepseek -d commenseqa -s onlyEnglish --nums 6000
python3 ./main.py --run -m deepseek -d mmlu -s onlyEnglish --nums 6000
python3 ./main.py --run -m deepseek -d truthfulqa -s onlyEnglish --nums 6000

python3 ./main.py --run -m qwen mathqa  -s onlyEnglish --nums 3000
python3 ./main.py --run -m qwen commenseqa -s onlyEnglish --nums 6000
python3 ./main.py --run -m qwen mmlu -s onlyEnglish --nums 6000
python3 ./main.py --run -m qwen truthfulqa -s onlyEnglish --nums 6000