import pandas as pd
import os
class ExcelMaker:
    def __init__(self,input_dir="",output_dir=""):
        self.input_dir=input_dir
        self.output_dir=output_dir
        if input_dir!="" and output_dir!="":
            self.init()
    def init(self):
        self.data=self.read_dict(self.input_dir)
        self.excel_writter=pd.ExcelWriter(self.output_dir)
    def set_dir(self,input_dir,output_dir):
        self.input_dir=input_dir
        self.output_dir=output_dir
        self.init()
    def excel_pre_data(self):
        basic_data=self.parse_basic_pre(self.data)
        self.write_basic(basic_data)
    def excel_advance_data(self):
        concrete_data=self.parse_promblem(self.data)
        self.write_concrete_data(concrete_data)
    def excel_basic_data(self):
        basic_data=self.parse_basic(self.data)
        self.write_basic(basic_data)
    @staticmethod
    def parse_basic_pre(data):
        basic_data=[]
        print(data)
        for model in data:
            #first sheet
            model_name=model
            solve_avg=data[model]
            tmp={"model_name":model_name}
            for key in solve_avg:
                tmp[key]=solve_avg[key]
            basic_data.append(tmp)
        return basic_data
    @staticmethod
    def parse_basic(data):
        basic_data=[]
        for model in data:
            #first sheet
            model_name=model["model_name"]
            start=model_name.find("fewshot.")+8
            end=model_name.rfind("'>")
            model_name=model_name[start:end]

            solve_avg=model["solve_avg"]
            tmp={"model_name":model_name}
            for key in solve_avg:
                tmp[key]=solve_avg[key]
            basic_data.append(tmp)
        return basic_data
    @staticmethod
    def parse_promblem(data):
        concrete_data={}
        for model in data:
            #second sheet
            model_name=model["model_name"]
            status_per_test=model["status_per_test"]
            problem=["fib", "sort", "max min avg", "return_all", "is_prime", "gcd", "reverse array", "lunar year", "rock paper scissors", "write a file"]
            model_eval={}
            for index in range(len(status_per_test)):
                model_eval[problem[index]]=status_per_test[index]
                
            concrete_data[model_name]=model_eval
        return concrete_data
    
    def write_basic(self,basic_data):
        df=pd.DataFrame(basic_data)
        df.to_excel(self.excel_writter, sheet_name="Sheet1", startrow=0, index=False)
    def write_concrete_data(self,concrete_data):
        for model in concrete_data:
            row=0
            df=pd.DataFrame(concrete_data[model])
            df.index.name=model
            df.to_excel(self.excel_writter,startrow=row, sheet_name="Sheet2")
            row+=len(df)+4
    def save(self):
        self.excel_writter.close()
    @staticmethod
    def read_dict(dir):
        with open(dir,"r",encoding="utf-8") as fp:
            data=fp.read()
        data=eval(data)
        return data
    @staticmethod
    def read_list(dir):
        return ExcelMaker.read_dict(dir)
    


em=ExcelMaker()
def pre_ex():
    input_dir="pre_sand.txt"
    output_dir="pre_output.xlsx"
    em.set_dir(input_dir, output_dir)
    em.excel_pre_data()
    em.save()
def main_ex():
    input_dir="experiment_result.txt"
    output_dir="experiment_result.xlsx"
    em.set_dir(input_dir, output_dir)
    em.excel_basic_data()
    em.excel_advance_data()
    em.save()
if __name__=="__main__":
    pre_ex()
    #main_ex()

    print("Done!")