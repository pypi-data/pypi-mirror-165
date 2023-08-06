from tasq_cli import settings
from tasq_cli.server import make_request


def detail_source_file(source_file_id):
    global logger
    logger = settings.get_logger()
    url = f'/source_files/{source_file_id}?'
    r = make_request(url)
    data = r.json()['data']
    del data['relationships']
    return data
