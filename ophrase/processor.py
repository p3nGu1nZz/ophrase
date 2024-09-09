from tenacity import retry, stop_after_attempt, wait_fixed
from typing import List, Dict, Any, Tuple
import json, subprocess as proc, ollama as oll
from .log import Log
from .constants import Const
from .task import Task
from .template import TASKS 

class Processor:
    def __init__(self, cfg, task: Task):
        self.cfg = cfg
        self.task = task
        Log.setup(self.cfg.debug)

    def run_command(self, cmd: List[str], error_msg: str = Const.RUN_COMMAND_ERROR) -> None:
        try:
            result = proc.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                Log.error(result.stdout)
                raise Exception(error_msg)
        except FileNotFoundError:
            Log.error(error_msg)
            raise Exception(error_msg)

