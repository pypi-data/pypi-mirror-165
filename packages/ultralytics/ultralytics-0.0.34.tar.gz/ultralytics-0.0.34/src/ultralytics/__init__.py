__version__ = '0.0.34'  # print(ultralytics.__version__)

import requests

from .main import connect_to_hub, train_model
from .yolov5_utils.general import LOGGER, PREFIX, check_requirements, colorstr, emojis, is_colab
from .yolov5_utils.hub_utils import split_key


def checks(verbose=True):
    # Check system software and hardware
    from .yolov5_wrapper import clone_yolo

    clone_yolo()

    print('Checking setup...')

    import os
    import shutil

    from .yolov5_utils.torch_utils import select_device  # imports

    check_requirements(('psutil', 'IPython'))
    import psutil
    from IPython import display  # to display images and clear console output

    if is_colab():
        shutil.rmtree('sample_data', ignore_errors=True)  # remove colab /sample_data directory

    if verbose:
        # System info
        # gb = 1 / 1000 ** 3  # bytes to GB
        gib = 1 / 1024 ** 3  # bytes to GiB
        ram = psutil.virtual_memory().total
        total, used, free = shutil.disk_usage("/")
        display.clear_output()
        s = f'({os.cpu_count()} CPUs, {ram * gib:.1f} GB RAM, {(total - free) * gib:.1f}/{total * gib:.1f} GB disk)'
    else:
        s = ''

    select_device(newline=False, version=__version__)
    print(emojis(f'Setup complete ✅ {s}'))


def login(api_key=''):
    # Login to Ultralytics HUB
    connect_to_hub(api_key, verbose=True)


def start(key=''):
    # Start training models with Ultralytics HUB. Usage: from src.ultralytics import start; start('API_KEY')
    api_key, model_id = split_key(key)
    train_model(api_key=api_key, model_id=model_id)


def reset_model(key=''):
    # Reset a trained model to an untrained state
    api_key, model_id = split_key(key)
    r = requests.post('https://api.ultralytics.com/model-reset',
                      json={"apiKey": api_key, "modelId": model_id})

    if r.status_code == 200:
        LOGGER.info(f"{PREFIX}model reset successfully")
        return
    LOGGER.warning(f"{PREFIX}model reset failure {r.status_code} {r.reason}")


def export_model(key='', format='torchscript'):
    # Export a model to all formats
    api_key, model_id = split_key(key)
    formats = ('torchscript', 'onnx', 'openvino', 'engine', 'coreml', 'saved_model', 'pb', 'tflite', 'edgetpu', 'tfjs',
               'ultralytics_tflite', 'ultralytics_coreml')
    assert format in formats, f"ERROR: Unsupported export format '{format}' passed, valid formats are {formats}"

    r = requests.post('https://api.ultralytics.com/export',
                      json={"apiKey": api_key, "modelId": model_id, "format": format})
    assert r.status_code == 200, f"{PREFIX}{format} export failure {r.status_code} {r.reason}"
    LOGGER.info(f"{PREFIX}{format} export started ✅")


def get_export(key='', format='torchscript'):
    # Get an exported model dictionary with download URL
    api_key, model_id = split_key(key)
    formats = ('torchscript', 'onnx', 'openvino', 'engine', 'coreml', 'saved_model', 'pb', 'tflite', 'edgetpu', 'tfjs',
               'ultralytics_tflite', 'ultralytics_coreml')
    assert format in formats, f"ERROR: Unsupported export format '{format}' passed, valid formats are {formats}"

    r = requests.post('https://api.ultralytics.com/get-export',
                      json={"apiKey": api_key, "modelId": model_id, "format": format})
    assert r.status_code == 200, f"{PREFIX}{format} get_export failure {r.status_code} {r.reason}"
    return r.json()
