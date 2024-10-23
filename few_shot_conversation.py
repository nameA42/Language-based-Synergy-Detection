from llm_connector import OpenAIChat
from joblib import delayed, Parallel
from tqdm import tqdm
from sts_prompts import get_sts_prompts, get_single_card_ask, AskType
import time

YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def process_response(chat, prompt, response, output_filename):
    print(f"{YELLOW}{prompt}{RESET}")
    if response is not None:
        inp = input(f"Should we inject the response? [y/n]\n<{response[:10]} ... {response[-100:]}>")
        if inp in ['y', 'yes', 'Y', 'Yes', 'YES']:
            chat.inject(prompt, response)
        else:
            print("asking for new response ...")
            response = chat.ask(prompt)
    else:
        print("asking for new response ...")
        response = chat.ask(prompt)
    with open(f"{output_filename}.log", "a", encoding='utf-8') as f:
        f.write(prompt)
        f.write(response)
        f.write('\n-------------------------------------------------------------\n')
    print(response)

def should_we_proceed(prompt):
    print("Should we proceed with the prompt:")
    print(f"{RED}{prompt}{RESET}")
    print("[y/n]")
    inp = input()
    return inp in ['y', 'yes', 'Y', 'Yes', 'YES']

if __name__=="__main__":
    system_prompt, prompts, responses, _ = get_sts_prompts(ask_type=AskType.Negative_or_Positive)
    chat = OpenAIChat(OpenAIChat.OpenAIModel.GPT_4O, chat_format=True, system_message=system_prompt)
    output_filename = f"few_shot_converation_{chat.model_identifier}_{int(time.time())}"
    for index, (prompt, response) in enumerate(zip(prompts, responses)):
        process_response(chat, prompt, response, output_filename)
        while not should_we_proceed(prompts[index+1] if index+1<len(prompts) else "<no prompt available. ending the conversation>"):
            inp = input("What should the prompt be?")
            process_response(chat, inp, None, output_filename)
        print("Proceeding")
    print("Done")
            
    
    