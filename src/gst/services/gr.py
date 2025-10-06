# -*- coding: utf-8 -*-

import click
import qrcode


def gen_qr_code(data: str) -> None:
    """Generate QRCode.

    Args:
        data (str): Data to qr codding
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)

    matrix = qr.get_matrix()

    for i in range(0, len(matrix), 2):
        line = ""
        top = matrix[i]
        bottom = matrix[i + 1] if i + 1 < len(matrix) else [False] * len(top)
        for t, b in zip(top, bottom):
            if t and b:
                line += "█"
            elif t and not b:
                line += "▀"
            elif not t and b:
                line += "▄"
            else:
                line += " "
        click.echo(line)
