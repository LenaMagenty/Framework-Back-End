import pytest
import requests.status_codes

from services.university.helpers.grade_helper import GradeHelper

@pytest.mark.api
class TestGradesStatsContract:
    def test_get_grades_stats_anonym(self, university_api_utils_anonym):
        grade_helper = GradeHelper(api_utils=university_api_utils_anonym)

        response = grade_helper.get_grades_stats()

        assert response.status_code == requests.status_codes.codes.forbidden, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected '{requests.status_codes.codes.unauthorized}'")
