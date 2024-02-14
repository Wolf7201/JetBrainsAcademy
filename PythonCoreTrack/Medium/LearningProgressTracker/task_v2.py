import re


class DataIsNotValid(Exception):
    pass


class EmailIsTaken(Exception):
    pass


class Student:
    """
    Класс для управления информацией о студенте и его учебных баллах.

    Позволяет создать объект студента с именем, фамилией и электронной
    почтой, а также управлять баллами по разным курсам.

    При создании объекта происходит валидация имени, фамилии и
    электронной почты. Для добавления баллов используется метод add_points.

    Пример использования:
    student = Student("Иван", "Иванов", "ivan.ivanov@example.com")
    student.add_points("10 20 30 40")

    Имя, фамилия и email должны соответствовать определенным
    форматам валидации.
    """

    id_counter = 1000
    name_pattern = (r"^(?![A-Za-z]*['-]{2})[A-Za-z][ '-]"
                    r"?[A-Za-z]+(?:[ '-][A-Za-z]+)*$")
    email_pattern = (r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]"
                     r"+\.[a-zA-Z0-9]{1,}$")
    students = {}
    emails = set()

    def __init__(self, first_name: str, last_name: str,
                 email: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.courses = Course.courses
        self.id = Student.id_counter

        if not self._is_valid_first_name():
            raise DataIsNotValid("Incorrect first name")
        elif not self._is_valid_last_name():
            raise DataIsNotValid("Incorrect last name")
        elif not self._is_valid_email():
            raise DataIsNotValid("Incorrect email")
        elif self.email in self.emails:
            raise EmailIsTaken("This email is already taken.")

        self.points = {name: 0 for name in self.courses}
        self.students[self.id_counter] = self
        self.emails.add(email)
        Student.id_counter += 1

    def _is_valid_first_name(self) -> bool:
        """Проверяет валидность имени студента."""
        return re.match(self.name_pattern, self.first_name) is not None

    def _is_valid_last_name(self) -> bool:
        """Проверяет валидность фамилии студента."""
        return re.match(self.name_pattern, self.last_name) is not None

    def _is_valid_email(self) -> bool:
        """Проверяет валидность электронной почты студента."""
        return re.match(self.email_pattern, self.email) is not None

    def _is_valid_points(self, input_list: list[str]) -> bool:
        """
        Проверяет валидность списка баллов.

        1. Балл - неотрицательное число.
        2. Количество баллов равно количеству курсов.
        """
        return (all(num.isdigit() and int(num) >= 0 for num in input_list)
                and len(input_list) == len(self.points))

    def add_points(self, input_string: str) -> None:
        """
        Добавляет баллы к курсам студента.
        Отправляет данные о студенте в курсы.
        Если баллы не валидны, возвращает ошибку.
        """
        courses_list = list(self.points)
        input_list = input_string.split()
        if self._is_valid_points(input_list):
            points = list(map(int, input_list))
            for i in range(len(courses_list)):
                course = courses_list[i]
                # Добавляем баллы пользователю.
                self.points[course] += points[i]
                # Отправляем данные в курс.
                self.courses[course].update(self, points[i])
            print("Points updated.")
        else:
            raise DataIsNotValid("Incorrect points format.")

    def get_student_score(self) -> str:
        """Отдает строку с баллами студента в курсах."""
        result_str = f'{self.id} points:'
        for course, points in self.points.items():
            result_str += f' {course}={points};'
        return result_str.rstrip(";")

    @staticmethod
    def get_students_id() -> str:
        """Отдает в консоль список id студентов."""
        if Student.students:
            answer = "Students:\n"
            for key in Student.students.keys():
                answer += f'{key}\n'
            return answer.rstrip()
        else:
            return "No students found"


class Course:
    courses = {}

    def __init__(self, name: str, passing_scores: int) -> None:
        self.name = name
        self.passing_scores = passing_scores
        self.completed_tasks = 0
        self.all_score = 0
        self.student_scores = {}
        self.completed_course = []
        self.courses[name] = self

    def update(self, student: Student, points: int) -> None:
        """Обновление данных курса."""
        if points == 0:
            return

        self.student_scores[student.id] = (
                self.student_scores.get(student.id, 0) + points
        )
        self.completed_tasks += 1
        self.all_score += points

        # Если балов студентов достаточно для окончания курса,
        # добавляем его в список для выпуска курса.
        if self.student_scores[student.id] >= self.passing_scores:
            self.completed_course.append(student)

    def get_average_score(self) -> float:
        """
        Если есть данные о выполненных задачах, возвращает
        средний балл выполненных задач.
        """
        if self.completed_tasks == 0:
            return 0
        return self.all_score / self.completed_tasks

    def get_top_students(self) -> str:
        """Получаем отсортированных студентов курса."""
        # Сортируем студентов по баллам (по убыванию),
        # а при равенстве баллов - по ID (по возрастанию)
        sorted_students = sorted(
            self.student_scores.items(), key=lambda x: (-x[1], x[0])
        )

        result_str = f"{self.name}\nid  points completed\n"
        for student_id, points in sorted_students:
            completion_rate = (points / self.passing_scores) * 100
            result_str += f"{student_id} {points}    {completion_rate:.1f}%\n"
        # Удаляем последний перенос строки для красоты вывода
        return result_str.rstrip()

    def get_completed_student_data(self) -> tuple[str, list[int]]:
        """
        Получаем строку с сообщениями для студентов
        окончивших курс и список этих студентов.
        """
        students = self.completed_course.copy()
        self.completed_course.clear()
        message = ''

        for student in students:
            full_name = f'{student.first_name} {student.last_name}'

            message += (f'To: {student.email}\n'
                        f'Re: Your Learning Progress\n'
                        f'Hello, {full_name}! '
                        f'You have accomplished our {self.name} course!\n')

        return message, students


class TrackerStatistics:
    """Класс для расчета метрик курсов."""

    @staticmethod
    def _calculate_by_criteria(criteria_func) -> tuple[list[str], list[str]]:
        """
        Метод для расчета статистики по критериям.
        Возвращает кортеж из двух списков: курсы с максимальным
        и минимальным значениями по заданному критерию.
        """
        criteria_results = {name: criteria_func(course)
                            for name, course in Course.courses.items()
                            if criteria_func(course) > 0}

        if not criteria_results:
            return ["n/a"], ["n/a"]

        max_value = max(criteria_results.values())
        min_value = min(criteria_results.values())

        most_criteria = [name for name, value in criteria_results.items()
                         if value == max_value]
        least_criteria = [name for name, value in criteria_results.items()
                          if value == min_value]

        if most_criteria == least_criteria:
            return most_criteria, ["n/a"]

        return most_criteria, least_criteria

    # Пример использования обновленного
    # метода для популярности, активности и сложности
    def get_statistic(self) -> str:
        """
        Метод для получения развернутой статистике по курсам.
        Метод расчитывает лучшие и худшие курсы по категориям.
        """
        # Расчет популярности на основании количества студентов.
        popularity = self._calculate_by_criteria(
            lambda course: len(course.student_scores)
        )

        # Расчет активности на основании количества выполненных заданий.
        activity = self._calculate_by_criteria(
            lambda course: course.completed_tasks
        )

        # Расчет сложности на основании среднего балла выполненных заданий.
        difficulty = self._calculate_by_criteria(
            lambda course: course.get_average_score()
        )

        return (
            f'Most popular: {", ".join(popularity[0])}\n'
            f'Least popular: {", ".join(popularity[1])}\n'
            f'Highest activity: {", ".join(activity[0])}\n'
            f'Lowest activity: {", ".join(activity[1])}\n'
            f'Easiest course: {", ".join(difficulty[0])}\n'
            f'Hardest course: {", ".join(difficulty[1])}'
        )


class LearningProgressTracker:
    """
    Класс для отслеживания учебного прогресса студентов.

    Этот класс позволяет добавлять студентов, управлять их очками
    и просматривать информацию о них.

    Основные методы:
    - start(): Запускает цикл обработки команд пользователя.
    """

    def __init__(self):
        self.running = True
        self.commands = {
            "exit": self._exit_command,
            "add students": self._student_manager,
            "list": lambda: print(Student.get_students_id()),
            "add points": self._add_student_points,
            "find": self._get_student_points,
            "statistics": self._statistics,
            "notify": self._generate_notifications,
        }

    def start(self) -> None:
        """Запускает программу, принимает команды для исполнения."""
        print("Learning Progress Tracker")

        while self.running:
            try:
                command = input().strip()
                if command == "back":
                    print("Enter 'exit' to exit the program.")
                elif command:
                    self.commands[command]()
                else:
                    raise ValueError("No input.")
            except KeyError:
                print("Error: unknown command!")
            except ValueError as e:
                print(e)

    def _exit_command(self) -> None:
        """Изменяет флаг для выхода из программы."""
        self.running = False
        print("Bye!")

    @staticmethod
    def _student_manager() -> None:
        """
        Принимает данные студента или команду back.
        Разделяет строку с данными студента.

        Создает студента.
        """
        print("Enter student credentials or 'back' to return: ")
        student_count = 0
        while True:

            data = input()
            space_count = data.count(' ')

            if data == "back":
                print(f"Total {student_count} students have been added.")
                break

            elif space_count >= 2:
                # Используем rsplit для разделения с конца строки email.
                parts = data.rsplit(' ', 1)
                full_name = parts[0]
                email = parts[1].strip()

                # Разделяем полное имя на имя и фамилию
                name_parts = full_name.split(' ', 1)
                first_name = name_parts[0].strip()
                last_name = name_parts[1].strip()

                try:
                    Student(first_name, last_name, email)

                    student_count += 1
                    print("The student has been added.")

                except (DataIsNotValid, EmailIsTaken) as e:
                    print(e)

            else:
                print("Incorrect credentials")

    @staticmethod
    def _add_student_points() -> None:
        """
        Добавление баллов пользователя.
        Если данные не валидны, выводит в консоль ошибку.
        """
        print("Enter an id and points or 'back' to return:")
        while True:
            input_string = input()
            if input_string == "back":
                break

            parts = input_string.split(' ', 1)
            student_id, points = parts[0], parts[1]

            try:
                if student_id.isdigit() and Student.students.get(int(student_id)):
                    student = Student.students.get(int(student_id))
                    student.add_points(points)
                else:
                    print(f'No student is found for id={student_id}')
            except DataIsNotValid as e:
                print(e)

    @staticmethod
    def _get_student_points() -> None:
        """Выводит данные баллов определенного пользователя."""
        print("Enter an id or 'back' to return")
        while True:
            str_input = input()
            if str_input == "back":
                break
            elif str_input.isdigit() and Student.students.get(int(str_input)):
                student = Student.students.get(int(str_input))
                print(student.get_student_score())
            else:
                print(f"No student is found for id={str_input}")

    @staticmethod
    def _statistics() -> None:
        """
        Выводит общую статистику по курсам,
        и лучших учениках по определённому курсу.
        """
        tracker_statistics = TrackerStatistics()
        print("Type the name of a course to see details or 'back' to quit:")
        print(tracker_statistics.get_statistic())

        # Создаем копию словаря со значениями в нижнем регистре,
        # чтобы команды от регистра не зависели.
        courses_lower = {key.lower(): value
                         for key, value in Course.courses.items()}
        while True:
            str_input = input()
            if str_input == "back":
                break
            # Проверка наличие команды в нижнем регистре в словаре.
            elif str_input.lower() in courses_lower:
                course = str_input.lower()
                print(courses_lower[course].get_top_students())
            else:
                print("Unknown course.")

    @staticmethod
    def _generate_notifications() -> None:
        """
        Генерация и вывод в консоль сообщений для студентов
        закончивших курс на основании количества баллов.
        """

        message = ''
        students = []

        for course in Course.courses.values():
            course_msg, student = course.get_completed_student_data()
            message += course_msg
            students.extend(student)
        student_count = len(set(students))
        # Обрезаем в конце знак переноса, чтобы
        # не было переноса строки.
        print(message.rstrip())
        print(f"Total {student_count} students have been notified.")


def main():
    courses_points = {
        "Python": 600,
        "DSA": 400,
        "Databases": 480,
        "Flask": 550,
    }

    for name, score in courses_points.items():
        Course(name, score)

    tracker = LearningProgressTracker()
    tracker.start()


if __name__ == '__main__':
    main()
