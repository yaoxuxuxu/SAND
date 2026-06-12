from google import genai
from google.genai import types
import time
class ModelManager:
    def __init__(self):
        self.client = genai.Client(api_key=self.readApiKey())
        #self.show_available_models()
        self.model_pool=0
        self.useful_models=["gemini-2.5-flash","gemini-3-flash-preview","gemma-4-26b-a4b-it","gemma-4-31b-it"]
        self.history=[]
        #self.chat=self.client.chats.create(model="gemini-2.5-flash",config=self.config())
    def show_available_models(self):
        models = self.client.models.list()
        for model in models:
            print(model.name)
        return
    def readApiKey(self):
        with open("./CodeGen/apikey","r+") as fp:
            api=fp.read()
        return api
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
        self.history.append(self.user(res))
        return
    
    def send(self,config_prompt,contexts=None):
        if contexts is None:
            contexts = self.history
        while True:
            try:
                res=self.client.models.generate_content(model=self.useful_models[self.model_pool],
                                                    config=self.config(config_prompt),
                                                    contents=contexts)
                break
            except Exception as e:
                print(f"Error occurred: {e}")
                time.sleep(5)  # Wait for 1 second before retrying
                self.model_pool=(self.model_pool+1)%len(self.useful_models)
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
    