import ast
import operator

def safe_eval(expression):
    """
    Safely evaluate a mathematical expression string.
    Only allows basic operators (+, -, *, /) and numbers.
    """
    # Allowed operators
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def _eval(node):
        if isinstance(node, ast.Constant):  # Number
            if isinstance(node.value, (int, float)):
                return node.value
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            if type(node.op) in operators:
                return operators[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> (e.g., -1)
            if type(node.op) in operators:
                return operators[type(node.op)](_eval(node.operand))
        elif isinstance(node, ast.Expression):
            return _eval(node.body)
        
        raise ValueError(f"Unsupported operation or type: {node}")

    try:
        # Parse the expression
        node = ast.parse(expression, mode='eval')
        return _eval(node.body)
    except Exception as e:
        # Re-raise as ValueError for consistent error handling
        raise ValueError(f"Invalid expression: {e}")
