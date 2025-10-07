from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional
import requests
from flask import current_app
import re

def parse_llm_output(output: str) -> str:
    """Removes the <think>...</think> block from the LLM output."""
    return re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL).strip()

class LlamaServerLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        llama_server_url = current_app.config.get('LLAMA_SERVER_LLM_URL')
        try:
            response = requests.post(
                f"{llama_server_url}/v1/chat/completions",
                json={
                    "messages": [{"role": "user", "content": prompt}],
                    "model": "ggml-org/Qwen3-1.7B-GGUF"
                }
            )
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']
            return parse_llm_output(content)
        except requests.exceptions.RequestException as e:
            print(f"Error calling LLM API: {e}")
            return ""

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}
