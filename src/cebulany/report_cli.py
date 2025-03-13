import argparse

from cebulany.app import app
from cebulany.resources.report import make_workbook


if __name__ == "__main__":
    with app.app_context():
        wb = make_workbook()
    wb.save("/data/report.xlxs")