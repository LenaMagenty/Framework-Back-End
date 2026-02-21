import requests

from services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades/"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}"
    STATS_ENDPOINT = f"{ENDPOINT_PREFIX}stats/"

    def get_grades_stats(self, **kwargs) -> requests.Response:
        response = self.api_utils.get(self.STATS_ENDPOINT, **kwargs)
        return response

    def post_grade(self, data: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, data=data)
        return response