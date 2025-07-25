def log(filename=None):  # type: ignore[no-untyped-def]
    """
    Декоратор для логирования вызова функции, её аргументов и результата.
    Если указан `filename`, лог записывается в файл. Иначе — выводится в консоль.
    В случае ошибки логируется сообщение об исключении и входные параметры функции.
    """

    def decorator(func):  # type: ignore[no-untyped-def]
        def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
            try:
                # Логирование начала вызова
                msg_start = f"Calling function '{func.__name__}' with args: {args}, kwargs: {kwargs}"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(msg_start + "\n")
                else:
                    print(msg_start)

                # Вызов самой функции
                result = func(*args, **kwargs)

                # Логирование успешного завершения
                msg_success = f"Function '{func.__name__}' returned: {result}"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(msg_success + "\n")
                else:
                    print(msg_success)

                return result

            except Exception as e:
                # Логирование ошибки
                msg_error = (
                    f"Function '{func.__name__}' raised exception: {type(e).__name__}:"
                    f" {e} with args: {args}, kwargs: {kwargs}"
                )
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(msg_error + "\n")
                else:
                    print(msg_error)
                raise  # повторно выбрасываем исключение

        return wrapper

    return decorator
