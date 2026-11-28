from Agent.tools import execute_tool
from Agent.memory import ConversationMemory
from Agent.llm import ask_llm
import os

def start_cli():

    print("=" * 50)
    print("               Welcome to the CLI!")
    print("=" * 50)

    memory = ConversationMemory()
    max_turns = 10

    while True:
        user_input = input("\nYou >> ").strip() #.strip() removes any leading/trailing whitespace from the input

        if user_input.lower() in ["exit", "quit"]:
            print("Agent >> Exiting the CLI. Goodbye!")
            break
        elif user_input.lower() == "help":
            print("Agent >> Available commands:")
            print("           help - Show this help message")
            print("           pwd - Print the current working directory")
            print("           ls - List files and directories in the current directory")
            print("           count_files - Number of files and directories in the current directory")
            print("           exit or quit - Exit the CLI")
            print("           ask <question> - Ask the AI")
            print("           clear - Clear conversation history")
            print("           /history - extracts the stored chat history")
            print("           /context - to set the context window size like '/context 5'")
        elif user_input.lower() == "pwd":
            result = execute_tool("pwd")
            print(f"Agent >> Current working directory: {result}")
        elif user_input.lower() == "ls":
            result = execute_tool("ls")
            print("Agent >> Files and directories in the current directory:")
            for item in result:
                print(f"           {item}")
        elif user_input.lower() == "count_files":
            result = execute_tool("count_files")
            print(f"Agent >> Number of files and directories in the current directory: {result}")
        elif user_input.lower() == "clear":
            memory.clear()
            print("Agent >> Conversation cleared.")
        elif user_input.lower().startswith("/context"):
            parts = user_input.split()
            if len(parts) != 2:
                print("Agent >> Usage: /context <number>")
            else:
                try:
                    requested_turns = int(parts[1])
                    if requested_turns < 0:
                        raise ValueError
                    max_turns = requested_turns
                    print(f"Agent >> Context window set to {max_turns} turns.")
                except ValueError:
                    print("Agent >> Context must be a non-negative integer.")
        elif user_input.lower().startswith("ask "):
            prompt = user_input[4:].strip()
            if not prompt:
                print("Agent >> Please enter a question.")
                continue
            try:
                answer = ask_llm(prompt, memory, max_turns)
                print(f"Agent >> {answer}")
            except Exception as error:
                print(f"Agent >> Request failed: {error}")
        elif user_input.lower() == "ask":
            print("Agent >> Please enter a question.")
        elif user_input.lower() == "/history":
            messages = memory.get_history()
            if not messages:
                print("Agent >> No conversation history.")
            else:   
                for message in messages:
                    print(
                        f"{message.role}: "
                        f"{message.parts[0].text}"
                    )
        else:
            print("Agent >> Unknown command. Type 'help' for a list of available commands.")
