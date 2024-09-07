import json
from .ophrase_const import Const

def handle_error(e: Exception, debug: bool) -> None:
    error_output = {Const.ERROR_KEY: f"{Const.ERROR_PROCESSING_INPUT}{e}"}
    if debug:
        import traceback
        error_output["trace"] = traceback.format_exc()
    print(json.dumps(error_output, indent=2, separators=(',', ': ')))
    raise SystemExit(1)
