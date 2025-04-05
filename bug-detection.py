from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import ast
import traceback
import sys
import re

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webapp', 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webapp', 'static'))
CORS(app)

def perform_basic_analysis(code_snippet):
    """Perform basic static analysis of the code"""
    analysis = []
    
    # Check for common issues
    if 'eval(' in code_snippet:
        analysis.append("Warning: eval() usage detected. This can be a security risk.")
    
    if 'exec(' in code_snippet:
        analysis.append("Warning: exec() usage detected. This can be a security risk.")
    
    # Check for common security issues
    if 'os.system(' in code_snippet:
        analysis.append("Warning: os.system() usage detected. This can be a security risk.")
    
    # Check for common anti-patterns
    if 'try:\n    pass' in code_snippet:
        analysis.append("Warning: Empty try block detected. This can hide errors.")
    
    if analysis:
        return "\n".join(analysis)
    else:
        return "Basic analysis found no critical issues."

class FloatingPointChecker(ast.NodeVisitor):
    def __init__(self, errors):
        super().__init__()
        self.errors = errors

    def visit_Compare(self, node):
        # Check for floating point equality comparisons
        if any(isinstance(op, (ast.Eq, ast.NotEq)) for op in node.ops):
            # Check if either side involves floating point operations or literals
            has_float = False
            
            # Check left side
            if isinstance(node.left, ast.BinOp):
                has_float = self._check_float_operation(node.left)
            elif isinstance(node.left, ast.Num) and isinstance(node.left.n, float):
                has_float = True
            elif isinstance(node.left, ast.Constant) and isinstance(node.left.value, float):
                has_float = True
            
            # Check right side
            for comparator in node.comparators:
                if isinstance(comparator, ast.BinOp):
                    has_float = has_float or self._check_float_operation(comparator)
                elif isinstance(comparator, ast.Num) and isinstance(comparator.n, float):
                    has_float = True
                elif isinstance(comparator, ast.Constant) and isinstance(comparator.value, float):
                    has_float = True
            
            if has_float:
                self.errors.append({
                    'error_type': 'floating point error',
                    'message': "Direct equality comparison of floating-point numbers may be unreliable due to precision issues",
                    'line': node.lineno,
                    'fix_suggestion': "Use math.isclose() instead of == for floating-point comparisons"
                })
        
        self.generic_visit(node)
    
    def _check_float_operation(self, node):
        # Check if operation involves floats
        if isinstance(node, ast.BinOp):
            # Check if either operand is a float
            left_float = (isinstance(node.left, ast.Num) and isinstance(node.left.n, float)) or \
                        (isinstance(node.left, ast.Constant) and isinstance(node.left.value, float))
            right_float = (isinstance(node.right, ast.Num) and isinstance(node.right.n, float)) or \
                         (isinstance(node.right, ast.Constant) and isinstance(node.right.value, float))
            
            # Check if operation typically produces floats
            produces_float = isinstance(node.op, (ast.Div, ast.FloorDiv))
            
            return left_float or right_float or produces_float or \
                   self._check_float_operation(node.left) or self._check_float_operation(node.right)
        return False

