import json
class Parser:
    def __init__(self):
        self.modes={"json":self.parse_json}
    def parse(self,mode,text):
        print(mode,text)
        if mode in self.modes:
            return self.modes[mode](text)
        else:
            return self.parse_default(mode,text)
    @staticmethod
    def parse_default(mode,text):
        begin_str="```"+mode
        begin_len=len(begin_str)
        begin=text.find(begin_str)
        end=text.find("```",begin+begin_len)
        if begin != -1 and end != -1:
            text = text[begin+7:end]
            return text
        else:
            print(text)
            raise Exception("markdown block not found")
    @staticmethod
    def parse_json(text):
        text = Parser.parse_default("json",text)
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise Exception(f"JSON parsing error: {e}")