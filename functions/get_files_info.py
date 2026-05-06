import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if valid_target_dir == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if os.path.isdir(target_dir) == False:
        return f'Error: "{directory}" is not a directory'
    
    try:
        dir_info = []
        for item in os.listdir(target_dir):
            dir_info.append(f"- {item}: file_size={os.path.getsize(os.path.join(target_dir, item))}, is_dir={os.path.isdir(os.path.join(target_dir, item))}")
        full_dir_info = "\n".join(dir_info)
        return full_dir_info
    except Exception as e:
        return f"Error: {e}"