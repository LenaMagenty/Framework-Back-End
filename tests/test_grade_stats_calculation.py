import random

import pytest
from faker import Faker

from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestGradesStats:
    def test_grade_stats_calculation(self, university_api_utils_admin):
        university_service = UniversityService(api_utils=university_api_utils_admin)

        Logger.info('### Step 1. Create group')
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group_request=group)

        Logger.info('### Step 2. Create teacher')
        teacher = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice([option for option in SubjectEnum])
        )
        teacher_response = university_service.create_teacher(teacher_request=teacher)

        Logger.info('### Step 3. Create student')
        student = StudentRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice([option for option in DegreeEnum]),
            phone=faker.numerify('+7##########'),
            group_id=group_response.id
        )
        student_response = university_service.create_student(student_request=student)

        assert student_response.group_id == group_response.id, \
            (f"Wrong group id. Actual: '{student_response.group_id}', "
             f"but expected: '{group_response.id}'")

        Logger.info('### Step 4. Create grades')
        grades = [2, 4, 5]

        for value in grades:
            grade = GradeRequest(
                teacher_id=teacher_response.id,
                student_id=student_response.id,
                grade=value
            )
            grade_response = university_service.create_grade(grade_request=grade)

            assert grade_response.teacher_id == teacher_response.id, \
                (f"Wrong teacher id in created grade. Actual: '{grade_response.teacher_id}', "
                 f"but expected: '{teacher_response.id}'")

            assert grade_response.student_id == student_response.id, \
                (f"Wrong student id in created grade. Actual: '{grade_response.student_id}', "
                 f"but expected: '{student_response.id}'")

            assert grade_response.grade == value, \
                (f"Wrong grade value. Actual: '{grade_response.grade}', "
                 f"but expected: '{value}'")

        Logger.info('### Step 5. Get grades stats and validate calculation')
        stats = university_service.get_grades_stats(student_id=student_response.id)

        expected_avg = sum(grades) / len(grades)

        assert stats.count >= len(grades), \
            (f"Wrong count. Actual: '{stats.count}', "
             f"but expected at least: '{len(grades)}'")

        assert stats.min == min(grades), \
            (f"Wrong min value. Actual: '{stats.min}', "
             f"but expected: '{min(grades)}'")

        assert stats.max == max(grades), \
            (f"Wrong max value. Actual: '{stats.max}', "
             f"but expected: '{max(grades)}'")

        assert stats.avg == pytest.approx(expected_avg, 0.01), \
            (f"Wrong avg value. Actual: '{stats.avg}', "
             f"but expected: '{expected_avg}'")
