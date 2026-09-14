"""A small command-line todo list with CSV persistence."""

import csv
from pathlib import Path


TODOS_FILE = Path("todos.csv")
todos = []
stop = False


def get_todos():
    """Return the active in-memory todo list."""
    return todos


def add_one_task(title):
    """Append one task title to the active list."""
    todos.append(title)


def print_list():
    """Print every task with its one-based list position."""
    if not todos:
        print("The todo list is empty.")
        return

    print("Current tasks:")
    for position, title in enumerate(todos, start=1):
        print(f"{position}. {title}")


def delete_task(number_to_delete):
    """Delete a task using its one-based list position."""
    try:
        position = int(number_to_delete)
    except (TypeError, ValueError):
        print("Please enter a valid task number.")
        return False

    if position < 1 or position > len(todos):
        print("That task number does not exist.")
        return False

    removed_title = todos.pop(position - 1)
    print(f'Removed: "{removed_title}"')
    return True


def save_todos():
    """Write the active task list to todos.csv."""
    with TODOS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        for title in todos:
            writer.writerow([title])


def load_todos():
    """Replace the active list with tasks from todos.csv."""
    try:
        with TODOS_FILE.open("r", newline="", encoding="utf-8") as file:
            loaded_todos = [row[0] for row in csv.reader(file) if row]
    except FileNotFoundError:
        print("No saved todo list was found.")
        return False

    todos.clear()
    todos.extend(loaded_todos)
    return True


def main():
    """Run the interactive command-line menu."""
    global stop
    stop = False

    while not stop:
        print(
            """
Choose an option:
1. Add one task
2. Delete a task
3. Print the current list of tasks
4. Save todos to todos.csv
5. Load todos from todos.csv
6. Exit
"""
        )

        try:
            response = input("Option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting todo list.")
            break

        if response == "1":
            title = input("What is your task title? ").strip()

            if title:
                add_one_task(title)
                print(f'Added: "{title}"')
            else:
                print("A task title cannot be empty.")

        elif response == "2":
            print_list()
            number_to_delete = input(
                "What task number do you want to delete? "
            )
            delete_task(number_to_delete)

        elif response == "3":
            print_list()

        elif response == "4":
            save_todos()
            print("Todos saved to todos.csv.")

        elif response == "5":
            if load_todos():
                print("Todos loaded from todos.csv.")

        elif response == "6":
            stop = True
            print("Goodbye!")

        else:
            print("Invalid option. Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
