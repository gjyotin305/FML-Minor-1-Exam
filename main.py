from transformers import AutoProcessor, LlavaNextForConditionalGeneration
from model.models import Experiment
from eval.utils import generate_wordcloud
from PIL import Image
import urllib.request
from constants import BIAS_PROMPTS, BIAS_IMAGE_PROMPTS
import json
import requests
import torch

model = LlavaNextForConditionalGeneration.from_pretrained(
    "llava-hf/llava-v1.6-mistral-7b-hf", 
    torch_dtype=torch.float16, 
    device_map="auto"
)
model.to("cuda")
model = torch.compile(model=model)

processor = AutoProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")

exp1 = Experiment(model=model, processor=processor)

# result = exp1.run_experiment_text(BIAS_PROMPTS)

# for i, res in enumerate(result):
#     print(f"Starting WordCloud Generation {i}")
#     print(res["response"])
#     generate_wordcloud(text=res["response"], file_name=f"{i}")

urls = [
    "https://i.imgur.com/3QIgja2.jpeg",
    "https://i.imgur.com/4TfBERc.jpeg",
    "https://imgur.com/Re7Nli8.jpeg"
]

for i, url in enumerate(urls):
    urllib.request.urlretrieve(url=url, filename=f"im_{i}.png")

images_pil = [Image.open(f"im_{i}.png") for i, url in enumerate(urls)]

result_ima = exp1.run_experiments_image(BIAS_IMAGE_PROMPTS, images=images_pil)

print(result_ima)
# print(exp1.run_inference(BIAS_PROMPTS[4]))