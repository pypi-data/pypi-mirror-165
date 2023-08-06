import hashlib
from cndvra8._base import Base


class Vra8(Base):
    def __init__(self, host, creds={"username": None, "password": None}, access_token=None):
        self.host = host
        self.creds = creds
        self.access_token = access_token

    def connect(self):
        if self.access_token is not None:
            return True
        if self._build_connection() is True:
            return True
        return False

    def _build_connection(self):
        return False

    def deployment(self, deployment_id):
        pass

    def build_deployment_name(self, deploy_id, service_name, env):
        uuid = hashlib.md5(deploy_id.encode('utf-8')).hexdigest()[0:8]
        return f"vra_{service_name}-{env}-{uuid}"

    def rename_deployment(self, deploy_id, new_name):
        url = f"/deployment/api/deployments/{deploy_id}?apiVersion={self._api_version()}"
        body = {"name": new_name}
        response = self._query(url, "patch", json_data=body)
        if response is False or response.status_code != 200:
            return None
        return True
