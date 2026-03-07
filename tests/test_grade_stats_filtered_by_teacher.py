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
from utils.assertions import soft_assert_equal

faker = Faker()


@pytest.mark.service
class TestGradesStats:
    @pytest.mark.parametrize(
        "grades_a, grades_b",
        [
            ([2, 5], [1, 1, 4]),
            ([3, 3, 5], [2]),
            ([1], [5, 5, 5]),
        ]
    )
    def test_grade_stats_filtered_by_teacher(self,
                                             university_api_utils_admin,
                                             grades_a,
                                             grades_b):

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

        Logger.info('### Step 4. Create grades for two teachers')

        for value in grades_a:
            university_service.create_grade(
                grade_request=GradeRequest(
                    teacher_id=teacher_a_response.id,
                    student_id=student_response.id,
                    grade=value
                )
            )

        for value in grades_b:
            university_service.create_grade(
                grade_request=GradeRequest(
                    teacher_id=teacher_b_response.id,
                    student_id=student_response.id,
                    grade=value
                )
            )

        Logger.info('### Step 5. Get stats filtered by teacher A and validate')
        stats = university_service.get_grades_stats(
            teacher_id=teacher_a_response.id
        )

        expected_avg = sum(grades_a) / len(grades_a)

        errors: list[str] = []

        soft_assert_equal(
            stats.count,
            len(grades_a),
            "Wrong count for teacher filter.",
            errors
        )

        soft_assert_equal(
            stats.min,
            min(grades_a),
            "Wrong min for teacher filter.",
            errors
        )

        soft_assert_equal(
            stats.max,
            max(grades_a),
            "Wrong max for teacher filter.",
            errors
        )

        soft_assert_equal(
            round(stats.avg, 2),
            round(expected_avg, 2),
            "Wrong avg for teacher filter.",
            errors
        )

        assert not errors, "Soft-assert failures:\n" + "\n".join(errors)
