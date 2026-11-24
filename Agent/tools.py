import os
import json

def get_current_directory():
    return os.getcwd()

def list_files_and_directories(directory="."):
    return os.listdir(directory)

def count_files(directory="."):
    return len(os.listdir(directory))

TOOLS = {
    "pwd": get_current_directory,
    "ls": list_files_and_directories,
    "count_files": count_files
}

def execute_tool(tool_name,arguments=None):
    if tool_name not in TOOLS:
        return "Unknown tool"
    if arguments is None:
        arguments = {}
    tool_function = TOOLS[tool_name]
    try:
        result = tool_function(**arguments)
        return result
    except (FileNotFoundError, NotADirectoryError) as error:
        return f"File system error: {error}"
    except TypeError as error:
        return f"Invalid tool arguments: {error}"

def execute_json_tool(json_request):
    try:
        request = json.loads(json_request)
    except json.JSONDecodeError as error:
        return f"Invalid JSON: {error}"
    if not isinstance(request, dict):
        return "Invalid request: Expected a JSON object"
    tool_name = request.get("name")
    arguments = request.get("arguments", {})
    if not isinstance(tool_name, str):
        return "Invalid request: Tool name must be a string"

    if not isinstance(arguments, dict):
        return "Invalid request: Arguments must be a dictionary"
    return execute_tool(tool_name, arguments)