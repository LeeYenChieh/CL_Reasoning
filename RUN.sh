#!/bin/bash

python3 ./main.py --run -m gpt4.1mini -d ${1} -s multiAgent --nums 500
python3 ./main.py --run -m gpt4omini -d ${1} -s multiAgent --nums 500
python3 ./main.py --run -m deepseek -d ${1} -s multiAgent --nums 500
python3 ./main.py --run -m gemini -d ${1} -s multiAgent --nums 500
python3 ./main.py --run -m qwen -d ${1} -s multiAgent --nums 500
