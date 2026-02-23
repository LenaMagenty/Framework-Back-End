import random

import pytest
from faker import Faker

from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.university_service import UniversityService
from utils.assertions import soft_assert_equal

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

        errors: list[str] = []

        soft_assert_equal(updated_student_response.id, student_response.id,
                          "Wrong student id after update.", errors)

        soft_assert_equal(updated_student_response.last_name, new_last_name,
                          "Last name wasn't updated.", errors)

        soft_assert_equal(updated_student_response.first_name, student_response.first_name,
                          "First name changed unexpectedly.", errors)

        soft_assert_equal(updated_student_response.email, student_response.email,
                          "Email changed unexpectedly.", errors)

        soft_assert_equal(updated_student_response.group_id, student_response.group_id,
                          "Group id changed unexpectedly.", errors)

        assert not errors, "Soft-assert failures:\n" + "\n".join(errors)
