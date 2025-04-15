import openai
from api import api_key

openai.api_key = api_key

# List all available models
models = openai.Model.list()

# Print model IDs
for model in models['data']:
    print(model['id'])
