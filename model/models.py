from transformers import (
    LlavaNextProcessor, 
    LlavaNextForConditionalGeneration, 
    AutoProcessor
)
import torch
import json
from typing import List, Dict
from PIL import Image
import requests


class Experiment(object):
    def __init__(
        self,
        model: LlavaNextForConditionalGeneration,
        processor: AutoProcessor
    ) -> None:
        self.model = model
        self.processor = processor

    def run_experiment(self, prompts: List[str]) -> List[Dict[str, str]]:
        prompts_test = []

        for x in prompts:
            conversation = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{x}"},
                    ],
                },
            ]
            prompts_test.append(conversation)

        inputs = self.processor(
            text=prompts, padding=True, return_tensors="pt").to("cuda:0")
        generate_ids = self.model.generate(**inputs, max_new_tokens=300)
        result = self.processor.batch_decode(
            generate_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )

        logs_prompt = [{"prompt": x, "response": y} for x, y in zip(prompts, result)]

        with open("logs.json", "w") as final:
            json.dump(logs_prompt, final)
            final.close()

        return logs_prompt


# processor = LlavaNextProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")

# model = LlavaNextForConditionalGeneration.from_pretrained(
#     "llava-hf/llava-v1.6-mistral-7b-hf",
#     torch_dtype=torch.float16,
#     low_cpu_mem_usage=True
# )
# model.to("cuda:0")
# model = torch.compile(model)


# conversation = [
#     {
#         "role": "user",
#         "content": [
#             {"type": "text", "text": "What is shown in this image?"},
#         ],
#     },
# ]
# prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
# inputs = processor(prompt, image, return_tensors="pt").to("cuda:0")

# # autoregressively complete prompt
# output = model.generate(**inputs, max_new_tokens=100)

# print(processor.decode(output[0], skip_special_tokens=True))
