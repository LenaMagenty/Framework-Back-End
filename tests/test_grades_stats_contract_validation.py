import pytest
import requests.status_codes

from services.university.helpers.grade_helper import GradeHelper


@pytest.mark.api
class TestGradesStatsContract:
    def test_stats_invalid_student_id(self, university_api_utils_admin):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)

        response = grade_helper.get_grades_stats(student_id='abc')

        assert response.status_code == requests.status_codes.codes.unprocessable_entity, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected '{requests.status_codes.codes.unprocessable_entity}'")
