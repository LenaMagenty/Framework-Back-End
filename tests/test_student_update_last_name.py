import random

import pytest
from faker import Faker

from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.university_service import UniversityService
from utils.assertions import soft_assert_dict

faker = Faker()


@pytest.mark.service
class TestStudentUpdate:
    def test_student_update_last_name(self, university_api_utils_admin):
        university_service = UniversityService(api_utils=university_api_utils_admin)

        Logger.info('### Step 1. Create group')
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group_request=group)

        Logger.info('### Step 2. Create student')
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

        Logger.info('### Step 3. Update last name via PUT')
        new_last_name = faker.last_name()

        updated_student_request = StudentRequest(
            first_name=student_response.first_name,
            last_name=new_last_name,
            email=student_response.email,
            degree=student_response.degree,
            phone=student_response.phone,
            group_id=student_response.group_id
        )

        updated_student_response = university_service.update_student(
            student_id=student_response.id,
            student_request=updated_student_request
        )

        actual_data = {
            "id": updated_student_response.id,
            "last_name": updated_student_response.last_name,
            "first_name": updated_student_response.first_name,
            "email": updated_student_response.email,
            "group_id": updated_student_response.group_id
        }

        expected_data = {
            "id": student_response.id,
            "last_name": new_last_name,
            "first_name": student_response.first_name,
            "email": student_response.email,
            "group_id": student_response.group_id
        }

        soft_assert_dict(actual_data, expected_data)
