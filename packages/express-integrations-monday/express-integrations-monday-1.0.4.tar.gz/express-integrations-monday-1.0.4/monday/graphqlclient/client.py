import time

import requests
import json


class GraphQLClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.token = None
        self.header_name = None

    def execute(self, query, variables=None):
        query_type = 'query' if 'query' in query else 'mutation'
        stripped_query = query.strip().lstrip(f"{query_type} {{")
        query_with_complexity = f"""{query_type} {{
          complexity {{
            reset_in_x_seconds,
            after,
            before,
            query
          }}
          {stripped_query}
        """
        r = self._send(query_with_complexity, variables)
        if 'errors' in r:
            raise Exception(', '.join([e['message'] if 'message' in e else str(e) for e in r['errors']]))

        # rate limiting
        complexity = r['data']['complexity']
        while complexity['before'] - complexity['query'] < 0:
            time.sleep(complexity['reset_in_x_seconds'] + 1)
            r = self._send(query_with_complexity, variables)
            complexity = r['data']['complexity']
        if r.status_code >= 400:
            raise Exception(r.text)
        if 'errors' in r:
            raise Exception(', '.join([e['message'] if 'message' in e else str(e) for e in r['errors']]))

    def inject_token(self, token, header_name='Authorization'):
        self.token = token
        self.header_name = header_name

    def _send(self, query, variables):
        payload = {'query': query}
        headers = {}
        files = None

        if self.token is not None:
            headers[self.header_name] = '{}'.format(self.token)

        if variables is None:
            headers['Content-Type'] = 'application/json'
            payload = json.dumps({'query': query}).encode('utf-8')
        elif variables.get('file', None) is not None:
            headers['content'] = 'multipart/form-data'
            files = [
                ('variables[file]', (variables['file'], open(variables['file'], 'rb')))
            ]

        try:
            response = requests.request("POST", self.endpoint, headers=headers, data=payload, files=files)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            print(e)
            raise e
