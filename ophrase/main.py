from tenacity import retry, stop_after_attempt, wait_fixed
from rich.console import Console
from typing import List, Dict, Any, Tuple
from .log import Log
from .serializer import Serializer
from .ophrase_const import Const
from .ophrase_config import Config
from .manager import Manager
from .ophrase_args import parse_args
from .error import handle_error, ValidationError
import json

console = Console()

class Main:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.manager = Manager(cfg)

    @staticmethod
    @retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
    def run():
        try:
            args = parse_args()
            main = Main(Config(debug=args.debug))
            Log.setup(args.debug)
            Log.start_main_function()
            main._execute(args.text, args.debug, args.prompt)
        except Exception as e:
            handle_error(e, args.debug)

    def _execute(self, text: str, debug: bool, include_prompts: bool) -> None:
        try:
            self.manager.check()
            responses, response_prompts = self.manager.generate(text)
            proofs = self.manager.validate(text, [r["response"] for r in responses])
            final_result = Serializer.serialize_output(text, responses, response_prompts, proofs, include_prompts)
            print(json.dumps(final_result, indent=2, separators=(',', ': ')))
        except ValidationError as e:
            handle_error(e, debug)
        except Exception as e:
            handle_error(e, debug)
