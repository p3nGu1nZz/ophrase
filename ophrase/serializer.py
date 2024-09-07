from typing import List, Dict, Any
from .log import Log
from .ophrase_const import Const
from .error import handle_error, ValidationError

class Serializer:
    @staticmethod
    def serialize_output(text: str, results: List[Dict[str, Any]], response_prompts: List[str], proof_prompts: List[str], include_prompts: bool) -> Dict[str, Any]:
        try:
            if isinstance(results, dict) and Const.ERROR_KEY in results:
                raise ValidationError(Const.ERROR_MESSAGE)
            
            responses = [response for result in results for response in result["response"]]
            
            output = {
                Const.ORIGINAL_TEXT_KEY: text,
                Const.RESPONSES_KEY: responses,
                Const.PROOFS_KEY: responses
            }
            
            if include_prompts:
                output[Const.PROMPTS_KEY] = {
                    Const.RESPONSES_KEY: response_prompts,
                    Const.PROOFS_KEY: proof_prompts
                }
            
            return output
        except ValidationError as e:
            handle_error(e, True)
        except Exception as e:
            handle_error(e, True)
