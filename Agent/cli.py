import os

def start_cli():

    print("=" * 50)
    print("              Welcome to the CLI!")
    print("=" * 50)

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
            print("           exit or quit - Exit the CLI")
        elif user_input.lower() == "pwd":
            current_directory = os.getcwd()
            print(f"Agent >> Current working directory: {current_directory}")
        elif user_input.lower() == "ls":
            files_and_directories = os.listdir(os.getcwd())
            print("Agent >> Files and directories in the current directory:")
            for item in files_and_directories:
                print(f"           {item}")
        else:
            print("Agent >> Unknown command. Type 'help' for a list of available commands.")
