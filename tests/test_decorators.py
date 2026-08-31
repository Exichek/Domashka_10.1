import pytest

from src.decorators import log


def test_log_console_success(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверяет логирование успешного выполнения функции в консоль."""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(2, 3)
    captured = capsys.readouterr()

    assert result == 5
    assert "add ok: 5" in captured.out


def test_log_console_error(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверяет логирование ошибки в консоль."""

    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()

    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0), {}" in captured.out


def test_log_file_success(tmp_path) -> None:
    """Проверяет запись успешного выполнения функции в файл."""
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def multiply(a: int, b: int) -> int:
        return a * b

    result = multiply(4, 5)

    assert result == 20
    assert log_file.read_text(encoding="utf-8") == "multiply ok: 20\n"


def test_log_file_error(tmp_path) -> None:
    """Проверяет запись ошибки в файл."""
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    log_content = log_file.read_text(encoding="utf-8")

    assert "divide error: ZeroDivisionError" in log_content
    assert "Inputs: (10, 0), {}" in log_content
