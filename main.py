from transformers import AutoProcessor, LlavaNextForConditionalGeneration
from model.models import Experiment
from eval.utils import generate_wordcloud
from constants import BIAS_PROMPTS
import json
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

result = exp1.run_experiment_text(BIAS_PROMPTS)

for i, res in enumerate(result):
    print(f"Starting WordCloud Generation {i}")
    print(res["response"])
    generate_wordcloud(text=res["response"], file_name=f"{i}")


# print(exp1.run_inference(BIAS_PROMPTS[4]))