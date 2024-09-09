from typing import List, Dict, Any
from .log import Log
from .constants import Const
from .template import Template
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
                self._log_error_and_raise(result.stdout, error_msg)
        except FileNotFoundError:
            self._log_error_and_raise(error_msg, error_msg)

    def execute(self, text: str, task: str, template, system_prompt, instructions) -> Dict[str, Any]:
        prompt = self._render_prompt(text, task, template, system_prompt, instructions)
        prompt = self._post_process(prompt, task)
        Log.debug(f"Prompt: {prompt}")
        
        output = self._generate_output(prompt)
        Log.debug(f"Response: {output}")
        Log.debug(Const.PROMPT_SEPARATOR)
        
        response = self._parse_response(output['response'])
        Log.debug(f"Response: {response}")
        
        return {"prompt": prompt, "data": output['response'], "response": response}

    def _log_error_and_raise(self, error_message: str, exception_message: str) -> None:
        Log.error(error_message)
        raise Exception(exception_message)

    def _render_prompt(self, text: str, task: str, template, system_prompt, instructions) -> str:
        return template.render(
            system=system_prompt,
            task=task,
            text=text,
            example=Template.TASKS[task],
            instructions=instructions,
            lang=self.cfg.lang
        )

    def _post_process(self, prompt: str, task: str) -> str:
        replacements = {
            "{{ task }}": task,
            "{{ lang }}": Const.LANG_DEFAULT
        }
        for key, value in replacements.items():
            prompt = prompt.replace(key, value)
        return prompt

    def _generate_output(self, prompt: str) -> Dict[str, Any]:
        return oll.generate(prompt=prompt, model=self.cfg.model)

    def _parse_response(self, response: str) -> Any:
        Log.debug(f"Raw response: {response}")
        try:
            # Ensure the response is a valid JSON array
            return json.loads(response)
        except json.JSONDecodeError as e:
            Log.error(f"JSON decode error: {e}")
            return {"error": "Invalid JSON response"}

    def create_prompt(self, text: str, task: str) -> str:
        template = Template.TEMPLATES[task]
        system_prompt = Template.SYSTEM_PROMPTS[task]
        instructions = Template.INSTRUCTIONS
        return self._render_prompt(text, task, template, system_prompt, instructions)
