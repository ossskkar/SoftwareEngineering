import pytest

from questing import Logger


def test_log(capsys):
    logger = Logger()
    msg = "Test message"
    expected_msg = f"[{logger.__class__.__name__}] {msg}"
    logger.log(msg)

    out, _ = capsys.readouterr()

    assert expected_msg in out

def test_log_multiple(capsys):
    logger = Logger()
    msg = "Test message"
    expected_msg = f"[{logger.__class__.__name__}] {msg}"
    logger.log(msg)

    out, _ = capsys.readouterr()

    assert expected_msg in out
