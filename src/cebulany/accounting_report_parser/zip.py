#!/usr/bin/env python3
from typing import IO
from zipfile import ZipFile

from .pdf import parse


def load_pdf_zip(zipfile: IO):
    with ZipFile(zipfile) as zip:
        filenames = zip.namelist()
        filenames.sort()

        for filename in filenames:
            with zip.open(filename) as file:
                yield from parse(file)
