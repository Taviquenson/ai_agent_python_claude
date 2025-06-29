from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from config import WORKING_DIR


available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")
    

    functions_dict = {
        "get_files_info": get_files_info,
        "get_file_content" : get_file_content,
        "run_python_file" : run_python_file,
        "write_file" : write_file,
    }

    # manually add the `working_directory`` argument to the dictionary of keyword arguments
    function_call_part.args["working_directory"] = "./calculator"

    try:
        function_result = functions_dict[function_name](**function_call_part.args)
    except KeyError as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    # Might need to return another types.Content ?
    # except Exception as e:
    #     print(f"Error encountered: {e}")

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )