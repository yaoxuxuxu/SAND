from CodeTest.tester import Tester
import pyarrow.parquet as pq
import re
from CodeGen.fewshot import patched_document
from CodeTest.evaluator import SandEvaluator
import copy
from HumanEval.TestTranslator import TestTranslator
class HumanEvalTester(Tester):
    def __init__(self, model):
        self.badmatch=[]
        self.backup_dataset=None
        self.testTranslator=TestTranslator()
        super().__init__(model)
    def test_once(self,test):
        #task structure
        #{'task_id': '1', 'prompt': problem }
        model=self.model()
        model.user_add(test['prompt'])
        sys_prompt="Only use Programming language sand." \
        "Given problem is written in python"\
        "translate and rewrite the code in sand"\
        "Do not rename the function"\
        "Do not put it inside a class"\
        "do not write test or debug code for it." \
        "output as markdown format with name sand"
        while 1:
            try:
                code=model.send(sys_prompt)
                code=self.parse_markdown("sand",code)
                break
            except Exception as e:
                print(str(e))
                print("code generation bug occur!! retrying")
        return SandEvaluator(code).check_all(mode="data",tests=test["test"],funname=test["entry_point"])
    import pyarrow.parquet as pq

    def read_dataset(self):
        table = pq.read_table(
            "hf://datasets/openai/openai_humaneval/"
            "openai_humaneval/test-00000-of-00001.parquet"
        )
        res = table.to_pylist()

        self.backup_dataset = copy.deepcopy(res)

        for i in range(len(res)):
            res[i] = self.translate(res[i])

        index = 0
        while index < len(res):
            if res[index] is None:
                res.pop(index)
            else:
                index += 1

        return res
    def translate(self,test):
        try:
            return self.testTranslator.translate(test)
        except:
            self.badmatch.append(test["task_id"])


def debug_all_case():
    tester = HumanEvalTester(patched_document)
    failed=[]
    success=[]
    test_id=0
    for testcase in tester.datasets:
        print(f"Test Case : {test_id}")
        
        patience=5
        while patience:
            
            status,message=tester.test_once(testcase)
            if status == "pass":
                break
            print(status)
            print(message)
            patience-=1
        if patience:
            print(str(test_id)+" : Accepted")
            success.append(test_id)
        else:
            print(str(test_id)+" : Failed")
            failed.append(test_id) 
        test_id+=1
    acc=len(success)/len(tester.datasets)
    print(f"acc : {acc}")

    with open("HumanEval/results.txt","w+") as fp:
        fp.write(f"acc : {acc}\n")
        fp.write(f"failed cases : {failed}\n")
        
def debug_case(id):
    tester = HumanEvalTester(patched_document)
    print(tester.badmatch)
    test=tester.datasets[id]
    status,message=tester.test_once(test)
    print(test["test"])
    print(tester.backup_dataset[id]['test'])
    print(status)
    print(message)
def debug_translator(id):
    tester = HumanEvalTester(patched_document)
    print(len(tester.datasets),len(tester.backup_dataset),len(tester.badmatch))
    test=tester.backup_dataset[id]
    print(test["test"])
    test=TestTranslator().translate(test)
    print(test)

if __name__ == "__main__":
    #debug_translator(44)
    #debug_case(1)
    debug_all_case()
