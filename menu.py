import json
from dis import pretty_flags

from prettytable import PrettyTable


def open_handbook(handbook_file: str) -> list:
    """ Открыть справочкник телефонной книги
        :param handbook_file: JSON файл, содержащий записи контактов телефонной книги
        :return: Объект JSON, со справочником контактов
        """
    with open(handbook_file, "r") as handbook:
        return json.load(handbook)


def save_handbook():
    pass


def show_all_handbook_rows(handbook: list, sort_by_field=None) -> str:
    pretty_table = PrettyTable()

    # set table field names
    pretty_table.field_names = ["name", "phone", "email", "address"]
    pretty_table.align["name"] = "l"
    pretty_table.align["address"] = "l"

    # place all lines from the dictionary into a table
    for hb in handbook:
        pretty_table.add_row(list(hb.values()))

    return pretty_table.get_string(sortby=sort_by_field)


def add_raw():
    pass


def find_raw():
    pass


def update_raw():
    pass


def delete_raw():
    pass


######################
# Считываем файл и записываем в объект JSON
hndbook = open_handbook("handbook.json")

# Выводим записи справочника в таблице
print(show_all_handbook_rows(hndbook, "name"))