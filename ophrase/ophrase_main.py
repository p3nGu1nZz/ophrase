from tenacity import retry, stop_after_attempt, wait_fixed
from rich.console import Console
from .ophrase_log import Log
from .ophrase_serializer import serialize_output
from .ophrase_const import Const
from .ophrase_config import Config
from .ophrase_manager import OphraseManager
from .ophrase_args import parse_args
import json

console = Console()

class OphraseMain:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.manager = OphraseManager(cfg)

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
    def _run(self, text: str, debug: bool, include_prompts: bool) -> None:
        if not debug:
            Log.setup(debug)
        Log.debug(Const.STARTING_MAIN_FUNCTION)
        try:
            self.manager.check()
            res, response_prompts = self.manager.generate(text)
            proofs = self.manager.validate(text, [r["response"] for r in res])
            proof_prompts = response_prompts
            final_result = serialize_output(text, res, response_prompts, proof_prompts, include_prompts)
            print(json.dumps(final_result, indent=2, separators=(',', ': ')))
        except ValidationError as e:
            error_output = {Const.ERROR_KEY: f"{Const.VALIDATION_ERROR}{e}"}
            if debug:
                import traceback
                error_output["trace"] = traceback.format_exc()
            print(json.dumps(error_output, indent=2, separators=(',', ': ')))
        except Exception as e:
            error_output = {Const.ERROR_KEY: f"{Const.ERROR_PROCESSING_INPUT}{e}"}
            if debug:
                import traceback
                error_output["trace"] = traceback.format_exc()
            print(json.dumps(error_output, indent=2, separators=(',', ': ')))
            raise SystemExit(1)

def main():
    args = parse_args()
    cfg = Config(debug=args.debug)
    ophrase_main = OphraseMain(cfg)
    ophrase_main._run(args.text, args.debug, args.prompt)
