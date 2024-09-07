from typing import List, Dict, Any
from .ophrase_log import Log
from .ophrase_const import Const
from .ophrase_gen import Generator

class Response:
    def __init__(self, cfg, task):
        self.gen = Generator(cfg, task)
        self.proof = Proof(self.gen)

    def generate(self, text: str) -> List[Dict[str, Any]]:
        Log.debug(f"Generating responses for: {text}")
        responses = self.gen.generate_responses(text)
        Log.debug(f"Generated responses: {responses}")
        return responses
