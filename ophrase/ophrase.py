import json
from typing import List, Dict, Any, Tuple
from .ophrase_const import Const
from .ophrase_config import Config
from .ophrase_manager import OphraseManager

class Ophrase:
    def __init__(self, cfg: Config):
        self.manager = OphraseManager(cfg)

    def check(self) -> None:
        self.manager.check()

    def pull(self) -> None:
        self.manager.pull()

    def generate(self, text: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        return self.manager.generate(text)

    def validate(self, text: str, responses: List[str]) -> List[str]:
        return self.manager.validate(text, responses)
