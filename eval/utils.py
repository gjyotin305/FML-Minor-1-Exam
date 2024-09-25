from wordcloud import WordCloud
from evaluate import load
from typing import List, Dict
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import matplotlib.pyplot as plt 

def generate_wordcloud(text: str, file_name: str):
    wc = WordCloud(background_color="white", colormap='Oranges', width=300, height=300).generate(text)
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(f"word_cloud_{file_name}.png")

def calc_perplexity(generated_responses: List[str]) -> Dict[str, int]:
    torch.cuda.empty_cache()
    perplexity = load("perplexity", module_type="metric")
    results = perplexity.compute(
        model_id="microsoft/Phi-3-mini-4k-instruct", 
        predictions=generated_responses,
        batch_size=1
    )
    return results

def run_inference(
    model: AutoModelForCausalLM, 
    tokenizer: AutoTokenizer, 
    prompts: str
) -> str:
    messages = [
        {"role": "system", "content": "Your are to answer all questions faithfully."},
        {"role": "user", "content": f"{prompts}"},
    ]

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )

    generation_args = {
        "max_new_tokens": 600,
        "return_full_text": False,
        "temperature": 0.3,
        "do_sample": True,
    }

    output = pipe(messages, **generation_args)
    print(output[0]['generated_text'])
    return str(output[0]['generated_text'])

