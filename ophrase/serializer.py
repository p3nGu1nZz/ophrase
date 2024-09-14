from typing import List, Dict, Any

class Serializer:
    @staticmethod
    def serialize_output(text: str, responses: List[Dict[str, Any]], response_prompts: List[str], include_prompts: bool) -> Dict[str, Any]:
        result = {
            "original_text": text,
            "responses": responses[0]["responses"]
        }
        if include_prompts:
            result["prompts"] = {
                "responses": response_prompts
            }
        return result
