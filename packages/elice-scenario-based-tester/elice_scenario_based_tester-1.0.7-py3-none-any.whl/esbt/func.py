from __future__ import annotations

import re
from io import BufferedReader
from typing import Any, Dict, Union

from aiohttp import FormData

from esbt import constants as script_c


class ScenarioException(Exception):
    pass


def extract_data_from_res(
    response: Any,
    extract_fields: list[str],
) -> Any:
    extracts: list[Union[str, int]] = []

    for field in extract_fields:
        index_field = re.compile(r'(.*)\[(\d+)\]$').search(field)
        if index_field is None:
            extracts.append(field)
        else:
            extracts.append(index_field.group(1))
            extracts.append(int(index_field.group(2)))

    for extract in extracts:
        try:
            response = response[extract]
        except (IndexError, KeyError, TypeError):
            raise Exception(f'Not exist data : {extract}')

    return response


def make_form_data(
    data: Dict[str, Any],
    files: Dict[str, tuple[str, str]],
    opened_files: list[BufferedReader] | None = None,
) -> FormData:
    form_data = FormData()

    for field, (file, mode) in files.items():
        f = open(file, mode)
        form_data.add_field(
            field, f, content_type=script_c.FORM_DATA_CONTENT_TYPE)
        opened_files.append(f)

    for key, value in data.items():
        form_data.add_field(key, str(value))

    return form_data
