#!/bin/bash

python3 ./main.py --run -m gpt4.1mini -d mathqa  -s onlyChinese --nums 3000
python3 ./main.py --run -m gpt4.1mini -d commenseqa -s onlyChinese --nums 6000
python3 ./main.py --run -m gpt4.1mini -d mmlu -s onlyChinese --nums 6000
python3 ./main.py --run -m gpt4.1mini -d truthfulqa -s onlyChinese --nums 6000

python3 ./main.py --run -m deepseek -d mathqa  -s onlyChinese --nums 3000
python3 ./main.py --run -m deepseek -d commenseqa -s onlyChinese --nums 6000
python3 ./main.py --run -m deepseek -d mmlu -s onlyChinese --nums 6000
python3 ./main.py --run -m deepseek -d truthfulqa -s onlyChinese --nums 6000

python3 ./main.py --run -m qwen -d mathqa  -s onlyChinese --nums 3000
python3 ./main.py --run -m qwen -d commenseqa -s onlyChinese --nums 6000
python3 ./main.py --run -m qwen -d mmlu -s onlyChinese --nums 6000
python3 ./main.py --run -m qwen -d truthfulqa -s onlyChinese --nums 6000