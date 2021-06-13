from tempfile import NamedTemporaryFile

from openpyxl import Workbook
from flask import send_file


def send_excel(workbook: Workbook, download_name):
    with NamedTemporaryFile() as tmp:
        workbook.save(tmp.name)

        return send_file(
            tmp.name,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=download_name,
        )
