import os

def get_current_directory():
    return os.getcwd()

def list_files_and_directories():
    return os.listdir()

def count_files():
    return len(os.listdir())

TOOLS = {
    "pwd": get_current_directory,
    "ls": list_files_and_directories,
    "count_files": count_files
}

def execute_tool(tool_name):
    if tool_name not in TOOLS:
        return "Unknown tool"
    tool_function = TOOLS[tool_name]
    result = tool_function()
    return result