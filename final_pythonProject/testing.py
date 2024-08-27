from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def checkInterpreterForTesting(exp,env ):
    global result
    print(f">> {exp}")
    lexer = Lexer(exp)
    tokens, error = lexer.make_tokens()
    if error:
        print(error.as_string())
        return [], error
    #print(tokens)
    parser = Parser(tokens)
    tree = parser.parse()
    interpreter = Interpreter()
    try:
        result = interpreter.interpret(tree, env)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    return result, error


## tested :

env = {}

text1 = "3+1"
res = checkInterpreterForTesting(text1, env)

text2 = "(5+15) + (3+1)"
res2 = checkInterpreterForTesting(text2, env)

text3 = "4 < 7"
res3 = checkInterpreterForTesting(text3, env)

text4 = "(12+3) && (5*3)"
res4 = checkInterpreterForTesting(text4, env)

text5 = "((10+10)+3) % 4"
res5 = checkInterpreterForTesting(text5, env)

text6 = "(-1 > 0) || (2 > 10)"
res6 = checkInterpreterForTesting(text6, env)

text7 = "(7-5) $ (2 * 10)"
res7 = checkInterpreterForTesting(text7, env)

text8 = "0/90"
res8 = checkInterpreterForTesting(text8, env)













