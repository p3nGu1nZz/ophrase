# ophrase.py

import json
from typing import List, Dict, Any, Tuple
from .ophrase_const import Const
from .ophrase_config import Config
from .ophrase_manager import OphraseManager
from .ophrase_main import OphraseMain
from .ophrase_args import parse_args

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

if __name__ == "__main__":
    try:
        args = parse_args()
        cfg = Config(debug=args.debug)
        ophrase = Ophrase(cfg)
        ophrase_main = OphraseMain(cfg)
        ophrase_main._run(args.text, args.debug, args.prompt)
    except Exception as e:
        error_output = {Const.ERROR_KEY: f"{Const.ERROR_PROCESSING_INPUT}{e}"}
        if args.debug:
            import traceback
            error_output["trace"] = traceback.format_exc()
        print(json.dumps(error_output, indent=2, separators=(',', ': ')))
        raise SystemExit(1)
