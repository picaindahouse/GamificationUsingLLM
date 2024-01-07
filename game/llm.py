# If running by default --> need to use Open AI API Key, thus withdrawing said key here
import os
from dotenv import load_dotenv
from openai import OpenAI
from settings import *

class LLM:
    def __init__(self, system):
        load_dotenv()
        key = os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key = key)
        self.system = system
        self.history = []

    def ask_chatgpt(self, new_question, max_tokens):
        ### Loading OpenAI ###

        messages = [
            {"role" : "system",
             "content" : self.system}
        ]

        for question, answer in self.history[-MAX_CONTEXT_QUESTIONS:]:
            messages.append({ "role": "user", "content": question })
            messages.append({ "role": "assistant", "content": answer })
        
        messages.append({ "role": "user", "content": new_question })

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature = 0.7, 
            max_tokens = max_tokens
        )


        new_answer = completion.choices[0].message.content
        self.history.append((new_question, new_answer))
        return new_answer
    
    '''
    def evaluate_answer(self, question, answer, max_tokens):
        system = """You are a game character speaking to a player. You have asked a question and gotten an answer in return. 
                    If the answer, answers your question reply with just 'TRUE'. 
                    However, if the answer does not properly answer the question then ask the question again but clarify what you mean."""
        

        user = "This is the question: " + question + " and this is the answer: " + answer

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role" : "system",
                 "content" :system},
                {"role" : "user",
                 "content" : user}
            ],
            temperature = 0.7, 
            max_tokens = max_tokens
        )

        return completion.choices[0].message.content
        '''



