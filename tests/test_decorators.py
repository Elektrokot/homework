import pytest

from src.decorators import log


# Тест 1: Проверяем, что при успешном выполнении функции выводятся правильные логи в консоль
def test_log_console(capsys):  # type: ignore[no-untyped-def]
    @log()
    def add(a, b):  # type: ignore[no-untyped-def]
        return a + b

    add(3, 5)

    captured = capsys.readouterr()
    assert "Calling function 'add' with args: (3, 5), kwargs: {}" in captured.out
    assert "Function 'add' returned: 8" in captured.out


# Тест 2: Проверяем, что при ошибке логируется сообщение и аргументы
def test_log_exception_console(capsys):  # type: ignore[no-untyped-def]
    @log()
    def divide(a, b):  # type: ignore[no-untyped-def]
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "Calling function 'divide' with args: (10, 0), kwargs: {}" in captured.out
    assert "raised exception: ZeroDivisionError: division by zero" in captured.out


# Тест 3: Проверяем, что логи успешно пишутся в файл
def test_log_file(tmpdir):  # type: ignore[no-untyped-def]
    log_file = tmpdir.join("test_log.txt")

    @log(filename=str(log_file))
    def multiply(a, b):  # type: ignore[no-untyped-def]
        return a * b

    multiply(4, 7)

    content = log_file.read()
    assert "Calling function 'multiply' with args: (4, 7), kwargs: {}" in content
    assert "Function 'multiply' returned: 28" in content


# Тест 4: Проверяем логирование ошибок в файл
def test_log_exception_file(tmpdir):  # type: ignore[no-untyped-def]
    log_file = tmpdir.join("error_log.txt")

    @log(filename=str(log_file))
    def subtract(a, b):  # type: ignore[no-untyped-def]
        return a - b

    with pytest.raises(Exception):
        subtract("hello", 5)  # Вызов с некорректными типами данных

    content = log_file.read()
    assert "Calling function 'subtract' with args: ('hello', 5), kwargs: {}" in content
    assert "raised exception: TypeError:" in content


# Тест 5: Убедимся, что результат функции не изменился
def test_function_result_unchanged():  # type: ignore[no-untyped-def]
    @log()
    def square(x):  # type: ignore[no-untyped-def]
        return x * x

    assert square(6) == 36
