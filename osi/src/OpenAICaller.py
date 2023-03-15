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

    def truncate_message(self, message, max_tokens):
        """Truncate a message to a maximum number of tokens.
        We use a rule of thumb that 1 token is about 4 symbols (https://platform.openai.com/tokenizer)

        Args:
            message (str):
            max_tokens (int): 

        Returns:
            str: truncated message
        """
        
        # count words
        symbol_count = len(message)

        if symbol_count <= max_tokens*4:
            return message

        new_len = int(max_tokens*4)
        print(f"Truncating message from {symbol_count} to {new_len} symbols")
        return message[:new_len]
    
    def gen_request_to_api(self, prompt, max_tokens=100, temperature=0.5, n=1, stop=None):
        prompt = self.truncate_message(prompt, 4000-max_tokens)
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(model=self.model_name, messages=messages, max_tokens=max_tokens, temperature=temperature)
        return response["choices"][0]["message"]["content"]