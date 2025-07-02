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
                    with open(filename, "a") as f:
                        f.write(msg_start + "\n")
                else:
                    print(msg_start)

                # Вызов самой функции
                result = func(*args, **kwargs)

                # Логирование успешного завершения
                msg_success = f"Function '{func.__name__}' returned: {result}"
                if filename:
                    with open(filename, "a") as f:
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
                    with open(filename, "a") as f:
                        f.write(msg_error + "\n")
                else:
                    print(msg_error)
                raise  # повторно выбрасываем исключение

        return wrapper

    return decorator


# Примеры использования декоратора
@log(filename="log_file.log")
# @log(filename=None)
def get_mask_account(account_number: str) -> str:
    masked_number = f"**{account_number[-4:]}"
    return masked_number


@log(filename="log_file.log")
# @log(filename=None)
def get_mask_card_number(card_number: str) -> str:
    return f"{card_number[:4]} {card_number[4:6]}" f"** **** {card_number[-4:]}"


@log("log_file.log")
def divide(a, b):  # type: ignore[no-untyped-def]
    return a / b


# Успешный вызов
# divide(10, 2)

# Вызов с ошибкой
# divide(5, 0)

if __name__ == "__main__":
    get_mask_account("12345678901234567890")
    get_mask_card_number("1234567890123456")
