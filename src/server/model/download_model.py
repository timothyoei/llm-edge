from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from dotenv import load_dotenv
import torch
print(torch.__version__)
from unsloth import FastLanguageModel

def download_model(model_id, model_path, access_token):
  model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_id,
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
    access_token=access_token
  )

  tokenizer.save_pretrained(model_path)
  model.save_pretrained(model_path)

def test_model(query, model_path):
  tokenizer = AutoTokenizer.from_pretrained(model_path)
  model = AutoModelForCausalLM.from_pretrained(model_path)

  inputs = tokenizer.encode(query, return_tensors="pt")
  outputs = model.generate(inputs, num_return_sequences=1, repetition_penalty=1.1)
  return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
  load_dotenv()

  model_id = os.getenv("API_MODEL_ID")
  model_path = "src/server/model/bin"
  access_token = os.getenv("HF_TOKEN")
  download_model(model_id, model_path, access_token)

  # query = "What color is the sky?"
  # print(test_model(query, model_path))