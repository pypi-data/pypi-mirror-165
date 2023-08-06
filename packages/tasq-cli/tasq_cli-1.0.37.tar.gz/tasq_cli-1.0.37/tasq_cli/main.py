import argparse
import logging
from datetime import datetime
from django.utils.text import slugify
from tasq_cli import jobs, export_files, credentials
from tasq_cli import projects
from tasq_cli import settings
from tasq_cli.upload import do_upload, create_csv_from_currently_uploaded_files, upload_csv


def main():
    parser = argparse.ArgumentParser(prog='tasq')
    parser.add_argument('-V', '--version', action='version', version=f'Tasq CLI {settings.VERSION}')
    parser.add_argument('-cf', '--config-file', action='store', help='use non-default config file')
    parser.add_argument('-d', '--dataset-name', action='store', help='set current dataset name')
    parser.add_argument('-c', '--client-id', action='store', help='override client id')
    parser.add_argument('-b', '--bucket-name', action='store', help='override bucket name')
    parser.add_argument('--silent', action='store_true', help='An opt-out from logging')

    # NOTE
    # in Python 3.8 you can pass an additional argument to add_subparsers
    # required=True
    subparsers = parser.add_subparsers(dest='action', metavar='action', help='action to run')

    images_parser = subparsers.add_parser('upload', help='upload files')
    images_parser.add_argument('-p', '--path', default=False, help='path to directory with images')
    images_parser.add_argument('-e', '--exclude', help='File extensions to exclude.', action='append', nargs='*')
    images_parser.add_argument('-u', '--url-prefix', action='store', help='specify the prefix of files to upload')
    images_parser.add_argument('--dry', help='create upload file but dont actually upload anything', action='store_true')

    csv_parser = subparsers.add_parser('create-csv', help='create csv for files that were already uploaded')
    csv_parser.add_argument('-d', '--csv-dataset-name', action='store', help='dataset name of csv to create')
    csv_parser.add_argument('-f', '--file-name', action='store', help='one file from dataset of csv to create')
    csv_parser.add_argument('--dry', help='create upload file but dont actually upload anything', action='store_true')

    upload_csv_parser = subparsers.add_parser('upload-csv', help='upload files')
    upload_csv_parser.add_argument('project_id', default=False, help='project in which to run a job')
    upload_csv_parser.add_argument('file_name', help='csv file to upload to project')
    upload_csv_parser.add_argument('--tag', help='tag to set on all uploaded images. If not set, the file name will be the tag')
    upload_csv_parser.add_argument('--dry', help='run but dont actually upload anything', action='store_true')

    run_job_parser = subparsers.add_parser('run-job', help='run a job')
    run_job_parser.add_argument('project_id', default=False, help='project in which to run a job')
    run_job_parser.add_argument('--tag', help='tag to include')
    run_job_parser.add_argument('--type', help='job type: annotation/composite')

    list_job_parser = subparsers.add_parser('list-jobs', help='list all jobs in a project')
    list_job_parser.add_argument('project_id', help='the project id')

    export_job_parser = subparsers.add_parser('export-job', help='exports a job')
    export_job_parser.add_argument('job_id', help='the job id')
    export_job_parser.add_argument('--raw', action='store_true', help='the job id')
    export_job_parser.add_argument('--worker_data', action='store_true', help='include worker data')

    export_file_job_parser = subparsers.add_parser('create-job-export-file', help='creates an export file for a job')
    export_file_job_parser.add_argument('job_id', help='the job id')
    export_file_job_parser.add_argument('--raw', action='store_true', help='the job id')
    export_file_job_parser.add_argument('--worker_data', action='store_true', help='include worker data')

    export_file_project_parser = subparsers.add_parser('create-project-export-file', help='creates an export file for a project')
    export_file_project_parser.add_argument('project_id', help='the project id')
    export_file_project_parser.add_argument('--raw', action='store_true', help='the project id')
    export_file_project_parser.add_argument('--worker_data', action='store_true', help='include worker data')

    list_projects_parser = subparsers.add_parser('list-projects', help='list all projects')

    get_export_link = subparsers.add_parser(
        'get-export-link', help='get a link to an export file, which is not necessarily populated yet'
    )
    get_export_link.add_argument('export_file_id', help='the export file id')

    get_export_file = subparsers.add_parser('get-export-file', help='get export file details')
    get_export_file.add_argument('export_file_id', help='the export file id')

    args = parser.parse_args()
    if not args.silent:
        logger = settings.get_logger()
    else:
        logger = logging.getLogger('dummy')
        logger.addHandler(logging.NullHandler())

    logger.info(f'Tasq CLI {settings.VERSION}')

    credentials.load_credentials(args.config_file)  # If not specified, loads from default config path

    # override client id if flag is present
    if args.client_id:
        credentials.CLIENT_ID = args.client_id
        logger.info(f'Overriding client id with {credentials.CLIENT_ID}')

    # override bucket name if flag is present
    if args.bucket_name:
        if args.bucket_name == 'tasq':
            logger.info('Setting default bucket name gits-active-storage')
            credentials.BUCKET = 'gits-active-storage'
            logger.info('Setting CDN_URL to cdn.tasq.ai')
            settings.CDN_URL = 'https://cdn.tasq.ai/{object_name}'
        else:
            credentials.BUCKET = args.bucket_name
            logger.info(f'Overriding bucket name with {credentials.BUCKET}')

    if args.dataset_name:
        DATASET_NAME = slugify(f'{args.dataset_name}')
    else:
        # NOTE
        # This could be set as a default on line 13, but this way we get to
        # inform the user what is happening.
        dataset_timestamp = datetime.now().strftime("%Y-%m-%d")
        logger.warning(f'Dataset name required. Setting dataset name to {dataset_timestamp}')
        DATASET_NAME = dataset_timestamp

    if args.action == 'upload':
        if not args.path:
            logger.error('Path to upload is required.')
            exit(1)

        if args.url_prefix:
            settings.CDN_URL = f'{args.url_prefix}/{{object_name}}'
        elif credentials.URL_PREFIX:
            settings.CDN_URL = f'{credentials.URL_PREFIX}/{{object_name}}'

        settings.dry = args.dry
        do_upload(DATASET_NAME, args.path, args.exclude, settings)

    if args.action == 'create-csv':
        create_csv_from_currently_uploaded_files(args.csv_dataset_name, args.file_name, settings)

    if args.action == 'upload-csv':
        upload_csv(args.file_name, args.project_id, args.tag)

    result = None
    if args.action == 'run-job':
        result = jobs.run_job(args.project_id, args.tag)
    if args.action == 'list-jobs':
        result = jobs.list_jobs(args.project_id)
    if args.action == 'export-job':
        result = jobs.export_job(args.job_id, args.raw, args.worker_data)
    if args.action == 'create-job-export-file':
        result = jobs.create_job_export_file(args.job_id, args.raw, args.worker_data)
    if args.action == 'create-project-export-file':
        result = projects.create_project_export_file(args.project_id, args.raw, args.worker_data)
    if args.action == 'list-projects':
        result = projects.list_projects()
    if args.action == 'get-export-link':
        result = export_files.get_export_link(args.export_file_id)
    if args.action == 'get-export-file':
        result = export_files.get_export_file(args.export_file_id)

    if result:
        print(result)


if __name__ == "__main__":
    main()
