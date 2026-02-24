import requests

from services.general.helpers.base_helper import BaseHelper


class StudentHelper(BaseHelper):
    ENDPOINT_PREFIX = "/students/"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}"
    ENDPOINT_STUDENT_ID = f"{ENDPOINT_PREFIX}{{student_id}}/"

    def post_student(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def put_student(self, student_id: int, json: dict) -> requests.Response:
        endpoint = self.ENDPOINT_STUDENT_ID.format(
            student_id=student_id
        )
        response = self.api_utils.put(endpoint, json=json)
        return response
