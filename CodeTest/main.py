from .tester import Tester
from CodeGen import fewshot
model_list=[fewshot.patched_document,fewshot.bnf_only,fewshot.nl_only,fewshot.example_only,fewshot.document]
def test_for_model(model):
    test=Tester("CodeTest/one_function")
    return test.test_all_tests(model)
def merge_dict(a,b):
    for index in b:
        if index in a:
            a[index]+=b[index]
def calc_result(model,counts,results):
    iter=len(results)
    template={"ok":0,"syntax_error":0,"runtime_error":0,"performance_error":0}
    result={"model_name":str(model),
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
    for model in model_list:
        counts=None
        results=[]
        for t in range(iter):
            count,result=test_for_model(model)
            if counts:
                merge_dict(counts,count)
            else:
                counts=count
            results.append(result)
        evaluation.append(calc_result(model,counts,results))
    with open("./experiment_result.txt","w+",encoding="utf-8") as fp:
        fp.write(str(evaluation))
    print("Done")
        
if __name__ == "__main__":
    main(10)

                


