from __future__ import annotations

import openai
#import transformers
import time
from enum import StrEnum
import copy

class RateLimitException(Exception):
    pass

class LLMConnector:
    last_call_timestamp: dict[str, float] = {}
    tokens_used_this_minute: dict[str, int] = {}
    def __init__(self, model_identifier: str):
        self.model_identifier = model_identifier
    
    def _get_token_limit_per_minute(self) -> int:
        raise Exception("not implemented yet")
    
    def _get_response(self, request) -> tuple[int, str]:
        raise Exception("not implemented yet")
    
    def _prompt_to_request(self, prompt: str) -> object:
        raise Exception("not implemented yet")
    
    def inject(self, request_text: str, response_text: str) -> None:
        raise Exception("not implemented yet")
    
    def copy(self) -> LLMConnector:
        raise Exception("not implemented yet")

    def ask(self, prompt: str) -> str:
        request = self._prompt_to_request(prompt)
        current = time.time()
        prev = LLMConnector.last_call_timestamp.get(self.model_identifier, None)
        tokens_used = LLMConnector.tokens_used_this_minute.get(self.model_identifier, None)
        est_token_count = len(prompt)//4
        limit = self._get_token_limit_per_minute()
        eps_seconds = 1
        if prev is not None and tokens_used is not None and tokens_used + est_token_count > limit:
            time.sleep(60 - min(current - prev, 60) + eps_seconds)
            LLMConnector.tokens_used_this_minute[self.model_identifier] = 0
        try:
            tokens_used, response = self._get_response(request)
        except RateLimitException as e:
            print('rate limit exception received. forced sleep.')
            time.sleep(60 - min((current - prev) if prev is not None else 0, 60) + eps_seconds)
            # if we receive this exception a second time, we delegate handling to the upper layer
            tokens_used, response = self._get_response(request)
        current = time.time()
        LLMConnector.tokens_used_this_minute[self.model_identifier] = \
            LLMConnector.tokens_used_this_minute.get(self.model_identifier, 0) + tokens_used
        LLMConnector.last_call_timestamp[self.model_identifier] = current
        return response
    
class OpenAIChat(LLMConnector):
    class OpenAIModel(StrEnum):
        GPT_4 = "gpt-4"
        GPT_Turbo_4 = "gpt-4-turbo-2024-04-09" # gpt-4-turbo for latest
        GPT_Turbo_35 = "gpt-3.5-turbo"
        GPT_4O = "gpt-4o"
        GPT_4O_mini = "gpt-4o-mini"
    
    TOKEN_LIMITS = { #https://platform.openai.com/account/limits
        OpenAIModel.GPT_4: 300000,
        OpenAIModel.GPT_Turbo_4: 800000,
        OpenAIModel.GPT_Turbo_35: 10000000,
        OpenAIModel.GPT_4O: 2000000,
        OpenAIModel.GPT_4O_mini: 10000000,
    }
    CLIENT = None

    def get_client(self):
        if OpenAIChat.CLIENT is None:
            from auth import OpenAI_AUTH
            OpenAIChat.CLIENT = openai.OpenAI(api_key=OpenAI_AUTH)
        return OpenAIChat.CLIENT
    
    def __init__(self, openAI_model: OpenAIModel, system_message: str|None=None, chat_format=True):
        if openAI_model == OpenAIChat.OpenAIModel.GPT_4O:
            input("[Warning] Using the more expensive GPT 4O model [press Enter to continue]")
        self.openAI_model = openAI_model
        self.chat_format = chat_format
        self.chat_log = [] if system_message is None else [{"role": "system", "content": system_message}]
        super().__init__(str(self.openAI_model))
    
    def copy(self) -> OpenAIChat:
        ret = OpenAIChat(self.openAI_model, None, self.chat_format)
        ret.chat_log = copy.deepcopy(self.chat_log)
        return ret
    
    def _get_token_limit_per_minute(self) -> int:
        return OpenAIChat.TOKEN_LIMITS[self.openAI_model] #TODO share between parallel instances
    
    def _get_response(self, request) -> tuple[int, str]:
        try:
            response = self.get_client().chat.completions.create(**request)
        except Exception as e:
            print(f"OpenAI Exception:\n{e}")
            raise e
        tokens_used = int(response.usage.total_tokens)
        response_text = response.choices[0].message.content
        if self.chat_format:
            self.chat_log = request['messages'] + [{'role': 'assistant', 'content': response_text}]
        return tokens_used, response_text
    
    def inject(self, request_text: str, response_text: str):
        # assert self.chat_format, "you can only inject request and responses in a chat format conversation."
        self.chat_log.append({"role": "user", "content": request_text})
        self.chat_log.append({"role": "assistant", "content": response_text})
    
    def _prompt_to_request(self, prompt: str) -> dict:
        # https://platform.openai.com/docs/guides/chat-completions/overview
        return {
                'model': self.openAI_model,
                'messages': self.chat_log + [{"role": "user", "content": prompt}],
            }

    def prompt_as_API_request(self, prompt: str, request_id: str):
        request = self._prompt_to_request(prompt)
        return {
            "custom_id": request_id,
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": request,
        }
    
    def as_fine_tuning_example(self):
        messages: list[dict] = copy.deepcopy(self.chat_log)
        for message in messages:
            if message["role"] == "assistant":
                message["weight"] = 0
        assert messages[-1]["role"] == "assistant", "fine-tuning log ends with user message"
        messages[-1]["weight"] = 1
        request = {'messages': messages}
        return request
    

