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
from datetime import datetime

import numpy as np
import pandas as pd

from stylo_metrix.utils import mean, median, stdev

log = logging.getLogger(__name__)


def write_csv(
        docs,
        target_path,
        name,
        codes,
        descriptions,
        aggregate,
        filenames,
        transpose,
        time):
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        log.info(f"Created directory {target_path}")

    filename = f"{target_path}/{name}" + (f"_{_get_time()}" if time else "") + ".csv"

    n = [doc._.name for doc in docs]
    d = [doc._.smv.get_values() for doc in docs]
    c = docs[0]._.smv.get_codes()
    df = pd.DataFrame(d, columns=c)
    df.insert(0, "name", n)
    df.to_csv(filename, sep=';', encoding='utf-8-sig', header=True, index=False)
    log.info(f"Saved output as {filename}")


def write_npy(
        docs,
        target_path,
        name,
        transpose,
        time):
    filename = f"{target_path}/{name}" + (f"_{_get_time()}" if time else "") + ".npy"
    data = np.array([doc._.smv.get_values() for doc in docs])
    if transpose:
        data = data.T
    np.save(filename, data)
    log.info(f">>> Saved output as {filename}")


def write_text(content, path):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)


def _get_time():
    return datetime.now().strftime("%Y-%m-%d_%H-%M")