def detect_errors(code_snippet):
    errors = []
    tree = None
    
    # Check for empty code
    if not code_snippet.strip():
        return [{'error_type': 'syntax error', 'message': 'Empty code snippet', 'line': 0}]

    # Try to parse the entire code first
    try:
        tree = ast.parse(code_snippet)
    except SyntaxError as e:
        error_line = e.lineno if hasattr(e, 'lineno') else 1
        return [{
            'error_type': 'syntax error',
            'message': f"{e.msg} (in statement: {code_snippet.split('\n')[error_line-1] if error_line > 0 and error_line <= len(code_snippet.split('\n')) else ''})",
            'line': error_line
        }]

    # Track variables and their types
    var_types = {}
    list_sizes = {}  # Track list sizes when they're defined
    dict_keys = {}   # Track dictionary keys
    function_names = set()  # Track all function names
    
    # First pass: collect all function names
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_names.add(node.name)
    
    # Run floating point checks
    float_checker = FloatingPointChecker(errors)
    float_checker.visit(tree)

    # Run the rest of the error detection
    class TypeTracker(ast.NodeVisitor):
        def __init__(self):
            super().__init__()
            self.scope_stack = [set()]  # Stack of sets to track variables in different scopes
            self.current_scope = self.scope_stack[-1]
            self.builtin_names = {'print', 'input', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'open', 'os', 'set'}
            self.function_params = set()  # Track function parameters
            self.list_sizes = {}  # Track list sizes
            self.dict_keys = {}  # Track dictionary keys

        def enter_scope(self):
            self.scope_stack.append(set())
            self.current_scope = self.scope_stack[-1]

        def exit_scope(self):
            self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1] if self.scope_stack else set()

        def is_variable_defined(self, var_name):
            # Check if variable is defined in any accessible scope, is a function name, is a builtin, or is a function parameter
            return (any(var_name in scope for scope in self.scope_stack) or 
                   var_name in function_names or 
                   var_name in self.builtin_names or
                   var_name in self.function_params)

        def visit_FunctionDef(self, node):
            # Add function parameters to the function_params set
            for arg in node.args.args:
                self.function_params.add(arg.arg)
            
            # Add function name to the current scope
            self.current_scope.add(node.name)
            
            # Enter new scope for function body
            self.enter_scope()
            
            # Visit function body
            for stmt in node.body:
                self.visit(stmt)
            
            # Exit function scope
            self.exit_scope()

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                if not self.is_variable_defined(node.id):
                    errors.append({
                        'error_type': 'name error',
                        'message': f"Variable '{node.id}' is used before declaration",
                        'line': node.lineno
                    })
            elif isinstance(node.ctx, ast.Store):
                self.current_scope.add(node.id)
            
            self.generic_visit(node)

        def visit_Call(self, node):
            # Check for potential ValueError in int() conversion
            if isinstance(node.func, ast.Name) and node.func.id == 'int':
                if len(node.args) > 0:
                    arg = node.args[0]
                    if isinstance(arg, ast.Str):
                        # Check if the string contains non-numeric characters
                        if not arg.s.replace('-', '').replace('.', '').isdigit():
                            errors.append({
                                'error_type': 'value error',
                                'message': f"Potential ValueError: Cannot convert string '{arg.s}' to integer",
                                'line': node.lineno,
                                'fix_suggestion': "Make sure the string contains only valid integer characters"
                            })
            
            self.generic_visit(node)

        def visit_BinOp(self, node):
            # Check for division by zero
            if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
                if isinstance(node.right, ast.Num) and node.right.n == 0:
                    errors.append({
                        'error_type': 'runtime error',
                        'message': "Division by zero detected",
                        'line': node.lineno,
                        'fix_suggestion': "Add a check to ensure the denominator is not zero"
                    })
                elif isinstance(node.right, ast.Constant) and node.right.value == 0:
                    errors.append({
                        'error_type': 'runtime error',
                        'message': "Division by zero detected",
                        'line': node.lineno,
                        'fix_suggestion': "Add a check to ensure the denominator is not zero"
                    })
            
            # Get types of operands
            left_type = self._get_operand_type(node.left)
            right_type = self._get_operand_type(node.right)
            
            # Check for type incompatibilities
            if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod)):
                # String operations
                if left_type == 'str' and right_type in ('int', 'float'):
                    errors.append({
                        'error_type': 'type error',
                        'message': f"Cannot perform {self._get_operation_name(node.op)} between 'str' and '{right_type}'",
                        'line': node.lineno,
                        'fix_suggestion': "Convert the number to string using str() or use string formatting"
                    })
                elif left_type in ('int', 'float') and right_type == 'str':
                    errors.append({
                        'error_type': 'type error',
                        'message': f"Cannot perform {self._get_operation_name(node.op)} between '{left_type}' and 'str'",
                        'line': node.lineno,
                        'fix_suggestion': "Convert the number to string using str() or use string formatting"
                    })
                
                # List operations
                if left_type == 'list' and right_type not in ('list', 'int'):
                    errors.append({
                        'error_type': 'type error',
                        'message': f"Cannot perform {self._get_operation_name(node.op)} between 'list' and '{right_type}'",
                        'line': node.lineno,
                        'fix_suggestion': "Use list methods like extend() or append() for list operations"
                    })
                elif left_type not in ('list', 'int') and right_type == 'list':
                    errors.append({
                        'error_type': 'type error',
                        'message': f"Cannot perform {self._get_operation_name(node.op)} between '{left_type}' and 'list'",
                        'line': node.lineno,
                        'fix_suggestion': "Use list methods like extend() or append() for list operations"
                    })
            
            self.generic_visit(node)

        def _get_operand_type(self, node):
            if isinstance(node, ast.Num):
                return 'int' if isinstance(node.n, int) else 'float'
            elif isinstance(node, ast.Constant):
                if isinstance(node.value, int):
                    return 'int'
                elif isinstance(node.value, float):
                    return 'float'
                elif isinstance(node.value, str):
                    return 'str'
                elif isinstance(node.value, list):
                    return 'list'
            elif isinstance(node, ast.Str):
                return 'str'
            elif isinstance(node, ast.List):
                return 'list'
            elif isinstance(node, ast.Name):
                if node.id in var_types:
                    return var_types[node.id]
            return 'unknown'

        def _get_operation_name(self, op):
            if isinstance(op, ast.Add):
                return "addition"
            elif isinstance(op, ast.Sub):
                return "subtraction"
            elif isinstance(op, ast.Mult):
                return "multiplication"
            elif isinstance(op, ast.Div):
                return "division"
            elif isinstance(op, ast.FloorDiv):
                return "floor division"
            elif isinstance(op, ast.Mod):
                return "modulo"
            return "operation"

        def visit_Assign(self, node):
            # Track list sizes when lists are defined
            if isinstance(node.value, ast.List):
                list_size = len(node.value.elts)
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.list_sizes[target.id] = list_size
                        var_types[target.id] = 'list'
            
            # Track dictionary keys when dictionaries are defined
            if isinstance(node.value, ast.Dict):
                keys = []
                for key in node.value.keys:
                    if isinstance(key, ast.Str):
                        keys.append(key.s)
                    elif isinstance(key, ast.Constant) and isinstance(key.value, str):
                        keys.append(key.value)
                    elif isinstance(key, ast.Num):
                        keys.append(str(key.n))
                    elif isinstance(key, ast.Constant) and isinstance(key.value, (int, float)):
                        keys.append(str(key.value))
                
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.dict_keys[target.id] = set(keys)
                        var_types[target.id] = 'dict'
            
            self.generic_visit(node)

        def visit_Subscript(self, node):
            # Check for list index out of range
            if isinstance(node.value, ast.Name):
                var_name = node.value.id
                
                # Get the key/index value
                key = None
                if isinstance(node.slice, ast.Index):
                    if isinstance(node.slice.value, ast.Str):
                        key = node.slice.value.s
                    elif isinstance(node.slice.value, ast.Constant):
                        if isinstance(node.slice.value.value, str):
                            key = node.slice.value.value
                        elif isinstance(node.slice.value.value, int):
                            key = str(node.slice.value.value)
                    elif isinstance(node.slice.value, ast.Num):
                        key = str(node.slice.value.n)
                elif isinstance(node.slice, ast.Constant):
                    if isinstance(node.slice.value, str):
                        key = node.slice.value
                    elif isinstance(node.slice.value, int):
                        key = str(node.slice.value)
                elif isinstance(node.slice, ast.Num):
                    key = str(node.slice.n)
                
                # Check for dictionary key errors
                if key is not None and var_name in self.dict_keys:
                    if key not in self.dict_keys[var_name]:
                        errors.append({
                            'error_type': 'key error',
                            'message': f"KeyError: '{key}' is not a key in dictionary '{var_name}'",
                            'line': node.lineno,
                            'fix_suggestion': f"Available keys are: {', '.join(sorted(self.dict_keys[var_name]))}"
                        })
                
                # Check for list index out of range
                if key is not None and var_name in self.list_sizes:
                    try:
                        index = int(key)
                        list_size = self.list_sizes[var_name]
                        if index < 0 or index >= list_size:
                            errors.append({
                                'error_type': 'index error',
                                'message': f"List index {index} is out of range for list '{var_name}' with size {list_size}",
                                'line': node.lineno,
                                'fix_suggestion': f"List indices should be between 0 and {list_size-1}"
                            })
                        elif index > 100:  # Arbitrary large index check
                            errors.append({
                                'error_type': 'potential error',
                                'message': f"List index {index} seems unusually large and might cause IndexError",
                                'line': node.lineno
                            })
                    except ValueError:
                        pass  # Not a numeric index, skip list index check
            
            self.generic_visit(node)

    # Run type tracking analysis
    type_tracker = TypeTracker()
    type_tracker.visit(tree)

    # Remove duplicate errors
    seen_errors = set()
    unique_errors = []
    for error in errors:
        error_key = (error['error_type'], error['message'], error['line'])
        if error_key not in seen_errors:
            seen_errors.add(error_key)
            unique_errors.append(error)

    # Sort errors by line number
    unique_errors.sort(key=lambda x: x['line'])

    return unique_errors if unique_errors else [{'error_type': 'bug-free', 'message': 'No errors found in your code!', 'line': 0}]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/detect', methods=['POST'])
def detect():
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code.strip():
            return jsonify({'errors': [{'error_type': 'syntax error', 'message': 'Code input is empty!', 'line': 0}]}), 400

        results = detect_errors(code)
        
        return jsonify({'errors': results})

    except Exception as e:
        return jsonify({'errors': [{'error_type': 'internal error', 'message': str(e), 'line': 0}]}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
