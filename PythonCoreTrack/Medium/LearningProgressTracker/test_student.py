import unittest
from PythonCoreTrack.Medium.LearningProgressTracker.task import (
    Student, FirstNameIsNotValid, LastNameIsNotValid, EmailIsNotValid, PointsIsNotValid
)


class TestStudent(unittest.TestCase):

    def test_valid_student_creation(self):
        """Проверка успешного создания студента с корректными данными."""
        student = Student("Ivan", "Ivanov", "ivan@example.com")
        self.assertEqual(student.first_name, "Ivan")
        self.assertEqual(student.last_name, "Ivanov")
        self.assertEqual(student.email, "ivan@example.com")

    def test_invalid_first_name(self):
        """Проверка создания студента с некорректным именем."""
        with self.assertRaises(FirstNameIsNotValid):
            Student("Ivan2", "Ivanov", "ivan@example.com")

    def test_invalid_last_name(self):
        """Проверка создания студента с некорректной фамилией."""
        with self.assertRaises(LastNameIsNotValid):
            Student("Ivan", "Ivanov2", "ivan@example.com")

    def test_invalid_email(self):
        """Проверка создания студента с некорректным email."""
        with self.assertRaises(EmailIsNotValid):
            Student("Ivan", "Ivanov", "ivanexample.com")

    def test_add_valid_points(self):
        """Проверка добавления корректных баллов студенту."""
        student = Student("Ivan", "Ivanov", "ivan@example.com")
        student.add_points("10 20 30 40")
        self.assertEqual(student.points["Python"], 10)
        self.assertEqual(student.points["DSA"], 20)
        self.assertEqual(student.points["Databases"], 30)
        self.assertEqual(student.points["Flask"], 40)

    def test_add_invalid_points_format(self):
        """Проверка добавления баллов в некорректном формате."""
        student = Student("Ivan", "Ivanov", "ivan@example.com")
        with self.assertRaises(PointsIsNotValid):
            student.add_points("10 20 -30 40")

    def test_add_invalid_points_count(self):
        """Проверка добавления некорректного количества баллов."""
        student = Student("Ivan", "Ivanov", "ivan@example.com")
        with self.assertRaises(PointsIsNotValid):
            student.add_points("10 20 30")


if __name__ == "__main__":
    unittest.main()
