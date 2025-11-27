import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        if os.path.abspath(full_path).startswith(os.path.abspath(working_directory)) == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isfile(full_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(full_path, "r") as f:
            file_content = f.read(MAX_CHARS)
            file_content += f"[...File '{file_path}' truncated at 10000 characters]"
            return file_content
    except Exception as e:
        return f"Error: {e}"
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file (limited to first 10000 characters), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read from, relative to the working directory.",
            ),
        },
    ),
)    

