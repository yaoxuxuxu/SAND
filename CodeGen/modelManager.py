from google import genai
class ModelManager:
    def __init__(self):
        self.client = genai.Client(api_key=self.readApiKey())
        self.chat=self.client.chats.create(model="gemini-2.5-flash",config=self.config())
    def readApiKey(self):
        with open("./CodeGen/apikey","r+") as fp:
            api=fp.read()
        return api
    def config(self):
        with open("./CodeGen/prompt_config.txt","r+") as fp:
            config_prompt=fp.read()
        return {"system_instruction": config_prompt}
    def fix_code(self,code):
        res=self.chat.send_message(code)
        return res.text
    def refix_code(self,message):
        message="Some bug occur.You need to fix this.Error Message:\n"+message
        res=self.chat.send_message(message)
        return res.text
    def main(self):
        res=self.chat.send_message("write a fib code, user input n, calculate fib(n)")
        with open("./CodeGen/test.py","w+") as fp:
            fp.write(res.text)

if __name__ == "__main__":
    mm=ModelManager()
    mm.main()
    