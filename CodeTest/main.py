from .tester import Tester
from CodeGen import fewshot
model_list=[fewshot.baseline,fewshot.example_only,fewshot.patched_document]

with open("./CodeGen/models.txt","r+") as fp:
    models=fp.read().split("\n")    

def test_for_model(model,llm):
    test=Tester("CodeTest/one_function")
    return test.test_all_tests(model,llm)
def merge_dict(a,b):
    for index in b:
        if index in a:
            a[index]+=b[index]
def calc_result(model,llm,counts,results):
    iter=len(results)
    template={"ok":0,"syntax_error":0,"runtime_error":0,"performance_error":0}
    result={"model_name":str(model),
            "llm":str(llm),
            "solve_avg":None,
            "status_per_test":None}
    for i in counts:
        counts[i]/=iter
    result["solve_avg"]=counts
    status=[]
    for j in range(len(results[0])):
        tmp=template.copy()
        for i in range(iter):
            tmp[results[i][j]]+=1
        status.append(tmp)
    result["status_per_test"]=status
    return result
            
def debug():
    pass
def main(iter):
    evaluation=[]
    for llm in models:
        for model in model_list:
            counts=None
            results=[]
            for t in range(iter):
                count,result=test_for_model(model,llm)
                if counts:
                    merge_dict(counts,count)
                else:
                    counts=count
                results.append(result)
            evaluation.append(calc_result(model,llm,counts,results))
    with open("./experiment_result.txt","w+",encoding="utf-8") as fp:
        fp.write(str(evaluation))
    print("Done")
        
if __name__ == "__main__":
    main(10)

                


