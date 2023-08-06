# Copyright (C) 2022  NASK PIB
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import logging
import os
import re

import pandas as pd

from stylo_metrix.structures.errors import EmptyFileError

log = logging.getLogger(__name__)


def get_filepaths(dir_path):
    if not os.path.isdir(dir_path):
        log.info(f"Couldn't read files because {dir_path} is not a directory.")
        raise Exception
    data = [os.path.join(dir_path, file) for file in os.listdir(dir_path) if file.lower().endswith('.txt')]
    if len(data) == 0:
        log.info(f"No text files found in directory {dir_path}.")
        raise Exception
    data.sort(key=str.lower)
    return data


def read_file(path, accept_empty):
    def is_empty(content):
        return re.search(r'^\s*$', content)

    def get_filename(path):
        return os.path.split(path)[1][:-4]

    if not path.lower().endswith('.txt'):
        log.info(f"File {path} is not a text file.")
        raise Exception
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not accept_empty and is_empty(content):
                raise EmptyFileError
            content = content.replace("radem", "rodem")  # patch na KeyError w nlp("radem") po stronie Morfeusza
            name = get_filename(path)
            return name, content
    except FileNotFoundError:
        log.info(f"Couldn't find file {path}.")
        raise Exception
    except OSError:
        log.info(f"Couldn't read file {path} due to OS error.")
        raise Exception
    except EmptyFileError:
        log.info(f"Read an empty file: {path}, this not allowed by task parameters.")
        raise Exception
    except Exception:
        log.info(f"Couldn't read file {path} due to an unknown error.")
        raise Exception


def read_csv(path, text_column="text", name_column=None):
    df = pd.read_csv(path)
    texts = list(df[text_column])
    if name_column:
        names = [str(n) for n in list(df[name_column])]
        return zip(texts, names)
    return texts
