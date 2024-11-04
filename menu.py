import json
from prettytable import PrettyTable


def open_handbook(handbook_file: str) -> list:
    """
    Открыть справочкник телефонной книги
    :param handbook_file: JSON файл, содержащий записи контактов телефонной книги
    :return: Объект list, с контактами в формате dict
    """
    with open(handbook_file, "r") as handbook:
        return json.load(handbook)


def save_handbook():
    pass


def show_all_handbook_rows(handbook: list, sort_by_field="name") -> str:
    pretty_table = PrettyTable()

    # set table field names
    pretty_table.field_names = ["name", "phone", "email", "address"]
    pretty_table.align["name"] = "l"
    pretty_table.align["address"] = "l"

    # place all lines from the dictionary into a table
    for raw in handbook:
        pretty_table.add_row(list(raw.values()))

    return pretty_table.get_string(sortby=sort_by_field)


def add_raw(handbook: list, raw: dict):

    expected_field_names = {"name", "phone", "email", "address"}

    if isinstance(raw, dict):
        missing_keys = expected_field_names - raw.keys()
        extra_keys = raw.keys() - expected_field_names

        if missing_keys:
            print(f"Ошибка при записи контакта. Отсутствуют ключи: {missing_keys}")
        elif extra_keys:
            print(f"Ошибка при записи контакта.Лишние ключи: {extra_keys}")
        else:
            handbook.append(raw)
    else:
        print(f"""
        Для записи контакта в справочник используется словарь (dict)
        В функции передан: {type(raw)}
        """)


def find_raws(handbook: list, search_string: str, find_by_field="name") -> list:
    result = [raw for raw in handbook if search_string in raw[find_by_field]]
    return result


def update_raw():
    pass


def delete_raw():
    pass


######################
# Считываем файл и записываем в объект JSON
hndbook = open_handbook("handbook.json")

# Выводим записи справочника в таблице
# print(show_all_handbook_rows(hndbook, "name"))

# Запись строки в справочник
add_raw(hndbook, {"name": "ЯТест Тестов", "phone": "+7 777 777-77-77", "email": "test.testov@example.com", "address": "кукуево"})
# add_raw(hndbook, ["Тест Тестов", "+7 777 777-77-77", "test.testov@example.com", "кукуево"])

print(show_all_handbook_rows(hndbook))

find_contacts = find_raws(hndbook, "Калуга", "address")
print(show_all_handbook_rows(find_contacts))