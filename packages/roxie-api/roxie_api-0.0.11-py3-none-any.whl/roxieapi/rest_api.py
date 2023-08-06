import os
import warnings
from typing import List
from urllib.parse import urljoin

import requests


def upload_and_run(base_url, input_files: List[str]) -> tuple:
    model_name = _get_model_name(input_files)

    # init
    timestamp = _init_model(base_url, model_name)

    # upload
    _upload_input_files(base_url, model_name, timestamp, input_files)

    # run
    return _run_model(base_url, model_name, timestamp)


def _get_model_name(input_file_paths: List[str]) -> str:
    for input_file_path in input_file_paths:
        input_file = os.path.basename(input_file_path)
        if input_file.endswith(".data"):
            return input_file.replace(".data", "")

    raise AttributeError(
        f"The list of input files should contain a data file (*.data), got {input_file_paths}."
    )


def _init_model(base_url: str, model_name: str) -> str:
    url_init = urljoin(base_url, f"model/{model_name}")
    response_init = requests.post(url_init)
    if response_init.status_code != 200:
        raise RuntimeError(response_init.json()["detail"]["output"])

    return response_init.json()["timestamp"]


def _upload_input_files(base_url, model_name, timestamp, input_files) -> None:
    url_upload = urljoin(base_url, "model")
    files = [("files", open(input_file)) for input_file in input_files]
    data = {"model_name": model_name, "timestamp": timestamp}

    response = requests.post(url_upload, files=files, data=data)

    if response.status_code != 200:
        raise RuntimeError(response.json()["detail"]["output"])


def _run_model(base_url, model_name, timestamp) -> tuple:
    url = urljoin(base_url, f"model/{model_name}/{timestamp}/run")
    response = requests.post(url)

    if response.status_code != 200:
        raise RuntimeError(response.json()["detail"]["output"])

    output_lines = response.json()["output"].split("\n")
    model_name = response.json()["model_name"]
    timestamp = response.json()["timestamp"]
    return model_name, timestamp, output_lines


def download_artefact(base_url, model_name, timestamp, input_dir, artefact):
    artefact_url = urljoin(base_url, f"artefact/{model_name}/{timestamp}/{artefact}")
    response_artefact = requests.get(artefact_url)
    if response_artefact.status_code != 200:
        warnings.warn("The requested artefact %s is not available!" % artefact)
    with open(os.path.join(input_dir, artefact), "wb") as file:
        file.write(response_artefact.content)
