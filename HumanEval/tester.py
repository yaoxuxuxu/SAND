from CodeTest.tester import Tester
import pandas as pd
class HumanEvalTester(Tester):
    def __init__(self, test_dir):
        super().__init__(test_dir)
        self.test_cases = self.load_test_cases()

    def test_once(self,test):
        model=self.model()
        model.user_add(test['prompt'])
        sys_prompt="You can only use Programming language sand." \
        "complete the code,We will test your code by calling `function(xxxxxxx)`."\
        "You must provide a top-level function named `function`."\
        "do not put it inside a class"\
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
        with open("./CodeTest/temp/generate"+self.test_id+".sand","w+") as fp:
            fp.write(code)
        try:
            self.run_test(code,test["std"],test["data"])
            return "OK!",code
        except Exception as e:
            return str(e),code

    def read_dataset(self):
        df = pd.read_parquet("hf://datasets/openai/openai_humaneval/openai_humaneval/test-00000-of-00001.parquet")
        res = df.to_dict("records")
        return res

if __name__ == "__main__":
    tester = HumanEvalTester("CodeTest/one_function")
    print(tester.datasets[0])  # Print the first test case