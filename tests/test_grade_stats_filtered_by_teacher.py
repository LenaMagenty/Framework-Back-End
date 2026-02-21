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
    def test_grade_stats_filtered_by_teacher(self, university_api_utils_admin):
        university_service = UniversityService(api_utils=university_api_utils_admin)

        Logger.info('### Step 1. Create group')
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group_request=group)

        Logger.info('### Step 2. Create teachers')
        teacher_a = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice([option for option in SubjectEnum])
        )
        teacher_a_response = university_service.create_teacher(teacher_request=teacher_a)

        teacher_b = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice([option for option in SubjectEnum])
        )
        teacher_b_response = university_service.create_teacher(teacher_request=teacher_b)

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

        Logger.info('### Step 4. Create grades for two teachers')
        grades_a = [2, 5]
        grades_b = [1, 1, 4]

        for value in grades_a:
            grade = GradeRequest(
                teacher_id=teacher_a_response.id,
                student_id=student_response.id,
                grade=value
            )
            university_service.create_grade(grade_request=grade)

        for value in grades_b:
            grade = GradeRequest(
                teacher_id=teacher_b_response.id,
                student_id=student_response.id,
                grade=value
            )
            university_service.create_grade(grade_request=grade)

        Logger.info('### Step 5. Get stats filtered by teacher A and validate')
        stats = university_service.get_grades_stats(teacher_id=teacher_a_response.id)

        expected_avg = sum(grades_a) / len(grades_a)

        assert stats.count == len(grades_a), \
            (f"Wrong count for teacher filter. Actual: '{stats.count}', "
             f"but expected: '{len(grades_a)}'")

        assert stats.min == min(grades_a), \
            (f"Wrong min for teacher filter. Actual: '{stats.min}', "
             f"but expected: '{min(grades_a)}'")

        assert stats.max == max(grades_a), \
            (f"Wrong max for teacher filter. Actual: '{stats.max}', "
             f"but expected: '{max(grades_a)}'")

        assert stats.avg == pytest.approx(expected_avg, 0.01), \
            (f"Wrong avg for teacher filter. Actual: '{stats.avg}', "
             f"but expected: '{expected_avg}'")
