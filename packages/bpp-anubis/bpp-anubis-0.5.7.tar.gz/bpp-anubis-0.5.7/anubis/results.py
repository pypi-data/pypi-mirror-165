import json
import zipfile
import os
from json.decoder import JSONDecodeError
from pathlib import Path


def create_aggregate(files: list, aggregate_out_file):
    agg_fp = Path(aggregate_out_file)
    aggregate = []
    for fp in files:
        with open(fp, 'r') as f:
            try:
                current_file_data = json.load(f)
            except JSONDecodeError:
                current_file_data = []
            aggregate += current_file_data

    with agg_fp.open('w+', encoding='utf-8') as f:
        f.write(json.dumps(aggregate))


def zipper(dir_to_zip):
    best_zipper_ever = zipfile.ZipFile(f'{dir_to_zip}.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(dir_to_zip):
        for file in files:
            best_zipper_ever.write(
                os.path.join(root, file),
                os.path.relpath(
                    os.path.join(root, file),
                    os.path.join(dir_to_zip, '../..')
                )
            )

    best_zipper_ever.close()


def reformat(form: str):
    if form.lower().replace(' ', '').replace('-', '') == 'testrail':
        print('reformat for testrail')
    raise NotImplementedError
