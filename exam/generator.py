from collections import defaultdict

import numpy as np
from django.contrib.auth.models import User

from exam.models import TestTask, ChoiceTestTask

np.random.seed()

BASE_LATEX_BEGIN = ""
BASE_LATEX_END = ""
GROUP_BEGIN = """\\begin{tcbraster}[raster columns=2, raster rows=2, raster height=\\textheight,
    enhanced, sharp corners, raster column skip=-.5mm,
    raster row skip=-.5mm, colback=white,
    title={\\thetcbrasternum}.,
    colbacktitle=white, coltitle=black]
"""
GROUP_END = "\\end{tcbraster}"
PAGE_BEGIN = "\\begin{tcolorbox}[title = \\thetcbrasternum. "
PAGE_END = "\\end{tcolorbox}"


class LatexCreator:
    def __init__(self, test=None, student_test=None):
        self.test = test
        self.student_test = student_test
        if test is None and student_test is None:
            raise Exception("You should provide test or student_test")
        self.groups = self.test.groups if self.test is not None else len(self.student_test.students.all())
        self.name = self.test.name if self.test is not None else self.student_test.name
        self.date = self.test.date if self.test is not None else self.student_test.date
        self.stage_title = self.test.stage.title if self.test is not None else self.student_test.stage.title

    def generate_tests(self, solution: bool = False) -> str:
        test_latex = BASE_LATEX_BEGIN
        for group_number in range(1, self.groups+1):
            test_latex += GROUP_BEGIN
            test_latex += self._generate_heading(group_number)
            test_latex += self._generate_tasks(group_number, solution)
            test_latex += GROUP_END
        return test_latex

    def _generate_tasks(self, group_number: int, solution: bool) -> str:
        tasks_latex = ""
        if self.test is not None:
            choice_tasks = ChoiceTestTask.objects.filter(test_id=self.test.id).all()
            choice_tasks_dict = {choice_task.page: choice_task for choice_task in choice_tasks}
            for page in range(2, max(choice_tasks_dict.keys())+1):
                if choice_tasks_dict.get(page) is not None:
                    tasks_latex += self._generate_choice_task(choice_tasks_dict.get(page), group_number, solution)
                else:
                    tasks_latex += (PAGE_BEGIN + "]" + PAGE_END)
        else:
            tasks = TestTask.objects.filter(student_test_id=self.student_test.id).all()
            tasks_dict = {task.page: task for task in tasks}
            for page in range(2, max(tasks_dict.keys())+1):
                if tasks_dict.get(page) is not None:
                    tasks_latex += self._generate_single_task(tasks_dict.get(page), group_number, solution)
                else:
                    tasks_latex += (PAGE_BEGIN + "]" + PAGE_END)
        return tasks_latex

    def _generate_choice_task(self, choice_task: ChoiceTestTask, group_number: int, solution: bool) -> str:
        task_latex = PAGE_BEGIN + choice_task.skill.title + " -- Wybierz i zrób przynajmniej jedno zadanie]"
        tasks = TestTask.objects.filter(choice_test_task__id=choice_task.pk)
        tasks = sorted(tasks, key=lambda t: t.skill_level.level)
        for task in tasks:
            task_latex += self._generate_task(task, group_number, solution)
        task_latex += PAGE_END
        return task_latex

    def _generate_task(self, test_task: TestTask, group_number: int, solution: bool) -> str:
        task_latex = "\\textbf{Poziom " + test_task.skill_level.level + "} \n "
        if test_task.generate_all:
            task_latex += "\\begin{enumerate} \n "
            for generator in test_task.generators.all().order_by("id"):
                try:
                    exec(generator.code)
                    if eval("len(tasks)") < group_number:
                        group_number = group_number % eval("len(tasks)")
                    task_latex += "\\item "
                    if solution:
                        task_latex += str(eval(f"answers[{group_number}]"))
                    else:
                        task_latex += str(eval(f"tasks[{group_number}]"))
                    task_latex += " \n"
                except Exception as e:
                    print(e)
            task_latex += "\\end{enumerate} \n "
        else:
            generators = test_task.generators.all().order_by("id")
            n_generators = len(generators)
            generator_num = group_number % n_generators
            version_from_generator = group_number // n_generators
            try:
                exec(generators[generator_num].code)
                if eval("len(tasks)") < version_from_generator:
                    version_from_generator = version_from_generator % eval("len(tasks)")
                if solution:
                    task_latex += str(eval(f"answers[{version_from_generator}]"))
                else:
                    task_latex += str(eval(f"tasks[{version_from_generator}]"))
            except Exception as e:
                print(e)

        return task_latex

    def _generate_single_task(self, test_task: TestTask, group_number: int, solution: bool) -> str:
        task_latex = PAGE_BEGIN + test_task.skill_level.skills.first().title + " ]"
        task_latex += self._generate_task(test_task, group_number, solution)
        task_latex += PAGE_END
        return task_latex

    def _generate_heading(self, group_number: int) -> str:
        return (
            PAGE_BEGIN + self.name + "]" +
            self._generate_name_and_surname(group_number) +
            self._generate_points_table() +
            self._generate_test_name() +
            PAGE_END
        )

    def _generate_name_and_surname(self, group_number: int) -> str:
        name = "\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots"
        if self.student_test is not None:
            if self.student_test.write_student_name:
                student: User = self.student_test.students.all().order_by("id")[group_number-1]
                name = student.first_name + " " + student.last_name + "\dots\dots\dots\dots"
        return """
        \\lhead
        {Imię i nazwisko: """ + name + """}
        \\rhead
        {Klasa: \dots, grupa
        """ + str(group_number) + "} \n"

    def _generate_points_table(self):
        table = "\\begin{center} \\begin{tabular}{ |p{30mm}|c|c|c|c| } \n \\hline "
        table += " Umiejętność & Strona & Podstawowy & Śr.-zaaw. & Zaawansowany \\\\ \n \\hline \n"
        if self.test:
            choice_tasks = ChoiceTestTask.objects.filter(test_id=self.test.id).all().order_by("skill__order")
            for choice_task in choice_tasks:
                row_header = choice_task.skill.title
                tasks = TestTask.objects.filter(choice_test_task__id=choice_task.pk)
                table += f"""{row_header} & {choice_task.page} &
                            {'' if tasks.filter(skill_level__level=1).first() is not None else 'X'} &
                            {'' if tasks.filter(skill_level__level=2).first() is not None else 'X'} &
                            {'' if tasks.filter(skill_level__level=3).first() is not None else 'X'}
                             \\\\ [3ex] \n \\hline \n """
        else:
            all_tasks = TestTask.objects.filter(student_test_id=self.student_test.id).all().order_by("skill_level_id")
            skill_tasks = defaultdict(list)
            for task in all_tasks:
                skill_tasks[task.skill_level.skills.first().title].append(task)
            for skill_title, tasks in skill_tasks.items():
                levels = [task.skill_level.level for task in tasks]
                pages = [task.page for task in tasks]
                table += f"""{skill_title} &
                            {'' if len([lvl for lvl in levels if lvl=="1"])>0 else 'X'} &
                            {'' if len([lvl for lvl in levels if lvl=="2"])>0 else 'X'} &
                            {'' if len([lvl for lvl in levels if lvl=="3"])>0 else 'X'} &
                            {pages} \\\\ [3ex] \n \\hline \n """
        table += " \\end{tabular} \\end{center}"
        return table

    def _generate_test_name(self):
        return """
        \\begin{center}
            \\Large	\\textbf{[""" + self.stage_title + """] -- """ + self.name + """ } -- """ + self.date.__str__() + """
        \\end{center}
        \\begin{center}
            \\Large	Powodzenia!
        \\end{center}
        """
