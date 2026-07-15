import os
import time
from groq import Groq
class ModelManager:
    def __init__(self,model):
        self.api_pool=self.readApiKey()
        #print(self.api_pool)
        self.api_index=-1
        self.change_api()
        #self.show_available_models()
        self.model_name=model
        self.history=[]
        #self.chat=self.client.chats.create(model="gemini-2.5-flash",config=self.config())
    def change_api(self):
        self.api_index=(self.api_index+1)%len(self.api_pool)
        self.client = Groq(api_key=self.api_pool[self.api_index])
    def show_available_models(self):
        models = self.client.models.list()
        for model in models.data:
            print(model.id)
        return
    def readApiKey(self):
        while True:
            try:
                with open("./CodeGen/groq_apikey","r+") as fp:
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
        return {"role": "system","content": config_prompt}
    def user_add(self,message):
        message={
        "role": "user",
        "content": message
        }
        self.history.append(message)
    def assistant_add(self,message):
        message={
        "role": "assistant",
        "content": message
        }
        self.history.append(message)
    
    def send(self,config_prompt,contexts=None):
        #context change
        if contexts is None:
            contexts = self.history
        #system prompt setting
        if contexts[0]["role"]!="system":
            contexts.insert(0, self.config(config_prompt))
        else:
            contexts[0]["content"]=config_prompt
        
        while True:
            try:
                res = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=contexts
                )
                assert(res!=None)
                break
            except Exception as e:
                print(f"Error occurred: {e}")
                time.sleep(5)  # Wait for 1 second before retrying
        res=res.choices[0].message.content
        self.assistant_add(res)
        return res
    
if __name__ == "__main__":
    mm=ModelManager("llama-3.1-8b-instant")
    exit(0)
    #mm.show_available_models()
    while True:
        s=input()
        if s=="exit":
            break
        mm.user_add(s)
        res=mm.send("")
        print(res)
    print(mm.history)
    