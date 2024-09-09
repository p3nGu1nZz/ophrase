from typing import List, Dict, Any
from .log import Log
from .constants import Const
from .template import Template
import random

class Generator:
    def __init__(self, cfg, task):
        self.cfg = cfg
        self.task = task

    def generate_responses(self, original_text: str) -> List[Dict[str, Any]]:
        Log.debug(f"Generating responses for: {original_text}")
        results = self._collect_responses(original_text)
        Log.debug(f"Collected responses: {results}")
        
        combined_responses = self._combine_and_shuffle_responses(results)
        Log.debug(f"Combined and shuffled responses: {combined_responses}")
        
        return [{"original_text": original_text, "responses": combined_responses}]

    def _collect_responses(self, original_text: str) -> List[Dict[str, Any]]:
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

    def _combine_and_shuffle_responses(self, results: List[Dict[str, Any]]) -> List[str]:
        combined_responses = []
        for response in results:
            Log.debug(f"Adding response data: {response['response']}")
            combined_responses.extend(response['response'])
        
        Log.debug(f"Combined responses before shuffling: {combined_responses}")
        random.shuffle(combined_responses)
        Log.debug(f"Combined responses after shuffling: {combined_responses}")

        return combined_responses
