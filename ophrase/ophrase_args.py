# ophrase_args.py

import argparse
from .ophrase_const import Const

def parse_args():
    parser = argparse.ArgumentParser(description=Const.ARG_DESCRIPTION)
    parser.add_argument(Const.ARG_TEXT, type=str, help=Const.ARG_TEXT_HELP)
    parser.add_argument(Const.ARG_DEBUG, action="store_true", help=Const.ARG_DEBUG_HELP)
    parser.add_argument(Const.ARG_PROMPT, action="store_true", help=Const.ARG_PROMPT_HELP)
    return parser.parse_args()
