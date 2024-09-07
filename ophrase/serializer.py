from typing import List, Dict, Any
from .log import Log  # Updated import
from .ophrase_const import Const

class Serializer:
    @staticmethod
    def serialize_output(text: str, results: List[Dict[str, Any]], response_prompts: List[str], proof_prompts: List[str], include_prompts: bool) -> Dict[str, Any]:
        if isinstance(results, dict) and Const.ERROR_KEY in results:
            Log.error(Const.ERROR_MESSAGE)
            return results
        
        combined_responses = [response for result in results for response in result["response"]]
        
        output = {
            Const.ORIGINAL_TEXT_KEY: text,
            Const.RESPONSES_KEY: combined_responses,
            Const.PROOFS_KEY: combined_responses
        }
        
        if include_prompts:
            output[Const.PROMPTS_KEY] = {
                Const.RESPONSES_KEY: response_prompts,
                Const.PROOFS_KEY: proof_prompts
            }
        
        return output