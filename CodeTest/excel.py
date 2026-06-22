import pandas as pd
def read():
    with open("experiment_result.txt","r",encoding="utf-8") as fp:
        data=fp.read()
    data=eval(data)
    return data

def parse(data):
    basic_data=[]
    concrete_data={}
    for model in data:
        #first sheet
        model_name=model["model_name"]
        start=model_name.find("fewshot.")+8
        end=model_name.rfind("'>")
        model_name=model_name[start:end]

        solve_avg=model["solve_avg"]
        status_per_test=model["status_per_test"]
        tmp={"model_name":model_name}
        for key in solve_avg:
            tmp[key]=solve_avg[key]
        basic_data.append(tmp)
        #second sheet
        problem=["fib", "sort", "max min avg", "return_all", "is_prime", "gcd", "reverse array", "lunar year", "rock paper scissors", "write a file"]
        model_eval={}
        for index in range(len(status_per_test)):
            model_eval[problem[index]]=status_per_test[index]
            
        concrete_data[model_name]=model_eval
    return basic_data, concrete_data

def write(basic_data,concrete_data):
    with pd.ExcelWriter("experiment_result.xlsx") as writer:
        df=pd.DataFrame(basic_data)
        df.to_excel(writer, sheet_name="Sheet1", startrow=0, index=False)
        row=0
        for model in concrete_data:
            df=pd.DataFrame(concrete_data[model])
            df.index.name=model
            df.to_excel(writer,startrow=row, sheet_name="Sheet2")
            row+=len(df)+4
        
def main():
    data=read()
    basic_data, concrete_data=parse(data)
    write(basic_data, concrete_data)

main()