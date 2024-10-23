from llm_connector import OpenAIChat, QWENChat
from utility import TextUtil

if __name__=="__main__":
    chat = OpenAIChat(OpenAIChat.OpenAIModel.GPT_4O_mini)
    # chat = QWENChat(QWENChat.QWENModel.QWEN2_5__0_5B)
    while True:
        prompt = input()
        print(TextUtil.get_colored_text(chat.ask(prompt), TextUtil.TEXT_COLOR.Yellow))
