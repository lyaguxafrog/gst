# -*- coding: utf-8 -*-

import segno


def gen_qr_code(data: str) -> None:
    """Generate QRCode.

    Args:
        data (str): Data to qr codding
    """
    qr = segno.make(data, error="L")  # минимальная коррекция ошибок
    qr.terminal(compact=True)
