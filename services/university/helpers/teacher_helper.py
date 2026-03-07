import requests

from services.general.helpers.base_helper import BaseHelper


class TeacherHelper(BaseHelper):
    ENDPOINT_PREFIX = '/teachers/'

    ROOT_ENDPOINT = f'{ENDPOINT_PREFIX}'
    ENDPOINT_TEACHER_ID = f"{ENDPOINT_PREFIX}{{teacher_id}}/"

    def post_teacher(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def delete_teacher(self, teacher_id: int) -> requests.Response:
        endpoint = self.ENDPOINT_TEACHER_ID.format(
            teacher_id=teacher_id
        )
        response = self.api_utils.delete(endpoint)
        return response