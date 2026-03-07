import random

import pytest

from faker import Faker

from services.university.models.base_teacher import SubjectEnum
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService

faker = Faker()


@pytest.mark.service
class TestTeacherDelete:

    def test_delete_teacher_twice(self, university_api_utils_admin):
        university_service = UniversityService(api_utils=university_api_utils_admin)

        teacher = TeacherRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 subject=random.choice([option for option in SubjectEnum]))

        teacher_response = university_service.create_teacher(teacher_request=teacher)

        teacher_id = teacher_response.id

        university_service.delete_teacher(teacher_id=teacher_id)

        delete_again_response = university_service.delete_teacher(teacher_id=teacher_id)

        assert delete_again_response.detail == 'Teacher not found', (
            f"Unexpected message on second delete. "
            f"Actual: '{delete_again_response.detail}', "
            f"Expected: 'Teacher not found'"
        )
