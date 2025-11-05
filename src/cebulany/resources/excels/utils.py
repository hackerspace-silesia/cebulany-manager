from tempfile import NamedTemporaryFile

from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.styles import NamedStyle, Font, PatternFill, Border, Side, Alignment
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock
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


def setup_styles(workbook, font_name='Calibri', font_size=10):
    thin = Side(border_style="thin", color="000000")
    border = Border(top=thin, left=thin, right=thin, bottom=thin)
    font_args = dict(name=font_name, size=font_size)
    number_format = '0.00 zł'

    header = NamedStyle(name="header")
    header.font = Font(bold=True, name=font_name, size=font_size + 2)
    header.alignment = Alignment(horizontal='center', vertical='center')
    header.border = border
    workbook.add_named_style(header)

    left_header = NamedStyle(name="left_header")
    left_header.font = Font(bold=True, **font_args)
    left_header.alignment.vertical = 'center'
    left_header.border = border
    workbook.add_named_style(left_header)

    inactive = NamedStyle(name="inactive")
    inactive.fill = PatternFill(start_color='D6D6D6', fill_type='solid')
    inactive.font = Font(bold=True, **font_args)
    inactive.border = border
    inactive.number_format = number_format
    inactive.alignment.vertical = 'center'
    workbook.add_named_style(inactive)

    bad = NamedStyle(name="bad")
    bad.font = Font(bold=True, color = 'C32148', **font_args)
    bad.border = border
    bad.number_format = number_format
    bad.alignment.vertical = 'center'
    workbook.add_named_style(bad)

    nice = NamedStyle(name="nice")
    nice.font = Font(bold=True, color='4D8C57', **font_args)
    nice.border = border
    nice.number_format = number_format
    nice.alignment.vertical = 'center'
    workbook.add_named_style(nice)

    ok = NamedStyle(name="ok")
    ok.font = Font(**font_args)
    ok.border = border
    ok.number_format = number_format
    ok.alignment.vertical = 'center'
    workbook.add_named_style(ok)

    wrap_text = NamedStyle(name="wrap_text")
    wrap_text.font = Font(**font_args)
    wrap_text.border = border
    wrap_text.number_format = number_format
    wrap_text.alignment.wrap_text = True
    wrap_text.alignment.vertical = 'center'
    workbook.add_named_style(wrap_text)

    wrap_text = NamedStyle(name="wrap_text_center")
    wrap_text.font = Font(**font_args)
    wrap_text.border = border
    wrap_text.number_format = number_format
    wrap_text.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    workbook.add_named_style(wrap_text)


def add_cell(sheet, value='', style='ok') -> Cell:
    cell = Cell(sheet)
    cell.value = value
    cell.style = style
    return cell


def color_text(s: str, color: str | None = None, bold: bool=False, font: str='Calibri', size: int=8):
    font = InlineFont(sz=size, b=bold, rFont=font, color=color)
    return TextBlock(font, s)