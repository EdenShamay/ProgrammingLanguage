from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def checkInterpreterForInteractive(interpreter, exp, env):
    global result
    lexer = Lexer(exp)
    tokens, error = lexer.make_tokens()
    if error:
        print(error.as_string())
        return [], error
    #print(tokens)
    parser = Parser(tokens)
    tree = parser.parse()
    try:
        result = interpreter.interpret(tree,env)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    return result, error


def run_interpreter(interpreter_impl, env):
    while True:
        try:
            text_input = input(">> ")
            if text_input.lower() in ('exit', 'quit'):
                break
            checkInterpreterForInteractive(interpreter_impl, text_input, env)
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    import sys
    interpreter = Interpreter()
    env = {}

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        checkInterpreterForInteractive(interpreter,text, env)
    else:
        run_interpreter(interpreter, env)


