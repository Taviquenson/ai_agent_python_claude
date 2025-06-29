import os, subprocess
from google.genai import types


def run_python_file(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))
    
    is_file_inside = str(abs_file_path).startswith(str(abs_working_directory))
    try:
        if not is_file_inside:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not str(file_path).endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
    except Exception as e:
        return f'Error: {e}'
    
    try:
        result = subprocess.run(["python3", file_path], timeout=30, capture_output=True, text=True, cwd=working_directory)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if len(result.stdout) == 0 and len(result.stderr) == 0:
            return f"No output produced."
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs the Python file specified by the given file_path",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path that indicates where to find the file",
                ),
            },
        ),
    )