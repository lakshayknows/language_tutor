import os
from pydantic import BaseModel

class PromptConfig(BaseModel):
    system_prompt: str

def load_system_prompt() -> PromptConfig:
    prompt_path = os.path.join("prompts", "system_prompt.txt")
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    return PromptConfig(system_prompt=text)

prompt_config = load_system_prompt()
system_prompt = prompt_config.system_prompt
