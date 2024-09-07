from typing import List, Dict, Any
from .log import Log  # Updated import
from .ophrase_const import Const
from .ophrase_template import TASKS, TEMPLATES, SYSTEM_PROMPTS, INSTRUCTIONS
import ollama as oll
import json

class Generator:
    def __init__(self, cfg, task):
        self.cfg = cfg
        self.task = task

    def generate_responses(self, original_text: str) -> List[Dict[str, Any]]:
        Log.debug(f"Generating responses for: {original_text}")
        results = []
        for task in TASKS.keys():
            response = self.task.execute(original_text, task, TEMPLATES["response"], SYSTEM_PROMPTS["response"], INSTRUCTIONS)
            if Const.ERROR_KEY not in response:
                results.append(response)
            if len(results) >= 3:
                break
        return results

    def generate_proofs(self, original_text: str, responses: List[str]) -> List[str]:
        Log.debug(f"Generating proofs for: {original_text}")
        valid_responses = []
        for response in responses:
            proof_response = self.task.execute(response, "paraphrase", TEMPLATES["proof"], SYSTEM_PROMPTS["proof"], INSTRUCTIONS)
            valid_responses.append(proof_response["response"])
        return valid_responses
