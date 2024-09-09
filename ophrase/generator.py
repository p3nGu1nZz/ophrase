from typing import List, Dict, Any
from .log import Log
from .constants import Const
from .template import Template

class Generator:
    def __init__(self, cfg, task):
        self.cfg = cfg
        self.task = task

    def generate_responses(self, original_text: str) -> List[Dict[str, Any]]:
        Log.debug(f"Generating responses for: {original_text}")
        results = []
        response_template = Template.TEMPLATES["response"]
        system_prompt = Template.SYSTEM_PROMPTS["response"]
        for task in Template.TASKS.keys():
            if task == "proof":
                continue
            response = self.task.execute(original_text, task, response_template, system_prompt, Template.INSTRUCTIONS)
            if Const.ERROR_KEY not in response:
                results.append(response)
            if len(results) >= 3:
                break
        return results

    def generate_proofs(self, original_text: str, responses: List[str]) -> List[str]:
        Log.debug(f"Generating proofs for: {original_text}")
        valid_responses = []
        proof_template = Template.TEMPLATES["proof"]
        system_prompt = Template.SYSTEM_PROMPTS["proof"]
        for response in responses:
            proof_response = self.task.execute(response, "proof", proof_template, system_prompt, Template.INSTRUCTIONS)
            valid_responses.append(proof_response["response"])
        return valid_responses
