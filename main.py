from transformers import AutoProcessor, LlavaNextForConditionalGeneration
from model.models import Experiment
from constants import BIAS_PROMPTS
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

result = exp1.run_experiment(BIAS_PROMPTS)

print(result)