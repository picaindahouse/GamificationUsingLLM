# If running by default --> need to use Open AI API Key, thus withdrawing said key here
import os
from dotenv import load_dotenv
from openai import OpenAI
from settings import *
from llama_cpp import Llama
from transformers import AutoTokenizer

class LLM:
    def __init__(self, system, local=False, local_model="tinyopenorca"):
        self.local = local
        if self.local:
            self.client = None
        else:
            load_dotenv()
            key = os.environ.get("OPENAI_API_KEY")
            self.client = OpenAI(api_key = key)
        self.system = system
        self.history = []

        # Choose from "tinyv1", "tinyopenorca", 
        # "mistral3", "mistral4", "mistral5", 
        # "llama2-3", "llama2-4", "llama2-5",
        # "phi2"
        self.local_model = local_model
        self.message = ''
        

    def change_system(self, new_system):
        self.system = new_system

    def ask_local(self, new_question, messages, max_tokens, temperature):
        path = local_models[self.local_model][0]
        stop_params = local_models[self.local_model][2]
        if self.local_model == "phi2":
            prompt = ""
            for message in messages:
                prompt += message['role'].capitalize() + ': ' + message['content'] + '\n'
            prompt += 'Assistant:'
        else:
            checkpoint = local_models[self.local_model][1]
            tokenizer = AutoTokenizer.from_pretrained(checkpoint)
            tokenized_chat = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
            prompt = tokenizer.decode(tokenized_chat[0])
        #print(prompt)
        self.message = prompt

        llm = Llama(model_path = path,
                    n_gpu_layers = 0,
                    n_ctx=2048) # No GPU
        
        new_answer = llm(prompt,
                         stop=stop_params,
                         max_tokens=max_tokens,
                         temperature=temperature)["choices"][0]["text"]
        
        self.history.append((new_question, new_answer))
        return new_answer

    def ask_chatgpt(self, new_question, max_tokens, temperature = 0.7):
        if self.local and 'mistral' in self.local_model:
            messages = [
                {"role": "user",
                 "content": "These are your instructions for this conversation: {" + self.system + \
                    "}. Now you will begin speaking to the player.",},
                {"role": "assistant",
                 "content": "Understood I will follow the instructions and speak as though I am speaking to a player playing the game from now on."
                }
            ]
        else: 
            messages = [
                {"role" : "system",
                "content" : self.system}
            ]

        for question, answer in self.history[-MAX_CONTEXT_QUESTIONS:]:
            messages.append({ "role": "user", "content": question })
            messages.append({ "role": "assistant", "content": answer })
        
        messages.append({ "role": "user", "content": new_question })
        
        if self.local:
            ### Loading Local Model ###
            return self.ask_local(new_question, messages, max_tokens, temperature)
        
        self.message = messages
        ### Loading OpenAI ###
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature = 0.7, 
            max_tokens = max_tokens
        )


        new_answer = completion.choices[0].message.content
        self.history.append((new_question, new_answer))
        return new_answer
