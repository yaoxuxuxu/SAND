import os
from google import genai
from google.genai import types
import time
class ModelManager:
    def __init__(self,model):
        self.api_pool=self.readApiKey()
        self.api_index=-1
        self.change_api()
        #self.show_available_models()
        self.model_name=model
        self.history=[]
        #self.chat=self.client.chats.create(model="gemini-2.5-flash",config=self.config())
    def change_api(self):
        self.api_index=(self.api_index+1)%len(self.api_pool)
        self.client = genai.Client(api_key=self.api_pool[self.api_index])
    def show_available_models(self):
        models = self.client.models.list()
        for model in models:
            print(model.name)
        return
    def readApiKey(self):
        while True:
            try:
                with open("./CodeGen/apikey","r+") as fp:
                    res=fp.read()
                break
            except Exception as e:
                print(os.getcwd())
                print(f"Error occurred while reading API key: {e}")
                time.sleep(5)
        apis=[]
        for i in res.split("\n"):
            if len(i)<5:
                continue
            if "#" in i:
                continue
            apis.append(i)
        return apis
    def config(self,config_prompt):
        return {"system_instruction": config_prompt}
    def user_add(self,message):
        message=types.UserContent(
        parts=[types.Part(text=message)]
        )
        self.history.append(message)
    def assistant_add(self,message):
        message=types.Content(
        parts=[types.Part(text=message)]
        )
        self.history.append(message)
    def getLastSolution(self,returnText=True):
        cnt=len(self.history)-1
        while cnt>=0:
            text=self.history[cnt].parts[0].text
            if text == "!!!next stage!!!" and len(text)<20:
                cnt-=1
                continue
            if type(self.history[cnt])==types.Content:
                if returnText:
                    return text
                return self.history[cnt]
            cnt-=1
        return None
    
    def user_input(self):
        res=input()
        self.user_add(res)
        return
    
    def send(self,config_prompt,contexts=None):
        if contexts is None:
            contexts = self.history
        while True:
            try:
                res=self.client.models.generate_content(model=self.model_name,
                                                    temperature=0.2,
                                                    config=self.config(config_prompt),
                                                    contents=contexts)
                assert(res.text!=None)
                break
            except Exception as e:
                print(f"Error occurred: {e}")
                if "exceed" in str(e):
                    self.change_api()
                time.sleep(5)  # Wait for 1 second before retrying
        self.assistant_add(res.text)
        return res.text
if __name__ == "__main__":
    mm=ModelManager()
    while True:
        s=input()
        if s=="exit":
            break
        res=mm.send(s)
        print(res)
    print(mm.history)
    