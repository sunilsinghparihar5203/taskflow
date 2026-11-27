import unittest
from datetime import date

from taskflow.domain import Task, parse_task, summarize_tasks_by_status


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

    def test_summarize_empty_tasks_includes_every_state(self) -> None:
        self.assertEqual(
            summarize_tasks_by_status([]),
            {"todo": 0, "in_progress": 0, "done": 0},
        )

    def test_summarize_mixed_tasks_includes_zero_counts(self) -> None:
        tasks = [
            Task(id="task-1", title="Write tests", state="todo"),
            Task(id="task-2", title="Review changes", state="todo"),
            Task(id="task-3", title="Ship release", state="done"),
        ]

        self.assertEqual(
            summarize_tasks_by_status(tasks),
            {"todo": 2, "in_progress": 0, "done": 1},
        )

    def test_valid_state_change(self) -> None:
        task = Task(id="task-1", title="Write tests", state="todo")

        task.change_state("in_progress")

        self.assertEqual(task.state, "in_progress")

    def test_parse_valid_record(self) -> None:
        task = parse_task({
            "id": "task-1",
            "title": "Write tests",
            "status": "todo",
            "due_date": "2026-11-25",
        })

        self.assertEqual(task.id, "task-1")
        self.assertEqual(task.title, "Write tests")
        self.assertEqual(task.state, "todo")
        self.assertEqual(task.due_date, date(2026, 11, 25))

    def test_parse_record_without_optional_due_date(self) -> None:
        task = parse_task({
            "id": "task-1",
            "title": "Write tests",
            "status": "todo",
        })

        self.assertIsNone(task.due_date)

    def test_parse_missing_required_field(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing required field: status"):
            parse_task({"id": "task-1", "title": "Write tests"})

    def test_parse_unsupported_status(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported task status"):
            parse_task({
                "id": "task-1",
                "title": "Write tests",
                "status": "paused",
            })

    def test_parse_blank_title(self) -> None:
        with self.assertRaisesRegex(ValueError, "title must not be empty"):
            parse_task({
                "id": "task-1",
                "title": "   ",
                "status": "todo",
            })

    def test_parse_invalid_due_date(self) -> None:
        with self.assertRaisesRegex(ValueError, "due_date must be a valid date"):
            parse_task({
                "id": "task-1",
                "title": "Write tests",
                "status": "todo",
                "due_date": "not-a-date",
            })


if __name__ == "__main__":
    unittest.main()
