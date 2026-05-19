import os
import subprocess
from google import genai

schema_run_python_file = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a pyhon file as a subprocess and returns a string.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The path to the file which the function intends to run.",
            ),
            "args": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                description="A list of arguments to pass to the function. Defaults to None.",
                items=genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if valid_target_dir is False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(target_file) is False:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if target_file.endswith(".py") is False:
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file]
    if args != None:
        command.extend(args)
    try:
        completed = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        return_string = []
        if completed.returncode != 0:
            return_string.append(f"Process exited with code {completed.returncode}")
        if not completed.stdout and not completed.stderr:
            return_string.append("No output produced")
        else:
            if completed.stdout:
                return_string.append(f"STDOUT: {completed.stdout}")
            if completed.stderr:
                return_string.append(f"STDERR: {completed.stderr}")
        return "\n".join(return_string)
    except Exception as e:
        return f"Error: executing Python file: {e}"