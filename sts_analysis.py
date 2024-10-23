from llm_connector import LLMConnector, OpenAIChat
from joblib import delayed, Parallel
from tqdm import tqdm
from sts_prompts import get_sts_prompts, get_single_card_ask, get_multi_card_multi_ask, get_multi_card_bundle_ask, AskType
from utility import TextUtil

thread_count = 50

class IncorrectResponseLengthException(Exception):
    def __init__(self, length, expected_length, response):
        super().__init__(f"Incorrecnt length of {length}, expected {expected_length}, for {response[:100] + ' ... ' + response[-100:]}")

def ask_until_format_is_right(chat, prompt, bundle_size:None|int=None):
    # mock answer
    # result = ('4\n---NEXT---\n' * (bundle_size-1) + '4\n') if bundle_size is not None else '4\n'
    result = chat.ask(prompt)
    for i in range(3):
        try:
            if bundle_size is not None:
                vals = [float(r.split()[-1] if len(r) > 0 else r) for r in result.split('---NEXT---')]
                if len(vals) != bundle_size:
                    raise IncorrectResponseLengthException(len(vals), bundle_size, result)
                    # raise IncorrectResponseLengthException()
            else:
                val = float(result.split()[-1])
            break
        except (ValueError, IncorrectResponseLengthException) as e:
            print(f"Unacceptable response for \"{prompt}\"")
            print(result)
            print(f"Exception: {e}")
            if i == 2:
                result = f'invalid response {i+1} times\n[latest] {result}\n1000000\n' * (1 if bundle_size is None else bundle_size)
                result += f'---NEXT---\n1000000\n' * (0 if bundle_size is None else (bundle_size - 1))
            else:
                # mock answer
                # result = ('4\n---NEXT---\n' * (bundle_size-1) + '4\n') if bundle_size is not None else '4\n'
                result = chat.ask(prompt)
    return result

def get_request_and_response(chat, card1, card2, id1, id2, starting_card_number):
        prompt, id = get_single_card_ask(card1, card2, id1, id2, starting_card_number)
        result = ask_until_format_is_right(chat, prompt)
        return prompt, result, id
    
def get_multi_request_and_response(chat: OpenAIChat, x_cards, y_cards, x_indices, y_indices, starting_card_number):
    prompts, ids = get_multi_card_multi_ask(x_cards, y_cards, x_indices, y_indices, starting_card_number)
    results = []
    chat = chat.copy()
    chat.chat_format = True
    for prompt in prompts:
        result = ask_until_format_is_right(chat, prompt)
        results.append(result)
    return prompts, results, ids

def get_bundle_request_and_response(chat: OpenAIChat, x_cards, y_cards, x_indices, y_indices, starting_card_number):
    prompt, ids = get_multi_card_bundle_ask(x_cards, y_cards, x_indices, y_indices, starting_card_number)
    # print(TextUtil.get_colored_text(f"{x_indices} x {y_indices}\n", TextUtil.TEXT_COLOR.Red))
    # print(TextUtil.get_colored_text(prompt, TextUtil.TEXT_COLOR.Yellow))
    results = ask_until_format_is_right(chat, prompt, len(x_cards) * len(y_cards)).split('---NEXT---')
    # print(TextUtil.get_colored_text('\n&\n'.join(results), TextUtil.TEXT_COLOR.Blue))
    return prompt, results, ids

def log(prompt, response, output_filename, tag=""):
    with open(f"{output_filename}.log", "a", encoding='utf-8') as f:
        f.write(prompt+'\n')
        f.write(tag + response)
        f.write('\n-------------------------------------------------------------\n')

def run_single_ask_job(chat, cards_df, next_card_number):
    queries = [(row1, row2, index1, index2) for index1, row1 in cards_df.iterrows() for index2, row2 in cards_df.iterrows()]
    req_responses = Parallel(n_jobs=thread_count)(delayed(get_request_and_response)(chat, queries[i][0], queries[i][1], queries[i][2], queries[i][3], next_card_number) for i in tqdm(range(len(queries))))
    assert isinstance(req_responses, list), "Parallel jobs have not resulted in an output of type list"
    assert None not in req_responses
    return req_responses

def run_multi_ask_job(chat, cards_df, card_count, next_card_number):
    parts = []
    for index, row in cards_df.iterrows():
        if len(parts) == 0 or len(parts[-1][0]) >= card_count:
            parts.append(([], []))
        parts[-1][0].append(index)
        parts[-1][1].append(row)
    queries = [(x_cards, y_cards, x, y) for x, x_cards in parts for y, y_cards in parts]
    req_responses = Parallel(n_jobs=thread_count)(delayed(get_multi_request_and_response)(chat, queries[i][0], queries[i][1], queries[i][2], queries[i][3], next_card_number) for i in tqdm(range(len(queries))))
    assert isinstance(req_responses, list), "Parallel jobs have not resulted in an output of type list"
    prompts, results, ids = [], [], []
    for chunk_ps, chunk_rs, chunk_is in req_responses: # type: ignore
        prompts += chunk_ps
        results += chunk_rs
        ids += chunk_is
    return zip(prompts, results, ids)

def run_bundle_ask_job(chat, cards_df, card_count, next_card_number):
    parts = []
    for index, row in cards_df.iterrows():
        if len(parts) == 0 or len(parts[-1][0]) >= card_count:
            parts.append(([], []))
        parts[-1][0].append(index)
        parts[-1][1].append(row)
    queries = [(x_cards, y_cards, x, y) for x, x_cards in parts for y, y_cards in parts]
    req_responses = Parallel(n_jobs=thread_count)(delayed(get_bundle_request_and_response)(chat, queries[i][0], queries[i][1], queries[i][2], queries[i][3], next_card_number) for i in tqdm(range(len(queries))))
    assert isinstance(req_responses, list), "Parallel jobs have not resulted in an output of type list"
    prompts, results, ids = [], [], []
    for chunk_p, chunk_rs, chunk_is in req_responses: # type: ignore
        prompts += [chunk_p] + ['[continued from last responses]'] * (len(chunk_rs) - 1)
        results += chunk_rs
        ids += chunk_is
    return zip(prompts, results, ids)

if __name__=="__main__":
    system_prompt, prompts, responses, next_card_number = get_sts_prompts(ask_type=AskType.NP_Bundle, shot_count=None)
    chat = OpenAIChat(OpenAIChat.OpenAIModel.GPT_4O_mini, chat_format=False, system_message=system_prompt)
    for prompt, response in zip(prompts, responses):
        chat.inject(prompt, response)
    import pandas as pd
    import numpy as np
    import time
    output_filename = f"synergy_results_{chat.model_identifier}_{int(time.time())}"
    df = pd.read_csv("IronClad Card Names.csv")
    # df = df[:3] # Test for first 3 cards only
    synergies = np.zeros((len(df), len(df)))
    for prompt, response in zip(prompts, responses):
        log(prompt, response, output_filename, "[injected]")

    # req_responses = run_single_ask_job(chat, df, next_card_number)
    req_responses = run_bundle_ask_job(chat, df, 6, next_card_number) # AskType.NP_Multi_Card only!
    for prompt, result, id in req_responses: # type: ignore
        index1, index2 = id
        log(prompt, result, output_filename)
        synergies[index1, index2] = float(result.split()[-1])
    pd.DataFrame(synergies).to_csv(f"{output_filename}.csv")