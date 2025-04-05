from flask import Flask, request, jsonify, render_template
import ast
import traceback
import json
import os
from pathlib import Path

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

# Load test cases and training data
TEST_CASES_PATH = Path('archive (1)/test.json')
TRAIN_DATA_PATH = Path('archive (1)/train.json')
PROBLEM_DESC_PATH = Path('archive (1)/problem_descriptions')

test_cases = {}
training_data = {}

# Load test cases
if TEST_CASES_PATH.exists():
    with open(TEST_CASES_PATH, 'r') as f:
        test_cases = json.load(f)

# Load training data
if TRAIN_DATA_PATH.exists():
    with open(TRAIN_DATA_PATH, 'r') as f:
        training_data = json.load(f)

def load_problem_descriptions():
    problems = {}
    if PROBLEM_DESC_PATH.exists():
        for file in PROBLEM_DESC_PATH.glob('*.html'):
            with open(file, 'r') as f:
                content = f.read()
                problem_id = file.stem
                problems[problem_id] = {
                    'content': content,
                    'id': problem_id
                }
    return problems

problem_descriptions = load_problem_descriptions()

@app.route('/')
def home():
    return render_template('index.html',
                         problem_count=len(problem_descriptions),
                         test_cases_count=len(test_cases))

@app.route('/api/detect', methods=['POST'])
def detect():
    try:
        data = request.get_json()
        code = data.get('code', '').strip()

        if not code:
            return jsonify({
                'errors': [{'error_type': 'error', 'message': 'No code provided.', 'line': 0}],
                'total_errors': 1
            })

        errors = []
        
        # Check for syntax errors
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append({
                'error_type': 'syntax error',
                'line': e.lineno,
                'message': f"Line {e.lineno}: {e.msg}"
            })
            return jsonify({'errors': errors, 'total_errors': len(errors)})

        # Safe Execution Environment
        safe_globals = {
            '__builtins__': {
                'abs': abs, 'all': all, 'any': any, 'bin': bin, 'bool': bool,
                'bytearray': bytearray, 'bytes': bytes, 'chr': chr, 'complex': complex,
                'dict': dict, 'divmod': divmod, 'enumerate': enumerate, 'filter': filter,
                'float': float, 'format': format, 'frozenset': frozenset, 'getattr': getattr,
                'hasattr': hasattr, 'hash': hash, 'hex': hex, 'id': id, 'int': int,
                'isinstance': isinstance, 'issubclass': issubclass, 'iter': iter, 'len': len,
                'list': list, 'map': map, 'max': max, 'min': min, 'next': next, 'oct': oct,
                'ord': ord, 'pow': pow, 'range': range, 'repr': repr, 'reversed': reversed,
                'round': round, 'set': set, 'slice': slice, 'sorted': sorted, 'str': str,
                'sum': sum, 'tuple': tuple, 'type': type, 'zip': zip, 'print': print  # ✅ Fixed print issue
            }
        }
        safe_locals = {}

        # Check for runtime errors
        try:
            exec(code, safe_globals, safe_locals)
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            line_number = tb[-1].lineno if tb else 1
            errors.append({
                'error_type': 'runtime error',
                'line': line_number,
                'message': f"Line {line_number}: {str(e)}"
            })

        # If no errors, return success
        if not errors:
            errors.append({
                'error_type': 'bug-free',
                'message': 'No errors found!',
                'line': 0
            })

        return jsonify({'errors': errors, 'total_errors': len(errors) - 1 if errors[0]['error_type'] == 'bug-free' else len(errors)})

    except Exception as e:
        return jsonify({
            'errors': [{'error_type': 'internal error', 'message': str(e), 'line': 0}],
            'total_errors': 1
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
