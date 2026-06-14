def one_function_testcode(param):
    code=f"""
    import testcode
    import stdcode
    testcode.function({param})==stdcode.function({param})
    """
    return code