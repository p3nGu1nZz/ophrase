from typing import List
from .log import Log

class Proof:
    def __init__(self, gen):
        self.gen = gen

    def generate(self, text: str, responses: List[str]) -> List[str]:
        Log.debug(f"Generating proofs for: {text}")
        proofs = self.gen.generate_proofs(text, responses)
        Log.debug(f"Generated proofs: {proofs}")
        return proofs
