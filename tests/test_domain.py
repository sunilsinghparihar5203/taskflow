import unittest

from taskflow.domain import Task


class TaskTests(unittest.TestCase):
    def test_valid_title_creates_task(self) -> None:
        task = Task(id="task-1", title="Write tests", state="todo")

        self.assertEqual(task.title, "Write tests")
        self.assertEqual(task.state, "todo")

    def test_blank_or_whitespace_title_is_rejected(self) -> None:
        for title in ("", " \t\n "):
            with self.subTest(title=title):
                with self.assertRaises(ValueError):
                    Task(id="task-1", title=title, state="todo")

    def test_valid_state_change(self) -> None:
        task = Task(id="task-1", title="Write tests", state="todo")

        task.change_state("in_progress")

        self.assertEqual(task.state, "in_progress")


if __name__ == "__main__":
    unittest.main()
