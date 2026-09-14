"""Tests for the todo list CLI."""

import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import app


class TodoListTests(unittest.TestCase):
    def setUp(self):
        app.get_todos().clear()
        self.temp_directory = tempfile.TemporaryDirectory()
        self.todos_file = Path(self.temp_directory.name) / "todos.csv"
        self.file_patch = patch.object(app, "TODOS_FILE", self.todos_file)
        self.file_patch.start()

    def tearDown(self):
        self.file_patch.stop()
        self.temp_directory.cleanup()

    def test_add_multiple_tasks(self):
        app.add_one_task("Make the bed")
        app.add_one_task("Make lunch")
        app.add_one_task("Clean kitchen")

        self.assertEqual(
            app.get_todos(),
            ["Make the bed", "Make lunch", "Clean kitchen"],
        )

    def test_print_list_uses_one_based_positions(self):
        app.add_one_task("Check delivery")
        app.add_one_task("Call warehouse")
        output = io.StringIO()

        with redirect_stdout(output):
            app.print_list()

        self.assertIn("1. Check delivery", output.getvalue())
        self.assertIn("2. Call warehouse", output.getvalue())

    def test_delete_task_uses_displayed_position(self):
        app.get_todos().extend(["Make the bed", "Make lunch", "Clean kitchen"])

        self.assertTrue(app.delete_task(2))

        self.assertEqual(app.get_todos(), ["Make the bed", "Clean kitchen"])

    def test_delete_task_rejects_invalid_positions(self):
        app.add_one_task("Keep this task")

        self.assertFalse(app.delete_task("not a number"))
        self.assertFalse(app.delete_task(0))
        self.assertFalse(app.delete_task(2))
        self.assertEqual(app.get_todos(), ["Keep this task"])

    def test_save_todos_writes_one_csv_row_per_task(self):
        expected = ["Call driver, route 4", "Confirm morning pickup"]
        app.get_todos().extend(expected)

        app.save_todos()

        with self.todos_file.open(newline="", encoding="utf-8") as file:
            self.assertEqual([row[0] for row in csv.reader(file)], expected)

    def test_load_todos_replaces_current_tasks(self):
        with self.todos_file.open("w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerows([["jump"], ["run"], ["roll"]])
        app.add_one_task("Old task")

        self.assertTrue(app.load_todos())

        self.assertEqual(app.get_todos(), ["jump", "run", "roll"])

    def test_load_missing_file_keeps_current_tasks(self):
        app.add_one_task("Unsaved task")

        self.assertFalse(app.load_todos())

        self.assertEqual(app.get_todos(), ["Unsaved task"])


if __name__ == "__main__":
    unittest.main()
