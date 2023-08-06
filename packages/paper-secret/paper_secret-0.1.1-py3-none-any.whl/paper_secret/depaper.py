#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import tempfile
from pathlib import Path
import sys
import paper_secret.util as util


def main():
    assert len(sys.argv) == 2, 'Expected one argument'
    merge_decode(Path(sys.argv[1]))


def merge_decode(src: Path) -> Path:
    """
    :param src: A file with at least k non-empty lines.
    :return: Path to file containing reconstructed secret.
    """
    assert src.exists(), str(src)
    assert src.is_file(), str(src)

    content = src.read_text('UTF-8')
    # All non-empty lines
    lines = [line.strip() for line in content.splitlines()
             if len(line.strip()) > 0]
    assert len(lines) >= 2

    merged = src.parent.joinpath(src.name + '.merged.txt')
    assert not merged.exists()

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = Path(tmpdirname)

        parts = []
        for line in lines:
            assert len(line) >= 4

            encoded_suffix: str
            encoded_part: str
            encoded_suffix, encoded_part = line[0:3], line[3:]

            binary_part = base64.b64decode(encoded_part.encode('UTF-8'))

            part = tmpdir.joinpath('.' + encoded_suffix)
            part.write_bytes(binary_part)
            parts.append(part)

        command = ['gfcombine', '-o', str(merged)] + [str(part) for part in parts]
        util.execute_stdin_capture(command)

    return merged


if __name__ == '__main__':
    main()
