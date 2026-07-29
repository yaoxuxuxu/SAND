from openai import OpenAI
import json
class ModelManager:
    def __init__(self,system_prompt=None,temperature=1.0):
        self.readAPIkey()
        self.messages=[]
        self.temperature=temperature
        if system_prompt:
            self.setSystemPrompt(system_prompt)
    def readAPIkey(self):
        with open("./CodeGen/foundryKey","r+",encoding="utf-8")as fp:
            res=json.load(fp)
        self.client=OpenAI(base_url=res['endpoint'],api_key=res['api_key'])
        self.modelname=res['deployment_name']
        return
    def send(self,message=None):
        if message:
            self.addUser(message)
        completion = self.client.chat.completions.create(
            model=self.modelname,
            messages=self.messages,
            temperature=self.temperature
        )
        res=completion.choices[0].message
        res=res.content
        self.addAssistant(res)
        return res
    def addUser(self,message):
        self.messages.append({"role": "user","content": message})
    def addAssistant(self,message):
        self.messages.append({"role": "assistant","content": message})
    def setSystemPrompt(self,message):
        system_prompt={"role": "system","content": message}
        if len(self.messages)>0 and self.messages[0]["role"]=='system':
            self.messages[0]=system_prompt
        self.messages.insert(0,system_prompt)
        
if __name__ == "__main__":
    mm=ModelManager()
    print("Initializing Complete!")
    while True:
        res=input()
        if res=="exit":
            break
        res=mm.send(res)
        print(res)