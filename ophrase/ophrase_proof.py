# ophrase_proof.py

from typing import List, Dict, Any
from .ophrase_log import Log
from .ophrase_const import Const
from .ophrase_gen import OphraseGen

class OphraseProof:
    def __init__(self, cfg, task):
        self.gen = OphraseGen(cfg, task)

    def validate(self, original_text: str, responses: List[str]) -> List[str]:
        return self.gen.generate_proofs(original_text, responses)
