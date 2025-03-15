from tempfile import NamedTemporaryFile

from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.styles import NamedStyle, Font, PatternFill, Alignment, Border, Side
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


def setup_styles(workbook):
    thin = Side(border_style="thin", color="000000")
    border = Border(top=thin, left=thin, right=thin, bottom=thin)
    font_args = dict(name='Calibri', size=10)
    number_format = '0.00 zł'

    header = NamedStyle(name="header")
    header.font = Font(bold=True, name='Calibri', size=12)
    header.alignment = Alignment(horizontal='center')
    header.border = border
    workbook.add_named_style(header)

    left_header = NamedStyle(name="left_header")
    left_header.font = Font(bold=True, **font_args)
    left_header.border = border
    workbook.add_named_style(left_header)

    inactive = NamedStyle(name="inactive")
    inactive.fill = PatternFill(start_color='D6D6D6', fill_type='solid')
    inactive.font = Font(bold=True, **font_args)
    inactive.border = border
    inactive.number_format = number_format
    workbook.add_named_style(inactive)

    bad = NamedStyle(name="bad")
    bad.fill = PatternFill(start_color='f1b0b7', fill_type='solid')
    bad.font = Font(bold=True, **font_args)
    bad.border = border
    bad.number_format = number_format
    workbook.add_named_style(bad)

    nice = NamedStyle(name="nice")
    nice.fill = PatternFill(start_color='7fb88e', fill_type='solid')
    nice.font = Font(bold=True, **font_args)
    nice.border = border
    nice.number_format = number_format
    workbook.add_named_style(nice)

    ok = NamedStyle(name="ok")
    ok.font = Font(**font_args)
    ok.border = border
    ok.number_format = number_format
    workbook.add_named_style(ok)


def add_cell(sheet, value='', style='ok') -> Cell:
    cell = Cell(sheet)
    cell.value = value
    cell.style = style
    return cell
