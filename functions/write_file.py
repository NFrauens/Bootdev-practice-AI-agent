import os
from google import genai

schema_write_file = genai.types.FunctionDeclaration(
    name="write_file",
    description="Writes text to a file which eiter exists or is made with this funciton.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The path to the file which the function intends to write to.",
            ),
            "content": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The content that the function will write to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if valid_target_dir == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(target_file) == True:
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    try:
        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"