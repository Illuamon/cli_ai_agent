import os 
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)

        #check if desired dir is permitted to dig in for the ai
        if os.path.abspath(full_path).startswith(os.path.abspath(working_directory)) == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        #check if the dir is really a dir
        if os.path.isdir(full_path) == False:
            return f'Error: "{directory}" is not a directory'

        #build the output string 
        contents = os.listdir(full_path)
        output_list = []
        for item in contents:
            path_to_item = os.path.join(full_path, item)
            size = os.path.getsize(path_to_item)
            is_dir = os.path.isdir(path_to_item)
            output = f"- {item}: file_size={size}, is_dir={is_dir}"
            output_list.append(output)
        
        return "\n".join(output_list)

    except Exception as e:
        return f"Error: {e}"
    
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

    