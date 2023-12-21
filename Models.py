from enum import Enum

class ModelType(str, Enum):
    LLAMA = "llama-7b"
    LLAMALORA = "llama-lora-7b"
    LORA = "lora-7b"
    VICUNA = "vicuna-7b"
    DAVINCI = "text-davinci-003"
    GPT3 = "gpt-3.5-turbo-0613"
    BASELINE = "copy-baseline"