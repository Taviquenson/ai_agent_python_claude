import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    if directory == None:
        directory = working_directory
    abs_working_directory = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(abs_working_directory, directory))
    # print(abs_working_directory)
    # print(abs_directory)

    is_dir_inside = str(abs_directory).startswith(str(abs_working_directory))
    # print(is_dir_inside)

    try:
        if not is_dir_inside:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'

        directory_content = os.listdir(abs_directory)
    except Exception as e:
        return f'Error: {e}'

    str_dir_cntnt = []
    # print(directory_content)
    for file in directory_content:
        abs_file = os.path.join(abs_directory, file)
        str_dir_cntnt.append(f"- {file}: file_size={os.path.getsize(abs_file)} bytes, is_dir={os.path.isdir(abs_file)}")
    try:
        return '\n'.join(str_dir_cntnt)
    except Exception as e:
        return f'Error: {e}'

schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )