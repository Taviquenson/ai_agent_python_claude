import os

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
        MAX_CHARS = 10000
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(f.read()) > MAX_CHARS:
                return f'{file_content_string}[...File "{file_path}" truncated at 10000 characters]'
            return file_content_string
    except Exception as e:
        return f'Error: {e}'
