import json
class Parser:
    def __init__(self):
        self.modes={"json":self.parse_json}
    def parse(self,mode,text):
        if mode not in self.modes:
            raise Exception(f"Unsupported mode: {mode}")
        return self.modes[mode](text)
    @staticmethod
    def parse_json(text):
        begin=text.find("```json")
        end=text.find("```",begin+7)
        if begin != -1 and end != -1:
            text = text[begin+7:end]
        else:
            print(text)
            raise Exception("JSON code block not found")
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise Exception(f"JSON parsing error: {e}")