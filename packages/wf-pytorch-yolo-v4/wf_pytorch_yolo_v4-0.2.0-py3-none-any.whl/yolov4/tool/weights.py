import hashlib
import logging
import os
from pathlib import Path

from .base import data_dir

import requests


DARKNET_YOLOV4_URL = 'https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights'

# Thanks quantumSoup @ https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def validate_checksum(dest_path):
    return '00a4878d05f4d832ab38861b32061283' == md5(dest_path)


def download_weights(dest_path=None):
    if dest_path is None:
        dest_path = os.path.join(data_dir(), 'yolov4.weights')

    if Path(dest_path).is_file() and validate_checksum(dest_path):
        return dest_path

    for ii in range(3):
        if ii > 0:
            logging.warning("Checksum failed, retrying download...")

        try:
            with open(dest_path, 'wb') as weights_file:
                content = requests.get(DARKNET_YOLOV4_URL, stream=True).content
                weights_file.write(content)
            # gdd.download_file_from_google_drive(file_id=id,
            #                                     dest_path=dest_path,
            #                                     unzip=True,
            #                                     showsize=True,
            #                                     overwrite=overwrite)
        except Exception as e:
            logging.error('Error at %s', 'file download', exc_info=e)
            return None

        if validate_checksum(dest_path):
            return dest_path

    logging.error('Unable to validate file checksum')
    return None
