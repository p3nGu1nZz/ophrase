from typing import List, Dict, Any
from .log import Log
from .generator import Generator

class Response:
    def __init__(self, cfg, task):
        self.gen = Generator(cfg, task)

    def generate(self, text: str) -> List[Dict[str, Any]]:
        Log.debug(f"Generating responses for: {text}")
        responses = self.gen.generate_responses(text)
        Log.debug(f"Generated responses: {responses}")
        return responses
