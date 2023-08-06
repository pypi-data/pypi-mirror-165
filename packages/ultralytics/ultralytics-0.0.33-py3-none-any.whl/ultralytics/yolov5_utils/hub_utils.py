import shutil

import requests

from ..yolov5_utils.general import PREFIX, emojis


def check_dataset_disk_space(url='https://github.com/ultralytics/yolov5/releases/download/v1.0/coco128.zip', sf=2.0):
    # Check that url fits on disk with safety factor sf, i.e. require 2GB free if url size is 1GB with sf=2.0
    gib = 1 / 1024 ** 3  # bytes to GiB
    data = int(requests.head(url).headers['Content-Length']) * gib  # dataset size (GB)
    total, used, free = (x * gib for x in shutil.disk_usage("/"))  # bytes
    print(f'{PREFIX}{data:.3f} GB dataset, {free:.1f}/{total:.1f} GB free disk space')
    if data * sf < free:
        return True  # sufficient space
    s = f'{PREFIX}WARNING: Insufficient free disk space {free:.1f} GB < {data * sf:.3f} GB required, ' \
        f'training cancelled ❌. Please free {data * sf - free:.1f} GB additional disk space and try again.'
    print(emojis(s))
    return False  # insufficient space


def split_key(key=''):
    # Verify and split a 'api_key[sep]model_id' string, sep is one of '.' or '_'
    # key = 'ac0ab020186aeb50cc4c2a5272de17f58bbd2c0_RqFCDNBxgU4mOLmaBrcd'  # example
    # api_key='ac0ab020186aeb50cc4c2a5272de17f58bbd2c0', model_id='RqFCDNBxgU4mOLmaBrcd'  # example
    import getpass

    s = emojis(f'{PREFIX}Invalid API key ⚠️\n')  # error string
    if not key:
        key = getpass.getpass('Enter model key: ')
    sep = '_' if '_' in key else '.' if '.' in key else None  # separator
    assert sep, s
    api_key, model_id = key.split(sep)
    assert len(api_key) and len(model_id), s
    return api_key, model_id
