import json
import re
from typing import Any, TypedDict, cast


class CleanResponseError(Exception):
    pass


class CleanResponseResponse(TypedDict):
    success: bool
    data: list



class CleanResponse:
    def __init__(self, response: str):
        self.response = response

    def get_json_from_html(self) -> list[Any]:
        pattern = r"window\.APP_INITIALIZATION_STATE\s*=\s*(\[[\s\S]*?\]);"
        match = re.search(pattern, self.response, re.DOTALL)

        if match:
            json_str = match.group(1)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e!s}")
                raise CleanResponseError(f"Failed to parse JSON: {e!s}") from e

        print("No match found for APP_INITIALIZATION_STATE")
        raise CleanResponseError("No match found for APP_INITIALIZATION_STATE") from None

    @staticmethod
    def clean_json(json_data: list[Any]) -> str:
        target_array = cast(list[Any], json_data[3])
        if len(target_array) <= 6:
            raise CleanResponseError("Invalid target array structure")
        cleaned_json = str(target_array[6]).split("\n")
        return cleaned_json[1]

    def clean_response(self) -> CleanResponseResponse:
        successfully_cleaned = False
        cleaned_json = []
        try:
            json_data = self.get_json_from_html()
            cleaned_json = json.loads(self.clean_json(json_data))
            successfully_cleaned = True
        except CleanResponseError as e:
            print(f"Failed to clean response: {e!s}")
            successfully_cleaned = False

        with open("test/test_suite/app/providers/google/debug/cleaned_response.json", "w") as f:
            json.dump(cleaned_json, f, indent=4)
        
        return {"success": successfully_cleaned, "data": cleaned_json}
