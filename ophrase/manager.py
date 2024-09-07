from typing import List, Dict, Any, Tuple
from .task import Task
from .generator import Generator
from .ophrase_log import Log
from .ophrase_const import Const
from .ophrase_config import Config

class Manager:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.task = Task(cfg)
        self.gen = Generator(cfg, self.task)
        self._log = Log

    def check(self) -> None:
        self.task.run(['ollama', '--version'], Const.RUN_COMMAND_ERROR)

    def pull(self) -> None:
        self.task.run(['ollama', 'pull', self.cfg.model], f"{Const.PULL_COMMAND_ERROR} {self.cfg.model}.")

    def generate(self, text: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        responses = self.gen.generate_responses(text)
        response_prompts = [r['prompt'] for r in responses]
        return responses, response_prompts

    def validate(self, text: str, responses: List[str]) -> List[str]:
        return self.gen.generate_proofs(text, responses)
