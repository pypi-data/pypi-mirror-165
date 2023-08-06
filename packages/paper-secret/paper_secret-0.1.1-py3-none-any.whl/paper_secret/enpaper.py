#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import tempfile
from pathlib import Path
import sys
import paper_secret.util as util


def main():
    assert len(sys.argv) == 2, 'Expected one argument'
    split_encode(Path(sys.argv[1]))


def split_encode(
        secret: Path,
        k: int = 3,
        n: int = 5,
        create_qr_codes: bool = True,
        merge_qr_codes: bool = True,
        create_text_pdf: bool = True
) -> list[Path]:
    """
    Creates a file ending in `_txt.txt`. This file consists of n lines.
    k of these n lines are enough to reconstruct the secret.

    The same content is also stored in a `.pdf` file.
    The lines are split up into n blocks of grouped lines.
    k of these n blocks are enough to reconstruct the secret.

    Each line is also available as QR-code inside a `.pdf` file.

    :param secret: File containing a secret.
    :param k: Threshold for recombination.
    :param n: Number of shares to generate
    :return: List of created files.
    """
    assert secret.exists(), str(secret)
    assert secret.is_file(), str(secret)

    txt_file = secret.parent.joinpath(secret.name + '.split-text.txt')
    qr_pdf = secret.parent.joinpath(secret.name + '.split-QR.pdf')
    txt_pdf = secret.parent.joinpath(secret.name + '.split-text.pdf')
    assert not txt_file.exists() and not qr_pdf.exists() and not txt_pdf.exists()

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = Path(tmpdirname)
        tmpdirfile = tmpdir.joinpath('_')

        # Creates n files _.xxx
        # One can reconstruct secret based on k out of n files
        util.execute_stdin_capture(['gfsplit', '-n', str(k), '-m', str(n), str(secret), str(tmpdirfile)])

        qrcodes = []
        lines = ''
        for part in tmpdir.iterdir():
            binary_part = part.read_bytes()
            encoded_part = base64.b64encode(binary_part).decode('UTF-8')
            encoded_suffix = part.suffix[1:]

            suffix_and_content = encoded_suffix + encoded_part
            lines = lines + suffix_and_content + '\n'

            encoded = part.parent.joinpath(part.name + '.txt')
            encoded.write_text(suffix_and_content)

            if create_qr_codes:
                qrcode = part.parent.joinpath(part.name + '.png')
                qrcodes.append(qrcode)
                util.execute_stdin_capture(['qrencode', '-o', str(qrcode), '-s', '10'],
                                           suffix_and_content.encode('UTF-8'))

        txt_file.write_text(lines)

        if create_text_pdf:
            txt_ps = tmpdir / 'txt.ps'
            command = ['enscript', '-B', '--margins=24:24:', '-o', str(txt_ps), '-f', 'Courier@12/12']
            util.execute_stdin_capture(command, lines.replace('\n', '\n\n\n').encode('UTF-8'))

            util.execute_stdin_capture(['ps2pdf', str(txt_ps), str(txt_pdf)])

        if create_qr_codes and merge_qr_codes:
            command = ['convert'] + [str(qrcode) for qrcode in qrcodes] + [str(qr_pdf)]
            util.execute_stdin_capture(command)

    files = [txt_file]
    if create_text_pdf:
        files.append(txt_pdf)
    if create_qr_codes and merge_qr_codes:
        files.append(qr_pdf)
    return files


if __name__ == '__main__':
    main()
