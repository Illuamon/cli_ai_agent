import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    if os.path.abspath(full_path).startswith(os.path.abspath(working_directory)) == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(full_path) == False:
        return f'Error: File "{file_path}" not found.'
    if file_path.endswith(".py") == False:
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        file_output = subprocess.run(["uv", "run", file_path, *args], capture_output=True, timeout=30, text=True, cwd=working_directory)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    output = []
    if file_output.stdout:
        output.append(f"STDOUT:\n{file_output.stdout}")
    if file_output.stderr:
        output.append(f"STDERR:\n{file_output.stderr}")
    if file_output.returncode != 0:
        output.append(f"Process exited with code {file_output.returncode}")

    return "\n".join(output) if output else "No output produced."


    
