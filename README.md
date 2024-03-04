# GamificationUsingLLM
Final Year Project

### To Run the Game using ChatGPT  
- Create an Open AI Account and get an API Key.
- In the game folder, create a .env file with OPENAI_API_KEY=[your_key]
- Get the ModelDeploymentImages folder from me and place this folder in the game folder.
- Navigate to game/llm.py
- In the __init__ function, for the LLM class, for the input parameters, ensure that local=False.
- In cmd/terminal cd to the game folder and run py main.py

### To Run the Game using Local Models
- Install the local model you wish to use from Hugging Face.
- For example can install Mistral 7b instruct model here: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF.
- Get the ModelDeploymentImages folder from me and place this folder in the game folder.
- Navigate to game/settings.py and find local_models
- Add your model to the local_models dictionary. Should be in the following format: 
- 'model_name': ['model_location', 'model_chat_template', ['A list of stopping parameters']]
- Save and then navigate to game/llm.py
- In the __init__ function, for the LLM class, for the input parameters, set the default values for local to True (Local=True) and local_model to the model_name you gave in step 5 (local_model='model_name').
- Save.
- In cmd/terminal cd to the game folder and run py main.py

### Credit
- The art assets and the soundtrack have been done by Pixel-boy and AAA and can be found here: https://pixel-boy.itch.io/ninja-adventure-asset-pack
- The game was built on top of the game built in a pygame tutorial done by Clear Code that can be found here: https://www.youtube.com/watch?v=QU1pPzEGrqw&t=2s


