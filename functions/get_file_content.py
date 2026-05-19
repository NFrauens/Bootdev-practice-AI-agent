import os
from config import CHAR_LIMIT #10000
from google import genai

schema_get_file_content = genai.types.FunctionDeclaration(
    name="get_file_content",
    description="Fetches a text files content up to a pre-determined character limit.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The path to the file that the function is fetching content from.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if valid_target_dir == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(target_file) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file, "r") as f:
            content = f.read(CHAR_LIMIT)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {CHAR_LIMIT} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"