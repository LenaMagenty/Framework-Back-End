import requests.status_codes
from faker import Faker

from services.university.helpers.teacher_helper import TeacherHelper

faker = Faker()


class TestTeacherDelete:

    def test_delete_teacher_success(self, university_api_utils_admin):
        teacher_helper = TeacherHelper(api_utils=university_api_utils_admin)

        create_response = teacher_helper.post_teacher(json={
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'subject': 'History'
        })

        assert create_response.status_code == requests.status_codes.codes.created, \
            (f"Wrong status code while creating teacher. "
             f"Actual: '{create_response.status_code}', "
             f"expected: '{requests.status_codes.codes.created}'")

        teacher_id = create_response.json().get('id')

        delete_response = teacher_helper.delete_teacher(teacher_id=teacher_id)

        assert delete_response.status_code == requests.status_codes.codes.ok, \
            (f"Wrong status code while deleting teacher. "
             f"Actual: '{delete_response.status_code}', "
             f"expected: '{requests.status_codes.codes.ok}'")

        assert delete_response.json().get('detail') == 'Teacher deleted', \
            (f"Wrong delete message. "
             f"Actual: '{delete_response.json()}', "
             f"expected: 'Teacher deleted'")

        delete_again_response = teacher_helper.delete_teacher(teacher_id=teacher_id)

        assert delete_again_response.status_code == requests.status_codes.codes.not_found, \
            (f"Wrong status code on second delete. "
             f"Actual: '{delete_again_response.status_code}', "
             f"expected: '{requests.status_codes.codes.not_found}'")
