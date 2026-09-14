# Todo List CLI with Python

A lightweight command-line task manager for adding, listing, deleting, saving,
and loading daily tasks. Tasks are kept in memory while the program runs and
can be persisted to `todos.csv` between sessions.

The project uses only Python's standard library.

## Run the application

Python 3 is required. From the project directory, run:

```bash
python3 app.py
```

Choose a numbered menu option. List positions begin at `1`; use the position
shown by option 3 when deleting a task.

Saving creates `todos.csv` in the current directory. Loading replaces the
current in-memory list with the tasks in that file.

## Run the tests

```bash
python3 test.py
```

The tests cover adding multiple tasks, numbered output, deletion, invalid
positions, CSV round trips, and missing-file behavior.
