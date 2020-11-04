import aiohttp
import json
from datetime import datetime


def _json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial


class ASyncSwisClient:
    def __init__(self, hostname, username, password, verify=False, session=None):
        self.url = "https://{}:17778/SolarWinds/InformationService/v3/Json/".\
            format(hostname)
        self.auth = aiohttp.BasicAuth(username, password, encoding='utf-8')
        self.verify = verify
        self._session = session or aiohttp.ClientSession(
            headers={'Content-Type': 'application/json'},
            auth=self.auth
        )

    async def query(self, query, **params):
        response = await self._req(
            "POST",
            "Query",
            {'query': query, 'parameters': params})
        return response

    async def invoke(self, entity, verb, *args):
        result = await self._req(
            "POST",
            "Invoke/{}/{}".format(entity, verb), args)
        return result

    async def create(self, entity, **properties):
        return await self._req(
            "POST",
            "Create/" + entity, properties)

    async def read(self, uri):
        return await self._req("GET", uri)

    async def update(self, uri, **properties):
        await self._req("POST", uri, properties)

    async def bulkupdate(self, uris, **properties):
        await self._req("POST", "BulkUpdate",
                        {'uris': uris, 'properties': properties})

    async def delete(self, uri):
        await self._req("DELETE", uri)

    async def _req(self, method, frag, data=None):
        resp = await self._session.request(method,
                                           self.url + frag,
                                           verify_ssl=self.verify,
                                           data=json.dumps(data, default=_json_serial))

        # try to extract reason from response when request returns error
        if 400 <= resp.status < 600:
            try:
                resp.reason = json.loads(resp.text)['Message']
            except:
                pass

        resp.raise_for_status()
        return await resp.json()

    async def close(self):
        await self._session.close()
