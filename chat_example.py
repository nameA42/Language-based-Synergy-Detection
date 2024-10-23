from llm_connector import OpenAIChat, QWENChat

if __name__=="__main__":
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    # chat = OpenAIChat(OpenAIChat.OpenAIModel.GPT_4O_mini)
    chat = QWENChat(QWENChat.QWENModel.QWEN2_5__0_5B)
    while True:
        prompt = input()
        print(f"{YELLOW}{prompt}{RESET}")
        print(chat.ask(prompt))
