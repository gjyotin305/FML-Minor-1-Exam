from transformers import AutoProcessor, LlavaNextForConditionalGeneration, AutoModelForCausalLM, AutoTokenizer
from model.models import Experiment
from eval.utils import generate_wordcloud, calc_perplexity, run_inference
from PIL import Image
import urllib.request
from openai import OpenAI
from constants import (
    BIAS_PROMPTS, 
    BIAS_IMAGE_PROMPTS, 
    HISTORY_PROMPTS, 
    MEDICINE_PROMPTS, 
    TECH_PROMPTS
)
import json
import requests
import torch

model_hall = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct", 
    device_map="cuda", 
    torch_dtype=torch.float16, 
    trust_remote_code=True, 
)

model_hall = torch.compile(model_hall)

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

model = LlavaNextForConditionalGeneration.from_pretrained(
    "llava-hf/llava-v1.6-mistral-7b-hf", 
    torch_dtype=torch.float16, 
    device_map="auto"
)
model.to("cuda")
model = torch.compile(model=model)

processor = AutoProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")

exp1 = Experiment(
    model=model, 
    processor=processor,
    model_hall=model_hall, 
    token_hall=tokenizer
)

# result = exp1.run_experiment_text(BIAS_PROMPTS)

# for i, res in enumerate(result):
#     print(f"Starting WordCloud Generation {i}")
#     print(res["response"])
#     generate_wordcloud(text=res["response"], file_name=f"{i}")

# urls = [
#     "https://i.imgur.com/3QIgja2.jpeg",
#     "https://i.imgur.com/4TfBERc.jpeg",
#     "https://imgur.com/Re7Nli8.jpeg"
# ]

# for i, url in enumerate(urls):
#     urllib.request.urlretrieve(url=url, filename=f"im_{i}.png")

# images_pil = [Image.open(f"im_{i}.png") for i, url in enumerate(urls)]

# print(images_pil)

# result_ima = exp1.run_experiments_image(
#     prompts=BIAS_IMAGE_PROMPTS, 
#     images=images_pil
# )

# print(result_ima)

result = exp1.run_inference_text(MEDICINE_PROMPTS)

print(result)