# class QWENChat(LLMConnector):
#     class QWENModel(StrEnum):
#         QWEN2_5__0_5B = "Qwen/Qwen2.5-0.5B" # ~1GB
#        QWEN2_5__1_5B = "Qwen/Qwen2.5-1.5B" # ~3GB
#        QWEN2_5__3B = "Qwen/Qwen2.5-3B" # ~?GB
#        QWEN2_5__7B = "Qwen/Qwen2.5-7B" # ~16GB
#        # list of QWEN2.5 models: https://huggingface.co/collections/Qwen/qwen25-66e81a666513e518adb90d9e
#        # list of QWEN2 models: https://huggingface.co/collections/Qwen/qwen2-6659360b33528ced941e557f
##    MODELS: dict[QWENModel, transformers.Qwen2PreTrainedModel] = {}
#    TOKENIZERS: dict[QWENModel, transformers.PreTrainedTokenizerBase] = {}

#    def get_tokenizer(self):
#        if self.qwen_model not in QWENChat.TOKENIZERS:
#            QWENChat.TOKENIZERS[self.qwen_model] = transformers.AutoTokenizer.from_pretrained(self.qwen_model)
#        return QWENChat.TOKENIZERS[self.qwen_model]
#    
#    def get_model(self):
#        if self.qwen_model not in QWENChat.MODELS:
#            QWENChat.MODELS[self.qwen_model] = transformers.AutoModelForCausalLM.from_pretrained(
#                self.qwen_model,
#                torch_dtype="auto",
#                device_map="auto"
#            )
#        return QWENChat.MODELS[self.qwen_model]
#    
#    def __init__(self, qwen_model: QWENModel, system_message: str|None=None, chat_format=True):
#        self.qwen_model = qwen_model
#        self.chat_format = chat_format
#        self.chat_log = [] if system_message is None else [{"role": "system", "content": system_message}]
#        super().__init__(str(self.qwen_model))
#    
#    def _get_response(self, request) -> tuple[int, str]:
#        text = self.get_tokenizer().apply_chat_template(**request)
#        model_inputs = self.get_tokenizer()([text], return_tensors="pt").to(self.get_model().device) # type: ignore
#        generated_ids = self.get_model().generate(
#            **model_inputs, # type: ignore
#            max_new_tokens=512,
#        )
#        generated_ids = [
#            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
#        ]
#        response = self.get_tokenizer().batch_decode(generated_ids, skip_special_tokens=True)[0]
#        if self.chat_format:
#            self.chat_log = request['conversation'] + [{'role': 'assistant', 'content': response}]
#        return 0, response
#    
#    def inject(self, request_text: str, response_text: str):
#        # assert self.chat_format, "you can only inject request and responses in a chat format conversation."
#        self.chat_log.append({"role": "user", "content": request_text})
#        self.chat_log.append({"role": "assistant", "content": response_text})
#    
#    def _prompt_to_request(self, prompt: str) -> object:
#        # https://platform.openai.com/docs/guides/chat-completions/overview
#        return {
#                'tokenize': False,
#                'add_generation_prompt': True,
#                'conversation': self.chat_log + [{"role": "user", "content": prompt}],
#            }
#    
#    def _get_token_limit_per_minute(self) -> int:
#        # TODO find a better solution
#        return 10_000_000 # some big number, since this is local