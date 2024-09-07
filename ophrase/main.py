from tenacity import retry, stop_after_attempt, wait_fixed
from rich.console import Console
from typing import List, Dict, Any, Tuple
from .ophrase_log import Log
from .ophrase_serializer import serialize_output
from .ophrase_const import Const
from .ophrase_config import Config
from .manager import Manager
from .ophrase_args import parse_args
from .error import handle_error
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
            main._setup_logging(args.debug)
            main._execute(args.text, args.debug, args.prompt)
        except Exception as e:
            handle_error(e, args.debug)

    def _setup_logging(self, debug: bool) -> None:
        if not debug:
            Log.setup(debug)
        Log.debug(Const.STARTING_MAIN_FUNCTION)

    def _execute(self, text: str, debug: bool, include_prompts: bool) -> None:
        try:
            self._check_manager()
            res, response_prompts = self._generate_responses(text)
            proofs = self._validate_responses(text, res)
            self._output_results(text, res, response_prompts, proofs, include_prompts)
        except ValidationError as e:
            handle_error(e, debug)
        except Exception as e:
            handle_error(e, debug)

    def _check_manager(self) -> None:
        self.manager.check()

    def _generate_responses(self, text: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        return self.manager.generate(text)

    def _validate_responses(self, text: str, responses: List[Dict[str, Any]]) -> List[str]:
        return self.manager.validate(text, [r["response"] for r in responses])

    def _output_results(self, text: str, res: List[Dict[str, Any]], response_prompts: List[str], proofs: List[str], include_prompts: bool) -> None:
        final_result = serialize_output(text, res, response_prompts, proofs, include_prompts)
        print(json.dumps(final_result, indent=2, separators=(',', ': ')))
