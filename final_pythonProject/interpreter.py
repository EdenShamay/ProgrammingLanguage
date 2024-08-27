from lexer import (t_PLUS, t_MINUS, t_MULTIPLY, t_DIVIDE, t_MODULO, t_AND, t_OR, t_EQ, t_NEQ, t_GT, t_LT,
                   t_GEQ, t_LEQ, t_NOT,t_FUNCTION)
from parser import Lambda, AST


class Interpreter:

    def visit(self, node, env):
        method_name = 'visit_' + type(node).__name__
        method = getattr(self, method_name)
        return method(node,env)

    def visit_BinOp(self, node, env):
        left_val = self.visit(node.left,env)
        right_val = self.visit(node.right,env)

        if node.op.type == t_PLUS:
            if isinstance(left_val, str) and isinstance(right_val, str):
                return left_val + right_val
            elif isinstance(left_val, (int, float, bool)) and isinstance(right_val, (int, float, bool)):
                return left_val + right_val
        elif node.op.type == t_MINUS:
            if isinstance(left_val, (int, float, bool)) and isinstance(right_val, (int, float, bool)):
                return left_val - right_val
        elif node.op.type == t_MULTIPLY:
            if isinstance(left_val, (int, float, bool)) and isinstance(right_val, (int, float, bool)):
                return left_val * right_val
        elif node.op.type == t_DIVIDE:
            if isinstance(left_val, (int, float, bool)) and isinstance(right_val, (int, float, bool)):
                if(left_val == 0 ):
                    raise Exception("Can not divide by zero")
            else:
                return left_val / right_val
        elif node.op.type == t_MODULO:
            if isinstance(left_val, (int, bool)) and isinstance(right_val, (int, bool)):
                return left_val % right_val
        elif node.op.type == t_AND:
            if(left_val == right_val):
                return True
            else:
                return False
           ## return left_val and right_val
        elif node.op.type == t_OR:
            return left_val or right_val
        elif node.op.type == t_EQ:
            return left_val == right_val
        elif node.op.type == t_NEQ:
            return left_val != right_val
        elif node.op.type == t_GT:
            return left_val > right_val
        elif node.op.type == t_LT:
            return left_val < right_val
        elif node.op.type == t_GEQ:
            return left_val >= right_val
        elif node.op.type == t_LEQ:
            return left_val <= right_val

    def visit_Num(self, node,env):
        return node.value

    def visit_Bool(self, node,env):
        return node.value

    def visit_UnaryOp(self, node,env):
        op = node.op.type
        if op == t_NOT:
            return not self.visit(node.expr)
        elif op == t_MINUS:
            return -self.visit(node.expr)

    def visit_Parameter(self, node, env):
        if env[node.fname][1]:
            return self.visit(env[node.fname][1][node.value], env)

    def visit_Function(self, node,env):
        node.params = [param.value for param in node.params]
        env[node.name] = node

    def visit_FunctionCall(self,node,env):
        func = env[node.name.value]
        parmas = dict(zip(func.params, node.args))
        func.params = parmas
        new_env = {node.name.value:(t_FUNCTION,parmas,func.body)}
        return self.call_function(func, node.name, new_env)

    def call_function(self, func, name, env):
        result = self.visit(func.body, env)
        return result

    def visit_Lambda(self, node, env):
        # For lambda expressions, create a function-like object
        return lambda *args: self.with_env(dict(zip(node.params, args)), lambda: self.visit(node.body, {}))

    def with_env(self, new_env, func):
        # Create a new environment and run the function with it
        old_env = self.env.copy()  # Save the old environment
        self.env.update(new_env)
        result = func()
        self.env = old_env  # Restore the old environment
        return result



    def interpret(self, tree, env):

        return self.visit(tree, env)
