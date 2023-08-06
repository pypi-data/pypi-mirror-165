import json

from tasq_cli import settings
from tasq_cli.server import make_request

logger = None


def list_projects():
    global logger
    logger = settings.get_logger()
    url = f'/projects/?sort=-id&page[size]=100'
    r = make_request(url)
    data = r.json()['data']
    for j in data:
        del j['relationships']
    print(json.dumps(data))
    return


def create_project_export_file(project_id, raw, worker_data):
    global logger
    logger = settings.get_logger()

    url = f'/export_files'
    headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/vnd.api+json'}

    data = {
        'data': {
            "type": "exportFiles",
            "attributes": {
                "projectId": f'{project_id}',
                "type": 'raw' if raw else 'target',
                "allJudgements": worker_data and not raw,
                "includeWorkerData": worker_data and not raw,
            },
        }
    }

    r = make_request(url, headers=headers, json=data)
    data = r.json()['data']
    del data['relationships']
    return data
