import os
from google.genai import types
from config import MAX_CHARS



def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))
    
    is_file_inside = str(abs_file_path).startswith(str(abs_working_directory))

    # print(file_path)
    # print(abs_file_path)

    try:
        if not is_file_inside:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'        
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        # read the file and return its contents as a string
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(f.read()) > MAX_CHARS:
                return f'{file_content_string}[...File "{file_path}" truncated at 10000 characters]'
            return file_content_string
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Outputs the content of the file specified by the given file_path",
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