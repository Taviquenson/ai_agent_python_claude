import os
from google.genai import types


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
    
schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Overwrites the contents of the file found in the specified file_path with the value of argument content. And if the file doesn't exist, it creates it and writes the value of argument content in it",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path that indicates where to find the file to be overwritten. Or where to create and write the file with the value of argument content if the file doesn't exist.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="This is the information that will overwritte the current content of the file from the file path. Or the information that will be written in a newly created file at the file path",
                ),
            },
        ),
    )