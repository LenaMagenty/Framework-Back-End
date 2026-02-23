import random
import pytest
from faker import Faker

from logger.logger import Logger
from services.university.models.base_teacher import SubjectEnum
from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.models.grade_request import GradeRequest
from services.university.university_service import UniversityService
from utils.assertions import soft_assert_equal

faker = Faker()


@pytest.mark.service
class TestGradesStats:

    @pytest.mark.parametrize(
        'grades, '
        'expected_count, '
        'expected_min, '
        'expected_max, '
        'expected_avg',
        [
            ([2, 4, 5], 3, 2, 5, 3.67),
            ([5, 5, 5], 3, 5, 5, 5.0),
            ([0, 5], 2, 0, 5, 2.5),
            ([4], 1, 4, 4, 4.0)
        ]
    )
    def test_grade_stats_calculation(
            self,
            university_api_utils_admin,
            grades,
            expected_count,
            expected_min,
            expected_max,
            expected_avg
    ):
        university_service = (UniversityService
                              (api_utils=university_api_utils_admin))

        Logger.info('### Step 1. Create group')
        group = GroupRequest(name=faker.name())
        group_response = (university_service.create_group
                          (group_request=group))

        Logger.info('### Step 2. Create teacher')
        teacher = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice([option for option in SubjectEnum])
        )
        teacher_response = (university_service.create_teacher
                            (teacher_request=teacher))

        Logger.info('### Step 3. Create student')
        student = StudentRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice([option for option in DegreeEnum]),
            phone=faker.numerify('+7##########'),
            group_id=group_response.id
        )
        student_response = (university_service.create_student
                            (student_request=student))

        Logger.info('### Step 4. Create grades')
        for value in grades:
            grade_request = GradeRequest(
                teacher_id=teacher_response.id,
                student_id=student_response.id,
                grade=value
            )
            (university_service.create_grade
             (grade_request=grade_request))

        Logger.info('### Step 5. Verify stats')
        stats = (university_service.get_grades_stats
                 (student_id=student_response.id))

        errors: list[str] = []

        soft_assert_equal(stats.count, expected_count,
                          "Wrong count.", errors)

        soft_assert_equal(stats.min, expected_min,
                          "Wrong min.", errors)

        soft_assert_equal(stats.max, expected_max,
                          "Wrong max.", errors)

        soft_assert_equal(pytest.approx(stats.avg, abs=0.01),
                          pytest.approx(expected_avg, abs=0.01),
                          "Wrong avg.", errors)

        assert not errors, "Soft-assert failures:\n" + "\n".join(errors)
