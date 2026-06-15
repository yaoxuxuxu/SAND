import random
def generate():
    return [""]
def test(param):
    code="""
    import testcode
    import File
    testcode.function()
    if File.exist("output.txt"){
        s=File.read("output.txt")
        File.remove("output.txt")
        s=="hello world"
    }
    else{
        false
    }
    
    """
    return code