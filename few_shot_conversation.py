from llm_connector import OpenAIChat
from joblib import delayed, Parallel
from tqdm import tqdm
from sts_prompts import get_sts_prompts, get_single_card_ask, get_multi_card_bundle_ask, AskType
import time
from utility import TextUtil
import pandas as pd

proceed_all = True

def get_cards(card_names, df):
    cards, indices = [], []
    for card_name in card_names:
        cards.append(None)
        indices.append(None)
        for index, row in df.iterrows():
            if row['Name'] == card_name:
                cards[-1] = row
                indices[-1] = index
        if cards[-1] is None:
            print(f"can't find card for {card_name}")
            return None, None
    return cards, indices

def process_response(chat, prompt, response, output_filename):
    if prompt == 'bundle':
        while True:
            print("Format is: card_name1, card_name2; card_name3, card_name4; <starting_number>")
            prompt = input()
            cards1, cards2, starting_number = prompt.split(';')
            starting_number = int(starting_number)
            cards1 = [card.strip() for card in cards1.split(',')]
            cards2 = [card.strip() for card in cards2.split(',')]
            print(f"Generating bundle prompt for {'/'.join(cards1)} x {'/'.join(cards2)}")
            df = pd.read_csv("IronClad Card Names.csv")
            cards_x, index_x = get_cards(cards1, df)
            cards_y, index_y = get_cards(cards2, df)
            if cards_x is None or cards_y is None:
                print("Enter again")
                continue
            prompt, _ =get_multi_card_bundle_ask(cards_x, cards_y, index_x, index_y, starting_number)
            break
    print(TextUtil.get_colored_text(prompt, TextUtil.TEXT_COLOR.Yellow))
    if response is not None:
        if not proceed_all:
            inp = input(f"Should we inject the response? [y/n]\n<{response[:10]} ... {response[-100:]}>")
        else:
            inp = 'y'
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
    inp = 'y' if prompt is not None else 'n'
    if not proceed_all:
        prompt = prompt if prompt is not None else "<no prompt available. ending the conversation>"
        print("Should we proceed with the prompt:")
        print(TextUtil.get_colored_text(prompt, TextUtil.TEXT_COLOR.Red))
        print("[y/n]")
        inp = input()
    return inp in ['y', 'yes', 'Y', 'Yes', 'YES']

if __name__=="__main__":
    # system_prompt, prompts, responses, _ = get_sts_prompts(ask_type=AskType.Negative_or_Positive)
    system_prompt, prompts, responses, _ = get_sts_prompts(ask_type=AskType.NP_Bundle)
    chat = OpenAIChat(OpenAIChat.OpenAIModel.GPT_4O, chat_format=True, system_message=system_prompt)
    output_filename = f"few_shot_converation_{chat.model_identifier}_{int(time.time())}"
    for index, (prompt, response) in enumerate(zip(prompts, responses)):
        process_response(chat, prompt, response, output_filename)
        while not should_we_proceed(prompts[index+1] if index+1<len(prompts) else None):
            inp = input("What should the prompt be?")
            process_response(chat, inp, None, output_filename)
        print("Proceeding")
    print("Done")
            
    
    