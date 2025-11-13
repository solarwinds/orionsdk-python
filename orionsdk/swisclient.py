import requests
import json
from datetime import datetime


def _json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial


class SwisClient:
    def __init__(self, hostname, username, password, port=17774, verify=False, session=None, timeout=30):
        self.url = "https://{}:{}/SolarWinds/InformationService/v3/Json/".\
                format(hostname, port)
        self._session = session or requests.Session()
        self._session.auth = (username, password)
        self._session.headers.update({'Content-Type': 'application/json'})
        self._session.verify = verify
        self._timeout = timeout

    def query(self, query, **params):
        return self._req(
                "POST",
                "Query",
                {'query': query, 'parameters': params}).json()

    def invoke(self, entity, verb, *args):
        return self._req(
                "POST",
                "Invoke/{}/{}".format(entity, verb), args).json()

    def create(self, entity, **properties):
        return self._req(
                "POST",
                "Create/" + entity, properties).json()

    def read(self, uri):
        return self._req("GET", uri).json()

    def update(self, uri, **properties):
        self._req("POST", uri, properties)

    def bulkupdate(self, uris, **properties):
        self._req("POST", "BulkUpdate",
            {'uris': uris, 'properties': properties})

    def delete(self, uri):
        self._req("DELETE", uri)

    def bulkdelete(self, uris):
        self._req("POST", "BulkDelete", {'uris': uris})

    def _req(self, method, frag, data=None):
        resp = self._session.request(method, 
                                     self.url + frag,
                                     timeout = self._timeout,
                                     data=json.dumps(data, default=_json_serial))

        # try to extract reason from response when request returns error
        if 400 <= resp.status_code < 600:
            try:
                resp.reason = json.loads(resp.text)['Message']
            except:
                pass

        resp.raise_for_status()
        return resp
