from tasq_cli.server import make_request


def get_export_link(export_file_id):
    url = f'/export_files/{export_file_id}/download/'
    r = make_request(url)
    return r.json()


def get_export_file(export_file_id):
    url = f'/export_files/{export_file_id}'
    r = make_request(url)
    data = r.json()['data']
    del data['relationships']
    return data
