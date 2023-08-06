import requests
import json

from tasq_cli import credentials
from tasq_cli.settings import SERVER, get_logger

logger = get_logger()
HEADERS = {
    "Authorization": f"BEARER {credentials.TOKEN}",
    "authority": 'console.tasq.ai',
}


def add_bulk_tag(tag, **query_params):
    query = '&'.join([f'filter%5B{param[0]}%5D={param[1]}' for param in query_params.items()])
    headers = HEADERS
    headers['accept'] = 'application/vnd.api+json'
    headers['Content-type'] = 'application/x-www-form-urlencoded'
    url = f'{SERVER}/project_resources/bulk_action/?{query}'
    data = '&'.join(f'{k}={p}' for k, p in query_params.items()) + f'&add_tag_name={tag}'
    response = requests.post(url, headers=headers, data=data)
    return response


def add_tags(tag, **query_params):
    query = '/?' + '&'.join([f'filter%5B{param[0]}%5D={param[1]}' for param in query_params.items()])
    query = query + '&page%5Bsize%5D=5000'
    url = f'{SERVER}/project_resources{query}'
    response = requests.get(url=url, headers=HEADERS)
    if response.status_code == 200:
        prs = response.json()
        logger.info("Tagging Project Resources")
        for pr in prs['data']:
            pr_id, tags = pr['id'], pr['attributes']['tagNames']
            batch = pr['relationships']['batch']['data']['id']
            step = pr['relationships']['step']['data']['id']
            logger.debug(f"Tagging project resource {pr_id}")
            add_tag(pr_id, tags, tag, batch, step)
            print(pr_id, tags, tag, batch, step)
    else:
        raise Exception(f"Response from server had status code other than 200; {response.content}")


def add_tag(project_resource_id, current_tags, tag, batch_id, step_id):
    url = f"{SERVER}/project_resources/{project_resource_id}"
    headers = HEADERS
    headers['accept'] = 'application/vnd.api+json'
    headers['Content-type'] = 'application/vnd.api+json'
    payload = {
        "data": {
            "id": str(project_resource_id),
            "type": "projectResources",
            "attributes": {
                "tagNames": list((*current_tags, tag)),
                "batchId": str(batch_id),
                "stepId": str(step_id),
            },
        }
    }
    return requests.patch(url=url, data=json.dumps(payload), headers=headers)


if __name__ == '__main__':
    pass
