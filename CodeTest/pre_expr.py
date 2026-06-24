from .tester import Tester
from CodeGen.fewshot import baseline
model_list=["gemma-4-26b-a4b-it"]#,"gemma-4-31b-it","gemini-2.5-flash","gemini-3-flash-preview"]
def test_for_model(model):
    test=Tester("CodeTest/one_function")
    return test.test_all_tests(lambda:baseline(model))
def merge_dict(a,b):
    for index in b:
        if index in a:
            a[index]+=b[index]
            
def main(iter):
    counts={}
    for _ in range(iter):
        for model in model_list:
            count,result=test_for_model(model)
            if model in counts:
                merge_dict(counts[model],count)
            else:
                counts[model]=count
    #normalization
    print(counts)
    for i in counts:
        for j in counts[i]:
            counts[i][j]/=iter
    
    with open("./pre_experiment_result.txt","w+",encoding="utf-8") as fp:
        fp.write(str(counts))
    print("Done")
        
if __name__ == "__main__":
    main(10)

                


