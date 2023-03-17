import sys
import os
import openai

class OpenAICaller:
    """This class is responsible for interacting with the openai API
    """
    def __init__(self, model_name):
        self.model_name = model_name
        openai.api_key = os.getenv("OPENAI_API_KEY")

        ## check is openai api key is set and openai api is working
        try:
            models = openai.Model.list()
            print("Connection successful!")
            print("Available models:")
            # for model in models["data"]:
            #     print(f"Model: {model['id']}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def gen_request_to_api(self, messages, max_tokens=100, temperature=0.5, n=1, stop=None):
        response = openai.ChatCompletion.create(model=self.model_name, messages=messages, max_tokens=max_tokens, temperature=temperature)
        return response["choices"][0]["message"]["content"]