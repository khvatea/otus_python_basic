import json
import sys
from prettytable import PrettyTable
import difflib


def handbook_open(handbook_file: str) -> list:
    """
    Открыть справочкник телефонной книги
    :param handbook_file: JSON файл, содержащий записи контактов телефонной книги
    :return: Объект list, с контактами в формате dict
    """
    with open(handbook_file, "r", encoding='utf8') as handbook_json:
        return json.load(handbook_json)


def save_handbook(handbook_file: str, handbook: list):
    with open(handbook_file, "w", encoding='utf8') as handbook_json:
        json.dump(handbook, handbook_json, ensure_ascii=False, indent=4)


def handbook_show_all_rows(handbook: list, sort_by_field="name") -> str:
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


def update_raw(handbook: list, name: str, update_contact: dict):
    expected_field_names = {"name", "phone", "email", "address"}

    if isinstance(update_contact, dict):
        extra_keys = update_contact.keys() - expected_field_names

        if extra_keys:
            print(f"Ошибка при обновлении контакта. Лишние ключи: {extra_keys}")
        else:
            for contact in handbook:
                if contact["name"] == name:
                    contact.update(update_contact)
                    return contact
    else:
        print(f"""
        В функции передан: {type(update_contact)}
        Требуется dict
        """)


def delete_raw(handbook: list, name: str):
    for contact in handbook:
        if contact["name"] == name:
            handbook.remove(contact)
            return contact
    return None

def handbooks_compare(handbook_source: str, handbook_buffer: str):
    with open(handbook_source, "r", encoding='utf8') as source:
        source_json = json.load(source)

    with open(handbook_buffer, "r", encoding='utf8') as buffer:
        source_buffer = json.load(buffer)

    ret = []
    before = [str(raw) for raw in source_json]
    after = [str(raw) for raw in source_buffer]
    difflist = difflib.ndiff(before, after)

    for line in difflist:
        if line.startswith(u'+'):
            ret.append("\033[3m\033[32m{}\n".format(line))
        elif line.startswith(u'-'):
            ret.append("\033[3m\033[31m{}\n".format(line))
        elif line.startswith(u'?'):
            ret.append("{}\033[0m".format(line))
    return ret

######################
# Считываем файл и записываем в объект JSON
# hndbook = handbook_open("handbook.json")
#
# # Выводим записи справочника в таблице
# # print(show_all_handbook_rows(hndbook, "name"))
#
# # Запись строки в справочник
# add_raw(hndbook, {"name": "ЯТест Тестов", "phone": "+7 777 777-77-77", "email": "test.testov@example.com", "address": "кукуево"})
# print(show_all_handbook_rows(hndbook))
#
# find_contacts = find_raws(hndbook, "ЯТест")
# print(show_all_handbook_rows(find_contacts))
#
# print(update_raw(hndbook, "Елизар Сюзян", {"phone": "+7 777 777-77-78", "email": "test.testov@example.com", "address": "кукуево"}))
#

# print(delete_raw(hndbook, "Елизар Сюзян"))
#
# save_handbook("handbook_1.json", hndbook)

print(handbooks_compare("handbook.json", "handbook_1.json"))
sys.stdout.writelines(handbooks_compare("handbook.json", "handbook_1.json"))