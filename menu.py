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
    for contact in handbook:
        pretty_table.add_row(list(contact.values()))

    return pretty_table.get_string(sortby=sort_by_field)


def add_raw(handbook: list, new_contact: dict):
    expected_field_names = {"name", "phone", "email", "address"}

    if isinstance(new_contact, dict):
        missing_keys = expected_field_names - new_contact.keys()
        extra_keys = new_contact.keys() - expected_field_names

        if missing_keys:
            print(f"Ошибка при записи контакта. Отсутствуют ключи: {missing_keys}")
        elif extra_keys:
            print(f"Ошибка при записи контакта. Лишние ключи: {extra_keys}")
        else:
            handbook.append(new_contact)
    else:
        print(f"""
        В функции передан: {type(new_contact)}
        Требуется dict
        """)


def find_raws(handbook: list, search_string: str, find_by_field="name") -> list:
    result = [contact for contact in handbook if search_string in contact[find_by_field]]
    return result


def update_raw(handbook: list, name: str, update_contact: dict) -> bool:
    is_update_contact = False
    expected_field_names = {"name", "phone", "email", "address"}

    if isinstance(update_contact, dict):
        extra_keys = update_contact.keys() - expected_field_names

        if extra_keys:
            print(f"Ошибка при обновлении контакта. Лишние ключи: {extra_keys}")
        else:
            for contact in handbook:
                if contact["name"] == name:
                    contact.update(update_contact)
                    is_update_contact = True
    else:
        print(f"""
        В функции передан: {type(update_contact)}
        Требуется dict
        """)
    return is_update_contact


def delete_raw():
    pass


######################
# Считываем файл и записываем в объект JSON
hndbook = open_handbook("handbook.json")

# Выводим записи справочника в таблице
# print(show_all_handbook_rows(hndbook, "name"))

# Запись строки в справочник
add_raw(hndbook, {"name": "ЯТест Тестов", "phone": "+7 777 777-77-77", "email": "test.testov@example.com", "address": "кукуево"})
print(show_all_handbook_rows(hndbook))

find_contacts = find_raws(hndbook, "ЯТест")
print(show_all_handbook_rows(find_contacts))

is_upd = update_raw(hndbook, "ЯТест Тестов", {"phone": "+7 777 777-77-78", "email": "test.testov@example.com", "address": "кукуево"})
print(show_all_handbook_rows(hndbook))
print(is_upd)

