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
import sys


def setup_logger(relative_path=None):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    sh_formatter = logging.Formatter("STYLOMETRIX - %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(sh_formatter)
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)

    if relative_path:
        file_name = get_logging_path(relative_path)
        fh_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh = logging.FileHandler(file_name, mode='a')
        fh.setFormatter(fh_formatter)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

    return logger


def get_logging_path(relative_path):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path
