"""
A timer context manager to measure the time taken to execute each command in the CLI.
"""

import time
from contextlib import contextmanager

import click


@contextmanager
def timer(silent=False):
    start = time.time()
    yield
    end = time.time()
    if not silent:
        click.echo(f"Time taken: {end - start:.2f} seconds\n")
