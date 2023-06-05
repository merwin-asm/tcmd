import os
import collections
from rich.console import Console
from rich.table import Table
from rich import box



# Create a console object
console = Console()

# Get the user's command history
def get_command_history():
    history = []
    
    if os.name == "posix":  # For Linux and macOS
        history_file = os.path.expanduser("~/.bash_history")
        with open(history_file, "r") as file:
            history = file.readlines()

    elif os.name == "nt":  # For Windows
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\CommandStore\\Recent\\")
        for i in range(winreg.QueryInfoKey(key)[1]):
            history.append(winreg.EnumValue(key, i)[1])

    return history

# Count the frequency of commands
def count_commands(history):
    counter = collections.Counter(history)
    return counter.most_common(10)

# Main function
def main():
    # Get command history
    command_history = get_command_history()

    # Count the frequency of commands
    top_commands = count_commands(command_history)

    # Create a table
    table = Table(show_header=True, header_style="bold magenta", box=box.MINIMAL_HEAVY_HEAD)
    table.add_column("Rank", style="cyan", justify="center")
    table.add_column("Command", style="green", justify="left")
    table.add_column("Count", style="yellow", justify="center")

    # Add data to the table
    for rank, (command, count) in enumerate(top_commands, start=1):
        rank_emoji = f"🥇 {rank}" if rank == 1 else f"🥈 {rank}" if rank == 2 else f"🥉 {rank}" if rank == 3 else f"🎖️  {rank}"
        if count < 100:
            table.add_row(rank_emoji, command.strip(), f"{count}  📈")
        else:
            table.add_row(rank_emoji, command.strip(), f"{count} 📈")

    # Print the table
    console.print(table)

if __name__ == "__main__":
    main()
