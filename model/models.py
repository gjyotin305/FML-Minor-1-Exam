from transformers import (
    LlavaNextProcessor, 
    LlavaNextForConditionalGeneration, 
    AutoProcessor,
    AutoModelForCausalLM,
    AutoTokenizer
)
import torch
import json
from typing import List, Dict
from PIL import Image
from eval.utils import run_inference, calc_perplexity
from openai import OpenAI
import requests


class Experiment(object):
    def __init__(
        self,
        model: LlavaNextForConditionalGeneration = None,
        model_hall: AutoModelForCausalLM = None,
        token_hall:AutoTokenizer = None,
        processor: AutoProcessor = None
    ) -> None:
        self.model = model
        self.model_hall = model_hall
        self.processor = processor
        self.token_hall = token_hall

    def run_inference_text(
        self, 
        prompts: List[Dict[str, str]],
        filename: str
    ) -> List[Dict[str, str]]:
        pp_prompts = [x["prompt"] for x in prompts]
        responses = [run_inference(self.model_hall, self.token_hall, prompts=prompt) for prompt in pp_prompts]

        perplexity_score = calc_perplexity(generated_responses=pp_prompts)

        logs_hall = [{"prompt": prompt, "response": response, "ppl_score": ppl} for prompt, response, ppl in zip(pp_prompts, responses, perplexity_score["perplexities"])]

        with open(f"logs_hall_{filename}.json", "w") as final:
            json.dump(logs_hall, final)
            final.close()
        
        return logs_hall

    def run_experiment_text(self, prompts: List[str]) -> List[Dict[str, str]]:
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
            conversation_prompt = self.processor.apply_chat_template(conversation, add_generation_prompt=True)
            prompts_test.append(conversation_prompt)

        inputs = self.processor(
            text=prompts_test, padding=True, return_tensors="pt").to("cuda:0")
        generate_ids = self.model.generate(**inputs, max_new_tokens=700)
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
    
    def run_experiments_image(self, images, prompts: str):
        prompts_test = []

        for x in prompts:
            conversation = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image"},
                        {"type": "text", "text": f"{x}"},
                    ],
                },
            ]
            conversation_prompt = self.processor.apply_chat_template(conversation, add_generation_prompt=True)
            prompts_test.append(conversation_prompt)

        inputs = self.processor(
            text=prompts_test, images=images, padding=True, return_tensors="pt").to("cuda:0")
        generate_ids = self.model.generate(**inputs, max_new_tokens=700)
        result = self.processor.batch_decode(
            generate_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )

        logs_prompt = [{"prompt": x, "response": y} for x, y in zip(prompts, result)]

        with open("logs_images_1.json", "w") as final:
            json.dump(logs_prompt, final)

        return logs_prompt

    def run_inference(self, prompt: str):
        process_prompt = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{prompt}"},
                ],
            },
        ]
        prompt = self.processor.apply_chat_template(process_prompt, add_generation_prompt=True)

        inputs = self.processor(
            text=prompt, padding=True, return_tensors="pt").to("cuda:0")
        generate_ids = self.model.generate(**inputs, max_new_tokens=700)
        result = self.processor.decode(
            generate_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )
        return result


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
