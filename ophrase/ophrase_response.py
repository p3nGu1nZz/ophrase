from typing import List, Dict, Any
from .ophrase_log import Log
from .ophrase_const import Const
from .ophrase_gen import OphraseGen

class OphraseResponse:
    def __init__(self, cfg, task):
        self.gen = OphraseGen(cfg, task)

    def generate_responses(self, text: str) -> List[Dict[str, Any]]:
        Log.debug(f"Generating responses for: {text}")
        responses = self.gen.generate_responses(text)
        Log.debug(f"Generated responses: {responses}")
        return responses

    def generate_proofs(self, text: str, responses: List[str]) -> List[str]:
        Log.debug(f"Generating proofs for: {text}")
        proofs = self.gen.generate_proofs(text, responses)
        Log.debug(f"Generated proofs: {proofs}")
        return proofs
