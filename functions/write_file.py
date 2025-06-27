import os

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))
    
    is_file_inside = str(abs_file_path).startswith(str(abs_working_directory))
    try:
        f_dirname = os.path.dirname(abs_file_path)
        if not is_file_inside:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(f_dirname):
            os.makedirs(f_dirname)
            with open(abs_file_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        else: # overwrite file contents with `content`
            with open(abs_file_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'