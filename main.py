import os


from src.csv_and_excel_input import read_csv_transactions, read_excel_transactions
from src.decorators import log
from src.generators import filter_by_currency

from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions
from src.widget import get_date, mask_account_card
from src.bank_operation import process_bank_search


@log(filename="logs/main.log")
def main():
    valid_number = {"1", "2", "3"}
    while True:
        print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        # Выбор источника данных
        choice = input("Введите номер пункта: ").strip()
        if choice in valid_number:
            break
        print(f"Статус операции недоступен.")

    if choice == "1":
        file_path = "data/operations.json"
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден.")
            return
        print("Для обработки выбран JSON-файл.")
        transactions = load_transactions(file_path)
    elif choice == "2":
        file_path = "input_data/transactions.csv"
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден.")
            return
        print("Для обработки выбран CSV-файл.")
        transactions = read_csv_transactions(file_path)
    elif choice == "3":
        file_path = "input_data/transactions_excel.xlsx"
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден.")
            return
        print("Для обработки выбран XLSX-файл.")
        transactions = read_excel_transactions(file_path)

    if not transactions:
        print("Не удалось загрузить транзакции.")
        return

    # Фильтрация по статусу
    valid_states = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        state = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).strip().upper()
        if state in valid_states:
            break
        print(f"Статус операции '{state}' недоступен.")

    print(f"Операции отфильтрованы по статусу '{state}'.")
    transactions = filter_by_state(transactions, state)

    # Сортировка по дате
    sort_choice = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if sort_choice == "да":
        order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        reverse = True if "убыв" in order else False
        transactions = sort_by_date(transactions, reverse=reverse)
        print(f"Операции отсортированы {'по убыванию' if reverse else 'по возрастанию'}.")

    # Фильтрация рублевых транзакций
    rub_only = input("Выводить только рублевые транзакции? Да/Нет\n").strip().lower()
    if rub_only == "да":
        transactions = list(filter_by_currency(transactions, "RUB"))
        print("Отфильтрованы только рублевые транзакции.")

    # Фильтрация по слову в описании
    word_filter = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower()
    if word_filter == "да":
        keyword = input("Введите слово для поиска в описании:\n").strip()
        try:
            transactions = process_bank_search(transactions, keyword)
            print(f"Отфильтрованы транзакции, содержащие слово '{keyword}'.")
        except TypeError as e:
            print(f"Ошибка при фильтрации: {e}")

    # Выбор количества транзакций для вывода
    limit = input("Введите количество транзакций для вывода (оставьте пустым для вывода всех):\n").strip()
    if limit.isdigit():
        limit = int(limit)
        transactions_to_display = transactions[:limit]  # Ограничиваем количество транзакций
        if transactions_to_display:
            print(f"Выводится {len(transactions_to_display)} транзакций из {len(transactions)} доступных.\n")
        else:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        transactions_to_display = transactions  # Выводим все транзакции
        if transactions_to_display:
            print(f"Выводятся все {len(transactions_to_display)} транзакций.\n")
        else:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")

    # Вывод информации о транзакциях
    for transaction in transactions_to_display:
        date = get_date(transaction.get("date", ""))
        description = transaction.get("description", "")
        from_info = mask_account_card(transaction.get("from", "")) if "from" in transaction else "Недоступно"
        to_info = mask_account_card(transaction.get("to", "")) if "to" in transaction else "Недоступно"
        amount = transaction.get("operationAmount", {}).get("amount", "0")
        currency = transaction.get("operationAmount", {}).get("currency", {}).get("code", "руб.")

        # Проверка на "открытие вклада"
        is_opening_deposit = "открытие" in description.lower()

        print(f"{date} {description}")
        if not is_opening_deposit and from_info:  # Выводим "from" только если это не открытие вклада
            print(f"{from_info} -> ", end="")
        print(f"{to_info}")
        print(f"Сумма: {amount} {currency}\n")

if __name__ == "__main__":
    main()

