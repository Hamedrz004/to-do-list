import unittest
import os
import csv
from unittest.mock import patch, mock_open
from main import task, tdlist, createlist, addtolist, removefromlist, savetocsv, importfromcsv, viewlists, menue

class TestTask(unittest.TestCase):
    def test_task_creation(self):
        t = task("Test Task", "Test Description", 1)
        self.assertEqual(t.name, "Test Task")
        self.assertEqual(t.descr, "Test Description")
        self.assertEqual(t.prio, 1)

    def test_change_prio(self):
        t = task("Test Task", "Test Description", 1)
        t.change_prio(2)
        self.assertEqual(t.prio, 2)

    def test_task_str(self):
        t1 = task("High Prio Task", "Description", 1)
        t2 = task("Medium Prio Task", "Description", 2)
        t3 = task("Low Prio Task", "Description", 3)
        self.assertEqual(str(t1), "**High Prio Task: description: Description")
        self.assertEqual(str(t2), "*Medium Prio Task: description: Description")
        self.assertEqual(str(t3), "Low Prio Task: description: Description")

    def test_task_call(self):
        t = task("Test Task", "Test Description", 1)
        self.assertEqual(t(), ("Test Task", "Test Description", 1))

class TestTdList(unittest.TestCase):
    def setUp(self):
        self.tdl = tdlist("Test List")

    def test_tdlist_creation(self):
        self.assertEqual(self.tdl.name, "Test List")
        self.assertEqual(self.tdl.list, [])

    def test_add_task(self):
        self.tdl.add_task("Task 1", "Descr 1", 2)
        self.assertEqual(len(self.tdl.list), 1)
        self.assertEqual(self.tdl.list[0].name, "Task 1")

    def test_remove_task(self):
        self.tdl.add_task("Task 1", "Descr 1", 2)
        self.tdl.add_task("Task 2", "Descr 2", 1)
        self.tdl.remove_task("Task 1")
        self.assertEqual(len(self.tdl.list), 1)
        self.assertEqual(self.tdl.list[0].name, "Task 2")

    def test_sortbyprio(self):
        self.tdl.add_task("Task 1", "Descr 1", 3)
        self.tdl.add_task("Task 2", "Descr 2", 1)
        self.tdl.add_task("Task 3", "Descr 3", 2)
        self.tdl.sortbyprio()
        self.assertEqual(self.tdl.list[0].name, "Task 2")
        self.assertEqual(self.tdl.list[1].name, "Task 3")
        self.assertEqual(self.tdl.list[2].name, "Task 1")

    def test_tasks(self):
        self.tdl.add_task("Task 1", "Descr 1", 2)
        self.tdl.add_task("Task 2", "Descr 2", 1)
        self.assertEqual(self.tdl.tasks(), ["Task 1", "Task 2"])

    def test_tdlist_str(self):
        self.assertEqual(str(self.tdl), "Test List is empty")
        self.tdl.add_task("Task 1", "Descr 1", 1)
        self.tdl.add_task("Task 2", "Descr 2", 2)
        expected_str = "Test List:\n1- **Task 1: description: Descr 1\n2- *Task 2: description: Descr 2"
        self.assertEqual(str(self.tdl), expected_str)

    def test_tdlist_call(self):
        self.tdl.add_task("Task 1", "Descr 1", 1)
        self.assertEqual(self.tdl(), ("Test List", [("Task 1", "Descr 1", 1)]))

    def test_save_and_load_csv(self):
        path = "test.csv"
        self.tdl.add_task("Task 1", "Descr 1", 1)
        self.tdl.add_task("Task 2", "Descr 2", 2)
        self.tdl.save_to_csv(path)

        new_tdl = tdlist("New List")
        new_tdl.load_from_csv(path)
        self.assertEqual(len(new_tdl.list), 2)
        self.assertEqual(new_tdl.list[0].name, "Task 1")
        self.assertEqual(new_tdl.list[1].prio, 2)
        os.remove(path)

class TestInteractiveFunctions(unittest.TestCase):

    def setUp(self):
        # Reset global state for each test
        import main
        main.tlists = {}
        main.aclist = None

    @patch('builtins.input', side_effect=['Test List', ''])
    def test_createlist(self, mock_input):
        import main
        createlist()
        self.assertIn("Test List", main.tlists)
        self.assertEqual(main.aclist, "Test List")

    @patch('builtins.input', side_effect=['Task 1', 'Description 1', '1', ''])
    def test_addtolist(self, mock_input):
        import main
        main.tlists['Test List'] = tdlist('Test List')
        main.aclist = 'Test List'
        addtolist()
        self.assertEqual(len(main.tlists['Test List'].list), 1)
        self.assertEqual(main.tlists['Test List'].list[0].name, 'Task 1')

    @patch('builtins.input', side_effect=['1', ''])
    def test_removefromlist(self, mock_input):
        import main
        main.tlists['Test List'] = tdlist('Test List')
        main.aclist = 'Test List'
        main.tlists['Test List'].add_task('Task 1', 'Descr 1', 1)
        removefromlist()
        self.assertEqual(len(main.tlists['Test List'].list), 0)

    @patch('builtins.input', side_effect=['test.csv', ''])
    @patch('builtins.print')
    def test_savetocsv(self, mock_print, mock_input):
        import main
        main.tlists['Test List'] = tdlist('Test List')
        main.aclist = 'Test List'
        main.tlists['Test List'].add_task('Task 1', 'Descr 1', 1)
        savetocsv()
        self.assertTrue(os.path.exists('test.csv'))
        with open('test.csv', 'r') as f:
            reader = csv.reader(f)
            self.assertEqual(next(reader), ['Task 1', 'Descr 1', '1'])
        os.remove('test.csv')

    @patch('builtins.input', side_effect=['New List', 'test.csv', ''])
    @patch('builtins.print')
    def test_importfromcsv(self, mock_print, mock_input):
        import main
        with open('test.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Task 1', 'Descr 1', '1'])

        importfromcsv()
        self.assertIn('New List', main.tlists)
        self.assertEqual(main.aclist, 'New List')
        self.assertEqual(len(main.tlists['New List'].list), 1)
        self.assertEqual(main.tlists['New List'].list[0].name, 'Task 1')
        os.remove('test.csv')

    @patch('builtins.input', side_effect=['1', ''])
    def test_viewlists(self, mock_input):
        import main
        main.tlists['List 1'] = tdlist('List 1')
        main.tlists['List 2'] = tdlist('List 2')
        viewlists()
        self.assertEqual(main.aclist, 'List 1')

    @patch('builtins.input', side_effect=['1'])
    @patch('builtins.print')
    def test_menue_valid_input(self, mock_print, mock_input):
        self.assertEqual(menue(), 1)

    @patch('builtins.input', side_effect=['9', '0', 'abc', '1'])
    @patch('builtins.print')
    def test_menue_invalid_input(self, mock_print, mock_input):
        self.assertEqual(menue(), 1)
        self.assertEqual(mock_print.call_count, 5)

if __name__ == '__main__':
    unittest.main()
