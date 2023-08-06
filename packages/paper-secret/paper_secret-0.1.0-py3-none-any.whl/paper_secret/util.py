#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys
from pathlib import Path


def execute_stdin_capture(command: list[str], stdin: bytes = b'', cwd: Path = Path()):
    """
    Executes the given `command`, passes `stdin` into it and returns its stdout.

    :raises Exception: In case of non-zero exit code.
      This exception includes the exit_code, stdout and stderr in its message.
    """

    # If a Linux shell's locale is en_GB.UTF-8, the output will be encoded to UTF-8.
    encoding = 'UTF-8'
    assert sys.stdout.encoding.upper() == encoding

    completed = subprocess.run(
        command,
        capture_output=True,
        cwd=cwd,
        input=stdin,
    )
    if completed.returncode != 0:
        raise Exception(
            f'command: {command}\n'
            f'exit_code: {completed.returncode}\n'
            f'stdout: {completed.stdout}\n'
            f'stderr: {completed.stderr}'
        )
