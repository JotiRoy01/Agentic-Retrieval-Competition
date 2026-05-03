from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from agentic.data_loader.data_loader import load
from agentic.exception import Agentic_Exception
import sys

class QueryExpansion :
    def __init__(self) :
        try :
            # load the dataset
            self.val_df = load(filename="val.csv")
        except Exception as e :
            raise Agentic_Exception(e, sys) from e

    def Eng_plus_Germ(self) :
        # Load the huggingface LLM model 
        model_id = "Qwen/Qwen2.5-1.5B-Instruct"

        try :
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.float16, # Use half-precision to save memory
                device_map="auto" # Automatically put it on the P100 GPU
            )

            # Create a text generation pipeline
            agent_pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=100)
        except Exception as e :
            raise Agentic_Exception(e, sys) from e



        # Our hard English query
        test_query = self.val_df['query'].iloc[0]
        print(f"Original Query: {test_query[:150]}...")

        system_prompt = """You are an expert Swiss lawyer. Your task is to extract the core legal concepts from the English query 
        and translate them into German keywords for a database search. 
        Also, list any relevant Swiss law abbreviations (like StPO, ZGB, OR, StGB)."""

        user_message = f"Query: {test_query}\n\nProvide the German keywords and Law abbreviations only:"

        # Format the prompt using Qwen's chat template
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        # Generate the response
        outputs = agent_pipe(prompt, do_sample=False)
        generated_text = outputs[0]["generated_text"][len(prompt):]
        

        print(f"Generated text: {generated_text.strip()}")
        return generated_text.strip()