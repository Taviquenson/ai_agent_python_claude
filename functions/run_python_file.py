import os, subprocess

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
        result = subprocess.run(["python3", file_path], timeout=30, capture_output=True, cwd=working_directory)
        stdout_str = result.stdout.decode('utf-8')
        stderr_str = result.stderr.decode('utf-8')
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if len(stdout_str) == 0 and len(stderr_str):
            return f"No output produced."
        return f"STDOUT:\n{stdout_str}\nSTDERR:\n{stderr_str}"
    except Exception as e:
        return f"Error: executing Python file: {e}"