import requests


class Base():
    def __init__(self, host, creds={"username": None, "password": None}, access_token=None):
        self.host = host
        self.creds = creds
        self.access_token = access_token
        self.default_headers = {}

    def _api_version(self):
        if self.version is None:
            self.version = self._get_version()
        return self.version

    def _get_version(self):
        return "123"  # to replace with real call

    def _query(self, url, method="get", json_data={}):
        if method not in ['get', 'post', 'delete', 'patch', 'put']:
            raise AttributeError("(CND) Method not allowed")
        full_url = f"{self.host}{url}"
        if method == 'get':
            response = requests.get(full_url, headers=self.default_headers, verify=False)

        if method in ['post', 'delete', 'patch', 'put']:
            response = getattr(requests, method)(full_url, headers=self.default_headers, json=json_data, verify=False)

        if response.status_code in [200, 201, 202, 404]:
            return response

        return False
