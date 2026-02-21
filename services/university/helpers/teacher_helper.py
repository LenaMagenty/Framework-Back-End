import requests

from services.general.helpers.base_helper import BaseHelper


class TeacherHelper(BaseHelper):
    ENDPOINT_PREFIX = '/teachers/'

    ROOT_ENDPOINT = f'{ENDPOINT_PREFIX}'

    def post_teacher(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def delete_teacher(self, teacher_id: int) -> requests.Response:
        endpoint = f'{self.ENDPOINT_PREFIX}{teacher_id}/'
        response = self.api_utils.delete(endpoint)
        return response