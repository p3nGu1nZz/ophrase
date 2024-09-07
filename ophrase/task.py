from typing import List, Dict, Any
from .ophrase_log import Log
from .ophrase_const import Const
from .ophrase_template import TASKS
import subprocess as proc
import ollama as oll
import json

class Task:
    def __init__(self, cfg):
        self.cfg = cfg

    def run(self, cmd: List[str], error_msg: str = Const.RUN_COMMAND_ERROR) -> None:
        try:
            result = proc.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                Log.error(result.stdout)
                raise Exception(error_msg)
        except FileNotFoundError:
            Log.error(error_msg)
            raise Exception(error_msg)

    def execute(self, text: str, task: str, template, system_prompt, instructions) -> Dict[str, Any]:
        prompt = template.render(
            system=system_prompt,
            task=task,
            text=text,
            example=TASKS[task],
            instructions=instructions,
            lang=self.cfg.lang
        )
        Log.debug(f"Prompt: {prompt}")
        
        output = oll.generate(prompt=prompt, model=self.cfg.model)
        Log.debug(f"Response: {output}")
        Log.debug(Const.PROMPT_SEPARATOR)
        
        data = output['response']
        Log.debug(f"Data: {data}")
        
        response = json.loads(data)
        Log.debug(f"Response: {response}")
        
        return {"prompt": prompt, "data": data, "response": response}
